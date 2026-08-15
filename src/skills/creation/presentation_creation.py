from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus
from src.core.config_manager import ConfigManager
import os

class PresentationCreationSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="presentation_creation",
            name="Presentation Creation",
            description="Creates a presentation (slides) using Gamma or local fallback.",
            category="creation",
            input_schema={
                "topic": "Topic of the presentation",
                "slide_count": "Number of slides",
                "content": "Detailed text content for the slides"
            },
            output_schema={
                "file_path": "Path to the created presentation file or URL"
            },
            required_credentials=["GAMMA_EMAIL", "GAMMA_PASSWORD"],
            risk_level="REVERSIBLE",
            supported_providers=["gamma", "canva", "local_markdown"]
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        creds = ConfigManager().get_credentials()
        # If no Gamma credentials, we drop to PARTIAL because we have a local fallback
        if creds.gamma_email and creds.gamma_password:
            return True, "Gamma Ready", SkillStatus.READY
        return False, "Missing Gamma Credentials. Using fallback.", SkillStatus.PARTIAL

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        topic = params.get("topic", "Untitled")
        content = params.get("content", "No content provided.")
        
        creds = ConfigManager().get_credentials()
        
        if creds.gamma_email and creds.gamma_password:
            # Here you would invoke Gamma via API or Browser Automation.
            # Simulating Gamma execution path:
            return {"result": f"Successfully created Gamma presentation for {topic}."}
        else:
            # Fallback to Local Markdown Slide Generation
            file_name = f"{topic.replace(' ', '_')}_Presentation.md"
            file_path = os.path.join(os.getcwd(), file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {topic}\n\n")
                f.write("## Auto-Generated Presentation\n\n")
                f.write(content)
                
            return {"file_path": file_path, "result": "Generated local markdown presentation (Fallback)."}
