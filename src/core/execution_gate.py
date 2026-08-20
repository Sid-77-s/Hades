from src.models.mission import Mission, MissionStatus

class ExecutionDeniedError(Exception):
    pass

class ExecutionGate:
    def can_execute(self, mission: Mission) -> bool:
        if mission.status != MissionStatus.AUTHORIZED_EXECUTION:
            return False
        return True
