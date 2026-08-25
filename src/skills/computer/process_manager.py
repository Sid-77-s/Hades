import asyncio
import os
import shutil
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus

class ProcessManagerSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="process_manager",
            name="Linux Process & Resource Manager",
            description="Inspects active Linux processes, checks system resource consumption (CPU/Memory/Disk), and checks service statuses.",
            category="computer",
            input_schema={
                "action": "list | check | system_resources | inspect_port",
                "process_name": "Optional process name for check action",
                "port": "Optional port number for inspect_port action",
                "limit": "Max processes to list (default 15)"
            },
            output_schema={
                "result": "Structured process data or resource metrics",
                "is_running": "Boolean if process check",
                "metrics": "System metrics dictionary"
            },
            risk_level="READ",
            supported_providers=["linux_proc"]
        )

    def verify_health(self) -> tuple[bool, str, str]:
        return True, "Linux process subsystem accessible", SkillStatus.READY

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        action = params.get("action", "list")
        limit = params.get("limit", 15)

        try:
            if action == "list":
                cmd = f"ps aux --sort=-%mem | head -n {limit + 1}"
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode("utf-8", errors="replace") if stdout else ""
                lines = output.strip().split("\n")
                return {
                    "header": lines[0] if lines else "",
                    "processes": lines[1:] if len(lines) > 1 else [],
                    "count": max(0, len(lines) - 1),
                    "result": output
                }

            elif action == "check":
                target = params.get("process_name", "").strip()
                if not target:
                    raise ValueError("process_name is required for check action")
                
                cmd = f"pgrep -fl {target}"
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode("utf-8", errors="replace").strip()
                is_running = proc.returncode == 0 and len(output) > 0
                return {
                    "process_name": target,
                    "is_running": is_running,
                    "matches": output.split("\n") if output else [],
                    "result": f"Process '{target}' is {'RUNNING' if is_running else 'NOT RUNNING'}"
                }

            elif action == "inspect_port":
                port = params.get("port")
                if not port:
                    raise ValueError("port is required for inspect_port action")
                
                cmd = f"ss -tuln | grep :{port} || true"
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode("utf-8", errors="replace").strip()
                return {
                    "port": port,
                    "active": len(output) > 0,
                    "details": output,
                    "result": output if output else f"No active listeners on port {port}"
                }

            elif action == "system_resources":
                cmd = "uptime; echo '---'; free -h; echo '---'; df -h . ; uname -a"
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode("utf-8", errors="replace")
                return {
                    "result": output,
                    "environment": "Ubuntu Linux (WSL2)"
                }

            else:
                raise ValueError(f"Unknown process manager action: {action}")

        except Exception as e:
            return {"error": str(e)}
