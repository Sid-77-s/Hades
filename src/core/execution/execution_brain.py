from typing import List, Dict, Any, Optional
import os
import json
import asyncio
import uuid
from src.models.mission import Mission, MissionStatus
from src.core.execution.task_graph import TaskGraph, Task, TaskStatus
from src.core.execution.review_engine import ReviewEngine
from src.core.execution.uncertainty_engine import UncertaintyEngine
from src.core.event_bus import EventBus
from src.core.memory_manager import MemoryManager
from src.skills.registry import registry as skill_registry
from src.core.worker_manager import worker_manager

class ExecutionBrain:
    def __init__(self):
        self.review_engine = ReviewEngine()
        self.uncertainty_engine = UncertaintyEngine()
        self.event_bus = EventBus()
        self.memory_manager = MemoryManager()
        self.registry = skill_registry
        self.registry.discover_skills()
        os.makedirs("output", exist_ok=True)
        
    async def process_mission(self, mission: Mission):
        """
        Main background orchestration loop for an AUTHORIZED_EXECUTION mission.
        """
        if mission.status != MissionStatus.AUTHORIZED_EXECUTION:
            print("[ExecutionBrain] Mission not authorized for execution.")
            return

        mission.status = MissionStatus.BACKGROUND_WORK
        self.event_bus.publish_sync("MISSION_STATUS_UPDATED", {"mission_id": mission.id, "status": mission.status.value})
        
        # 1. Plan Generation
        task_graph = self._generate_plan(mission)
        self.event_bus.publish_sync("PLAN_CREATED", {
            "mission_id": mission.id, 
            "tasks": len(task_graph.tasks)
        })
        
        # 2. Execution Loop
        while not task_graph.is_complete() and not task_graph.has_failures():
            ready_tasks = task_graph.get_ready_tasks()
            
            if not ready_tasks:
                if not task_graph.is_complete():
                    task_graph.mark_failed("ALL", "Task deadlock - no ready tasks.")
                break
                
            for task in ready_tasks:
                await self._execute_task(mission, task, task_graph)
                
        # 3. Handle Completion or Failure
        if task_graph.is_complete():
            mission.status = MissionStatus.COMPLETED
            
            task_summaries = []
            for t in task_graph.tasks.values():
                if t.result:
                    task_summaries.append(f"- {t.objective}: {t.result[:300]}")
            raw_summary = "\n".join(task_summaries)
                    
            try:
                prompt = f"""You are Hades returning to the human partner after completing background Linux work.
The user's objective was: {mission.understanding.objective.value}
The results produced are:
{raw_summary[:1200]}

Generate a short, natural, conversational message telling the user you are back and summarizing what you did.
Personality: Calm, direct, intelligent, capable partner.
DO NOT say "Mission Complete" or "Task successfully executed".
Keep it under 3-4 sentences.
Example: "Done. I created the project structure, set up the configuration, and verified the services are running cleanly."
"""
                res = worker_manager.complete(
                    messages=[{"role": "system", "content": prompt}],
                    capability="fast",
                    max_tokens=150
                )
                final_msg = res.choices[0].message.content
                final_msg += f"\n\n---\n**Execution Summary:**\n{raw_summary}"
            except Exception as e:
                print(f"[ExecutionBrain] Failed to generate conversational return: {e}")
                final_msg = f"Done. I've finished the work.\n\n{raw_summary}"

            # Save to persistent memory
            self.memory_manager.add_mission_to_history(
                mission_id=mission.id,
                objective=mission.understanding.objective.value or "Execute request",
                status="COMPLETED",
                summary=final_msg,
                outputs=[t.result for t in task_graph.tasks.values() if t.result]
            )

            self.event_bus.publish_sync("MISSION_COMPLETED", {
                "mission_id": mission.id, 
                "result": final_msg
            })
        else:
            mission.status = MissionStatus.NEEDS_USER
            failed_reasons = [t.error for t in task_graph.tasks.values() if t.error]
            error_detail = "; ".join(failed_reasons) if failed_reasons else "Encountered a blocker during execution."
            
            self.event_bus.publish_sync("MISSION_BLOCKED", {
                "mission_id": mission.id, 
                "error": f"I ran into an issue: {error_detail}"
            })
            

    def _generate_plan(self, mission: Mission) -> TaskGraph:
        graph = TaskGraph(mission_id=mission.id)
        obj = mission.understanding.objective.value or "Execute user request"
        
        t1 = Task(
            id=f"task_{uuid.uuid4().hex[:8]}",
            mission_id=mission.id,
            objective=obj,
            allowed_capabilities=["terminal"],
            success_criteria=["Complete the requested objective cleanly"]
        )
        graph.add_task(t1)
        return graph

    async def _execute_task(self, mission: Mission, task: Task, graph: TaskGraph):
        task.status = TaskStatus.RUNNING
        self.event_bus.publish_sync("TASK_STARTED", {"task_id": task.id, "objective": task.objective})
        
        # 1. Match Skill
        skill = None
        for cap in task.allowed_capabilities:
            # Map capability alias if needed
            cat_name = "computer" if cap in ["terminal", "filesystem", "process_manager"] else cap
            
            # Direct skill id lookup first
            direct_skill = self.registry.get_skill(cap)
            if direct_skill and direct_skill.metadata.health_status in ["READY", "PARTIAL"]:
                skill = direct_skill
                break
                
            skills = self.registry.get_skills_by_category(cat_name.lower())
            healthy_skills = [s for s in skills if s.metadata.health_status in ["READY", "PARTIAL"]]
            if healthy_skills:
                skill = healthy_skills[0]
                break

        if not skill:
            skill = self.registry.get_skill("terminal") or self.registry.get_skill("filesystem")

        friendly_name = skill.metadata.name if skill else "Linux Execution Engine"
        self.event_bus.publish_sync("CAPABILITY_SELECTED", {"task_id": task.id, "adapter": friendly_name})
        
        # 2. Parameterize tool execution using worker intelligence
        params: Dict[str, Any] = {}
        skill_id = skill.metadata.skill_id if skill else "terminal"

        try:
            if skill_id == "terminal":
                cmd_prompt = f"""You are Hades generating the exact Linux bash command for a task.
Task Objective: {task.objective}
Workspace directory: {os.getcwd()}
Operating System: Ubuntu Linux (WSL2)

Return ONLY valid JSON with format:
{{
  "command": "The exact bash command to execute"
}}
Do NOT include backticks or markdown outside JSON.
"""
                res = worker_manager.complete(
                    messages=[{"role": "user", "content": cmd_prompt}],
                    capability="coding",
                    response_format={"type": "json_object"},
                    timeout=15
                )
                cmd_data = json.loads(res.choices[0].message.content)
                params["command"] = cmd_data.get("command", task.objective)
                params["cwd"] = os.getcwd()

            elif skill_id == "filesystem":
                fs_prompt = f"""You are Hades determining filesystem operations for a task.
Task Objective: {task.objective}
Workspace directory: {os.getcwd()}

Return ONLY valid JSON with format:
{{
  "action": "read | write | list | exists | mkdir | find | stat",
  "path": "path to file or directory",
  "content": "content to write if action is write"
}}
"""
                res = worker_manager.complete(
                    messages=[{"role": "user", "content": fs_prompt}],
                    capability="fast",
                    response_format={"type": "json_object"},
                    timeout=15
                )
                fs_data = json.loads(res.choices[0].message.content)
                params.update(fs_data)

            elif skill_id == "process_manager":
                params["action"] = "system_resources" if "resource" in task.objective.lower() else "list"

            elif skill_id == "web_search":
                params["query"] = task.objective

            elif skill_id == "browser_navigate":
                # Extract URL if present
                import re
                url_match = re.search(r"https?://[^\s]+", task.objective)
                params["url"] = url_match.group(0) if url_match else "https://duckduckgo.com"

            else:
                params = {
                    "command": task.objective,
                    "action": "write",
                    "path": os.path.join("output", "task_output.md"),
                    "content": f"# Output for: {task.objective}"
                }

            # 3. Execute Skill
            result = await skill.execute(params=params, context=mission.understanding.model_dump())
            
            # 4. Rigorous Review & Verification
            review = self.review_engine.review_task(task, result)
            
            if review.get("passed", False):
                result_summary = str(result.get("result") or result.get("stdout") or result)
                graph.mark_completed(task.id, result_summary)
                self.event_bus.publish_sync("TASK_COMPLETED", {"task_id": task.id, "result": "Verified output."})
            else:
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.RETRYING
                    self.event_bus.publish_sync("TASK_RETRYING", {"task_id": task.id, "feedback": review.get("feedback")})
                    # Re-attempt with retry feedback
                    await self._execute_task(mission, task, graph)
                else:
                    err_msg = review.get("feedback", "Review verification failed.")
                    graph.mark_failed(task.id, err_msg)
                    self.event_bus.publish_sync("TASK_FAILED", {"task_id": task.id, "error": err_msg})
                    
        except Exception as e:
            graph.mark_failed(task.id, str(e))
            self.event_bus.publish_sync("TASK_FAILED", {"task_id": task.id, "error": str(e)})

