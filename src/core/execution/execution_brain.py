from typing import List, Dict, Any, Optional
import os
import asyncio
import uuid
from src.models.mission import Mission, MissionStatus
from src.core.execution.task_graph import TaskGraph, Task, TaskStatus
from src.core.execution.review_engine import ReviewEngine
from src.core.execution.uncertainty_engine import UncertaintyEngine
from src.core.event_bus import EventBus
from src.skills.registry import registry as skill_registry
from src.core.worker_manager import worker_manager

class ExecutionBrain:
    def __init__(self):
        self.review_engine = ReviewEngine()
        self.uncertainty_engine = UncertaintyEngine()
        self.event_bus = EventBus()
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
            
            raw_results = ""
            for t in task_graph.tasks.values():
                if t.actual_output:
                    raw_results += f"\n{t.actual_output}"
                    
            try:
                import litellm
                model = worker_manager.select_worker("fast") or "gemini/gemini-flash-latest"
                prompt = f"""You are Hades returning to the user after completing background work.
The user's objective was: {mission.understanding.objective.value}
The raw result from the system is: {raw_results[:1500]}

Generate a short, natural, conversational message telling the user you are back and what you found.
DO NOT say "Task completed."
DO NOT paste the entire raw text. Just give the conversational summary and highlight what matters.
Keep it under 4 sentences.
Example: "Hey, I'm back. I finished the research. I found six strong competitors, but two are much closer to what we're building than I expected. I've pulled everything together for you."
"""
                res = litellm.completion(model=model, messages=[{"role": "system", "content": prompt}], max_tokens=150)
                final_msg = res.choices[0].message.content
                final_msg += f"\n\n---\n{raw_results}"
            except Exception as e:
                print(f"[ExecutionBrain] Failed to generate conversational return: {e}")
                final_msg = f"Hey, I'm back. I finished the work.\n\n{raw_results}"

            self.event_bus.publish_sync("MISSION_COMPLETED", {
                "mission_id": mission.id, 
                "result": final_msg
            })
        else:
            mission.status = MissionStatus.NEEDS_USER
            self.event_bus.publish_sync("MISSION_BLOCKED", {
                "mission_id": mission.id, 
                "error": "I hit a blocker on the background work. Let's discuss how you want to proceed."
            })
            
    def _generate_plan(self, mission: Mission) -> TaskGraph:
        graph = TaskGraph(mission_id=mission.id)
        obj = (mission.understanding.objective.value or "Execute request").lower()
        
        if "presentation" in obj or "deck" in obj or "slides" in obj:
            t1 = Task(
                id=f"task_{uuid.uuid4().hex[:8]}",
                mission_id=mission.id,
                objective=mission.understanding.objective.value or "Create a draft presentation structure and content",
                expected_output="A presentation file (.pptx) or generated link",
                allowed_capabilities=["creation", "presentations"],
                success_criteria=["Must have coherent slide content"]
            )
            graph.add_task(t1)
        elif "research" in obj or "report" in obj or "market" in obj or "analyze" in obj or "summary" in obj:
            t1 = Task(
                id=f"task_{uuid.uuid4().hex[:8]}",
                mission_id=mission.id,
                objective=f"Research and write comprehensive intelligence report: {mission.understanding.objective.value}",
                expected_output="A structured markdown report file saved to output/research_report.md",
                allowed_capabilities=["research", "computer", "general"],
                success_criteria=["Report must contain key findings and analysis"]
            )
            graph.add_task(t1)
        else:
            t1 = Task(
                id=f"task_{uuid.uuid4().hex[:8]}",
                mission_id=mission.id,
                objective=mission.understanding.objective.value or "Execute user request",
                allowed_capabilities=["computer", "general", "research"],
                success_criteria=["Complete the objective"]
            )
            graph.add_task(t1)
            
        return graph

    async def _execute_task(self, mission: Mission, task: Task, graph: TaskGraph):
        task.status = TaskStatus.RUNNING
        self.event_bus.publish_sync("TASK_STARTED", {"task_id": task.id, "objective": task.objective})
        
        # 1. Match Skill
        skill = None
        for category in task.allowed_capabilities:
            skills = self.registry.get_skills_by_category(category.lower())
            healthy_skills = [s for s in skills if s.metadata.health_status in ["READY", "PARTIAL"]]
            if healthy_skills:
                skill = healthy_skills[0]
                break

        # Fallback to research/filesystem execution if specific skill not matched
        if not skill:
            # Direct LLM + Filesystem research creation
            try:
                model = worker_manager.select_worker("research") or "gemini/gemini-flash-latest"
                import litellm
                res = litellm.completion(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are the Hades Autonomous Research Engine. Produce a thorough, executive-ready markdown report with clear headings, analysis, and takeaways."},
                        {"role": "user", "content": f"Produce the report for: {task.objective}"}
                    ]
                )
                report_content = res.choices[0].message.content
                out_path = os.path.join("output", "research_report.md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(report_content)
                
                result = f"Report generated successfully and saved to `{out_path}`.\n\nSummary:\n{report_content[:400]}..."
                graph.mark_completed(task.id, result)
                self.event_bus.publish_sync("TASK_COMPLETED", {"task_id": task.id, "result": result})
                return
            except Exception as e:
                graph.mark_failed(task.id, str(e))
                self.event_bus.publish_sync("TASK_FAILED", {"task_id": task.id, "error": str(e)})
                return

        friendly_name = skill.metadata.name
        self.event_bus.publish_sync("CAPABILITY_SELECTED", {"task_id": task.id, "adapter": friendly_name})
        
        try:
            result = await skill.execute(
                params={
                    "command": task.objective,
                    "query": task.objective,
                    "topic": task.objective,
                    "action": "write",
                    "path": os.path.join("output", "mission_output.md"),
                    "content": f"# Mission Artifact\n\nObjective: {task.objective}"
                }, 
                context=mission.understanding.model_dump()
            )
            
            review = self.review_engine.review_task(task, str(result))
            
            if review.get("passed", False):
                graph.mark_completed(task.id, str(result))
                self.event_bus.publish_sync("TASK_COMPLETED", {"task_id": task.id, "result": "Verified output."})
            else:
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.RETRYING
                    self.event_bus.publish_sync("TASK_RETRYING", {"task_id": task.id, "feedback": review.get("feedback")})
                else:
                    graph.mark_failed(task.id, review.get("feedback", "Review verification failed."))
                    self.event_bus.publish_sync("TASK_FAILED", {"task_id": task.id, "error": review.get("feedback")})
                    
        except Exception as e:
            graph.mark_failed(task.id, str(e))
            self.event_bus.publish_sync("TASK_FAILED", {"task_id": task.id, "error": str(e)})
