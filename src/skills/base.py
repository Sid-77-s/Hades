from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import traceback

class SkillStatus(str):
    READY = "READY"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    UNAVAILABLE = "UNAVAILABLE"
    REQUIRES_CONFIGURATION = "REQUIRES_CONFIGURATION"
    CONFIGURATION_REQUIRED = "CONFIGURATION_REQUIRED"
    REQUIRES_PAID_SERVICE = "REQUIRES_PAID_SERVICE"

class SkillMetadata(BaseModel):
    skill_id: str
    name: str
    description: str
    category: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    required_credentials: List[str] = Field(default_factory=list)
    risk_level: str = "READ" # READ, REVERSIBLE, SIGNIFICANT, HIGH_IMPACT
    supported_providers: List[str] = Field(default_factory=list)
    estimated_cost: str = "Free"
    health_status: str = SkillStatus.UNAVAILABLE
    fallback_skills: List[str] = Field(default_factory=list)

class BaseSkill:
    def __init__(self):
        self._metadata = self.get_metadata()
        self._check_health()
        
    def get_metadata(self) -> SkillMetadata:
        """Define and return the skill's metadata."""
        raise NotImplementedError
        
    def _check_health(self):
        """Internal routine to set health based on credentials or dependencies."""
        try:
            is_healthy, reason, status = self.verify_health()
            self._metadata.health_status = status if status else (SkillStatus.READY if is_healthy else SkillStatus.FAILED)
        except Exception as e:
            self._metadata.health_status = SkillStatus.FAILED
            print(f"[Skill:{self._metadata.skill_id}] Health check failed: {e}")

    def verify_health(self) -> tuple[bool, str, Optional[str]]:
        """
        Verify if the skill has everything it needs to execute.
        Returns (is_healthy: bool, reason: str, status_code: str)
        """
        return True, "Ready", SkillStatus.READY

    @property
    def metadata(self) -> SkillMetadata:
        return self._metadata

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """The main execution method for the skill."""
        raise NotImplementedError
