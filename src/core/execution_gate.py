from src.models.mission import Mission, MissionStatus

class ExecutionDeniedError(Exception):
    pass

class ExecutionGate:
    @staticmethod
    def enforce_mission_lock(mission: Mission):
        if mission.status != MissionStatus.LOCKED:
            raise ExecutionDeniedError(
                f"Execution denied: Mission status must be LOCKED. Current status is {mission.status}"
            )
