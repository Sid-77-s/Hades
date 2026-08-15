import os
import shutil
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus

class FilesystemSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="filesystem",
            name="Filesystem Manager",
            description="Performs read/write/delete operations on the local filesystem.",
            category="computer",
            input_schema={
                "action": "read | write | list | delete",
                "path": "Target file or directory path",
                "content": "Optional content for write action"
            },
            output_schema={
                "result": "Content of file, list of directory, or status message"
            },
            risk_level="REVERSIBLE"
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        # Filesystem is always available on the local machine
        return True, "Ready", SkillStatus.READY

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        action = params.get("action")
        path = params.get("path")
        content = params.get("content", "")
        
        if not action or not path:
            raise ValueError("action and path are required")
            
        try:
            if action == "read":
                with open(path, "r", encoding="utf-8") as f:
                    return {"result": f.read()}
            elif action == "write":
                os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return {"result": f"Successfully wrote to {path}"}
            elif action == "list":
                items = os.listdir(path)
                return {"result": items}
            elif action == "delete":
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                return {"result": f"Successfully deleted {path}"}
            else:
                raise ValueError(f"Unknown action: {action}")
        except Exception as e:
            return {"error": str(e)}
