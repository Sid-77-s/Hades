from src.models.mission import Mission
from src.core.execution.task_graph import Task
from src.core.event_bus import EventBus

class UncertaintyEngine:
    def __init__(self):
        self.event_bus = EventBus()

    def handle_uncertainty(self, mission: Mission, issue_type: str, details: str):
        """
        Called when the ExecutionBrain encounters a high-impact decision or unrecoverable error
        that requires human judgment.
        """
        print(f"[UncertaintyEngine] Raising {issue_type}: {details}")
        
        # Publish an event that the UI should show as a "MEANINGFUL_DECISION" or "BLOCKER"
        payload = {
            "mission_id": mission.id,
            "issue_type": issue_type,
            "details": details,
            "requires_user_action": True
        }
        
        self.event_bus.publish_sync("USER_INTERVENTION_REQUIRED", payload)
        
        # In a fully asynchronous system, we'd pause the mission.
        # For now, we rely on the event bus to notify the user.
