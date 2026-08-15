import asyncio
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus

class TerminalSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="terminal",
            name="Terminal Execution",
            description="Executes shell commands.",
            category="computer",
            input_schema={
                "command": "The shell command to execute"
            },
            output_schema={
                "stdout": "Standard output",
                "stderr": "Standard error",
                "exit_code": "Exit code of the process"
            },
            risk_level="HIGH_IMPACT"
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        # Terminal is available locally
        return True, "Ready", SkillStatus.READY

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        command = params.get("command")
        if not command:
            raise ValueError("command is required")
            
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else "",
            "exit_code": process.returncode
        }
