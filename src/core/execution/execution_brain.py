from typing import List, Dict, Any
import asyncio
from src.models.mission import Mission, MissionStatus
from src.core.execution.task_graph import TaskGraph, Task, TaskStatus
from src.core.execution.review_engine import ReviewEngine
from src.core.execution.uncertainty_engine import UncertaintyEngine
from src.core.event_bus import EventBus
import uuid

class ExecutionBrain:
    def __init__(self, capability_registry=None):
        self.review_engine = ReviewEngine()
        self.uncertainty_engine = UncertaintyEngine()
        self.event_bus = EventBus()
        self.registry = capability_registry
        
    async def process_mission(self, mission: Mission):
        """
        Main orchestration loop for a LOCKED mission.
        """
        if mission.status != MissionStatus.LOCKED:
            print("[ExecutionBrain] Mission not locked.")
            return

        mission.status = MissionStatus.PLANNING
        self.event_bus.publish_sync("MISSION_STATUS_UPDATED", {"mission_id": mission.id, "status": mission.status.value})
        
        # 1. Plan Generation
        task_graph = self._generate_plan(mission)
        self.event_bus.publish_sync("PLAN_CREATED", {"mission_id": mission.id, "tasks": len(task_graph.tasks)})
        
        mission.status = MissionStatus.EXECUTING
        self.event_bus.publish_sync("MISSION_STATUS_UPDATED", {"mission_id": mission.id, "status": mission.status.value})
        
        # 2. Execution Loop
        while not task_graph.is_complete() and not task_graph.has_failures():
            ready_tasks = task_graph.get_ready_tasks()
            
            if not ready_tasks:
                if not task_graph.is_complete():
                    # Deadlock
                    task_graph.mark_failed("ALL", "Task deadlock - no ready tasks.")
                break
                
            # Execute tasks (sequentially for now, can be parallel via asyncio.gather)
            for task in ready_tasks:
                await self._execute_task(mission, task, task_graph)
                
        # 3. Handle Completion or Failure
        if task_graph.is_complete():
            mission.status = MissionStatus.DELIVERED
            self.event_bus.publish_sync("MISSION_COMPLETED", {"mission_id": mission.id, "result": "All tasks completed successfully."})
        else:
            mission.status = MissionStatus.BLOCKED
            self.event_bus.publish_sync("MISSION_BLOCKED", {"mission_id": mission.id, "error": "Mission execution failed."})
            
    def _generate_plan(self, mission: Mission) -> TaskGraph:
        """
        Generates a TaskGraph based on the mission understanding.
        For the hackathon, we use a simple heuristic/hardcoded logic based on keywords, 
        or an LLM call. Here we simulate the LLM call with a hardcoded presentation plan.
        """
        graph = TaskGraph(mission_id=mission.id)
        
        # Simple heuristic: if objective mentions presentation, use presentation pipeline.
        obj = mission.understanding.objective.value.lower() if mission.understanding.objective.value else ""
        if "presentation" in obj or "deck" in obj:
            t1 = Task(
                id=f"task_{uuid.uuid4().hex[:8]}",
                mission_id=mission.id,
                objective="Create a draft presentation structure and content",
                expected_output="A presentation file or generated link",
                allowed_capabilities=["PRESENTATIONS"],
                success_criteria=["Must have a coherent story", "Must match audience needs"]
            )
            graph.add_task(t1)
        else:
            # Generic task
            t1 = Task(
                id=f"task_{uuid.uuid4().hex[:8]}",
                mission_id=mission.id,
                objective=mission.understanding.objective.value or "Execute request",
                allowed_capabilities=["RESEARCH", "CODING"],
                success_criteria=["Complete the objective"]
            )
            graph.add_task(t1)
            
        return graph

    async def _execute_task(self, mission: Mission, task: Task, graph: TaskGraph):
        task.status = TaskStatus.RUNNING
        self.event_bus.publish_sync("TASK_STARTED", {"task_id": task.id, "objective": task.objective})
        
        adapter = None
        if self.registry:
            adapter = self.registry.get_best_adapter(task.allowed_capabilities)
            
        if not adapter:
            graph.mark_failed(task.id, "No suitable capability found.")
            self.uncertainty_engine.handle_uncertainty(mission, "MISSING_CAPABILITY", "I lack the capability to perform this task.")
            return

        # Clean up adapter name for user UI
        friendly_name = adapter.__class__.__name__.replace("Adapter", "").replace("Playwright", " Automation")
        self.event_bus.publish_sync("CAPABILITY_SELECTED", {"task_id": task.id, "adapter": friendly_name})
        
        try:
            # 1. Execute
            result = await adapter.execute(task.objective, mission.understanding.dict())
            
            # 2. Review
            review = self.review_engine.review_task(task, str(result))
            
            if review.get("passed", False):
                graph.mark_completed(task.id, str(result))
                self.event_bus.publish_sync("TASK_COMPLETED", {"task_id": task.id, "result": "Task passed review."})
            else:
                # 3. Recover
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.RETRYING
                    self.event_bus.publish_sync("TASK_RETRYING", {"task_id": task.id, "feedback": review.get("feedback")})
                    # We would loop back via getting ready tasks again, but we modify logic here:
                    # Actually, simple graph marks it retrying, and it will be picked up next loop.
                else:
                    graph.mark_failed(task.id, review.get("feedback", "Review failed repeatedly."))
                    
        except Exception as e:
            graph.mark_failed(task.id, str(e))
            self.event_bus.publish_sync("TASK_FAILED", {"task_id": task.id, "error": str(e)})
