from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"

class Task(BaseModel):
    id: str
    mission_id: str
    objective: str
    status: TaskStatus = TaskStatus.QUEUED
    dependencies: List[str] = Field(default_factory=list)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    expected_output: str = ""
    success_criteria: List[str] = Field(default_factory=list)
    allowed_capabilities: List[str] = Field(default_factory=list)
    result: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 2

class TaskGraph(BaseModel):
    mission_id: str
    tasks: Dict[str, Task] = Field(default_factory=dict)
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
        
    def get_ready_tasks(self) -> List[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status == TaskStatus.QUEUED or task.status == TaskStatus.READY:
                # Check if all dependencies are COMPLETED
                deps_met = all(self.tasks[dep_id].status == TaskStatus.COMPLETED for dep_id in task.dependencies)
                if deps_met:
                    task.status = TaskStatus.READY
                    ready.append(task)
        return ready

    def mark_completed(self, task_id: str, result: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.COMPLETED
            self.tasks[task_id].result = result

    def mark_failed(self, task_id: str, error: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.FAILED
            self.tasks[task_id].error = error
            
    def is_complete(self) -> bool:
        return all(t.status == TaskStatus.COMPLETED for t in self.tasks.values())
        
    def has_failures(self) -> bool:
        return any(t.status == TaskStatus.FAILED or t.status == TaskStatus.BLOCKED for t in self.tasks.values())
