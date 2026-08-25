import asyncio
import os
import shlex
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus

BLOCKED_PATTERNS = [
    "rm -rf /",
    "rm -rf /*",
    "mkfs",
    ":(){ :|:& };:",
    "> /dev/sda",
    "> /dev/nvme"
]

class TerminalSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="terminal",
            name="Linux Terminal Execution",
            description="Executes shell commands within the Linux environment and workspace.",
            category="computer",
            input_schema={
                "command": "The shell command to execute",
                "cwd": "Optional working directory path (defaults to current workspace)",
                "timeout": "Timeout in seconds (default 30)"
            },
            output_schema={
                "stdout": "Standard output string",
                "stderr": "Standard error string",
                "exit_code": "Process exit code (0 for success)",
                "command": "Command that was executed"
            },
            risk_level="HIGH_IMPACT",
            supported_providers=["linux_bash"]
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        return True, "Linux bash operational", SkillStatus.READY

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        command = params.get("command", "").strip()
        if not command:
            raise ValueError("command is required")

        # Safety validation
        for pattern in BLOCKED_PATTERNS:
            if pattern in command:
                return {
                    "stdout": "",
                    "stderr": f"Execution blocked: Command matches prohibited dangerous pattern '{pattern}'",
                    "exit_code": 126,
                    "command": command
                }

        cwd = params.get("cwd") or os.getcwd()
        timeout = params.get("timeout", 30)

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except Exception:
                    pass
                return {
                    "stdout": "",
                    "stderr": f"Command timed out after {timeout} seconds.",
                    "exit_code": 124,
                    "command": command
                }
            
            stdout_str = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
            stderr_str = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
            
            return {
                "stdout": stdout_str,
                "stderr": stderr_str,
                "exit_code": process.returncode,
                "command": command,
                "cwd": cwd
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1,
                "command": command
            }

