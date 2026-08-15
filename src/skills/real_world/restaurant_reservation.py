from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus

class RestaurantReservationSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="restaurant_reservation",
            name="Restaurant Reservation",
            description="Searches for restaurants and books a table.",
            category="real_world",
            input_schema={
                "location": "City or neighborhood",
                "cuisine": "Type of food",
                "party_size": "Number of people",
                "date_time": "Time of reservation"
            },
            output_schema={
                "status": "Success or failure",
                "confirmation_code": "Reservation confirmation code"
            },
            required_credentials=["OPENTABLE_API_KEY"],
            risk_level="HIGH_IMPACT"
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        # Since this is a demo environment and we lack actual OpenTable APIs, we return configuration required.
        return False, "Missing OPENTABLE_API_KEY", SkillStatus.CONFIGURATION_REQUIRED

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        raise NotImplementedError("Skill requires configuration.")
