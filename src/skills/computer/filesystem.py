import os
import shutil
import glob
from typing import Any, Dict
from src.skills.base import BaseSkill, SkillMetadata, SkillStatus

class FilesystemSkill(BaseSkill):
    def get_metadata(self) -> SkillMetadata:
        return SkillMetadata(
            skill_id="filesystem",
            name="Linux Filesystem Manager",
            description="Performs read, write, exists, list, find, mkdir, and delete operations on the local Linux filesystem.",
            category="computer",
            input_schema={
                "action": "read | write | list | exists | mkdir | find | delete | stat",
                "path": "Target file or directory path",
                "content": "Optional string content for write action",
                "pattern": "Optional glob pattern for find action"
            },
            output_schema={
                "result": "Content of file, list of directory, or status dictionary",
                "exists": "Boolean indicating existence",
                "size_bytes": "Integer file size if applicable",
                "path": "Target path processed"
            },
            risk_level="REVERSIBLE",
            supported_providers=["linux_fs"]
        )
        
    def verify_health(self) -> tuple[bool, str, str]:
        return True, "Linux filesystem accessible", SkillStatus.READY

    async def execute(self, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
        action = params.get("action", "read")
        path = params.get("path", "")
        content = params.get("content", "")
        pattern = params.get("pattern", "*")

        if not path and action != "find":
            raise ValueError("path is required for this action")
            
        try:
            if action == "exists":
                exists = os.path.exists(path)
                is_file = os.path.isfile(path) if exists else False
                is_dir = os.path.isdir(path) if exists else False
                size = os.path.getsize(path) if exists and is_file else 0
                return {
                    "exists": exists,
                    "is_file": is_file,
                    "is_dir": is_dir,
                    "size_bytes": size,
                    "path": path,
                    "result": f"{path} exists: {exists} (file={is_file}, dir={is_dir}, size={size}B)"
                }

            elif action == "read":
                if not os.path.exists(path):
                    return {"error": f"File not found: {path}", "exists": False, "path": path}
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    data = f.read()
                return {
                    "result": data,
                    "size_bytes": len(data),
                    "path": path,
                    "exists": True
                }

            elif action == "write":
                parent = os.path.dirname(os.path.abspath(path))
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                size = os.path.getsize(path)
                return {
                    "result": f"Successfully wrote {size} bytes to {path}",
                    "size_bytes": size,
                    "path": path,
                    "exists": True
                }

            elif action == "mkdir":
                os.makedirs(path, exist_ok=True)
                return {"result": f"Directory verified/created: {path}", "path": path, "exists": True}

            elif action == "list":
                if not os.path.exists(path):
                    return {"error": f"Directory not found: {path}", "exists": False}
                items = os.listdir(path)
                return {"result": items, "count": len(items), "path": path, "exists": True}

            elif action == "find":
                search_dir = path or os.getcwd()
                search_pattern = os.path.join(search_dir, pattern)
                matches = glob.glob(search_pattern, recursive=True)
                return {"result": matches, "count": len(matches), "pattern": search_pattern}

            elif action == "stat":
                if not os.path.exists(path):
                    return {"exists": False, "path": path}
                st = os.stat(path)
                return {
                    "exists": True,
                    "size_bytes": st.st_size,
                    "is_dir": os.path.isdir(path),
                    "is_file": os.path.isfile(path),
                    "mtime": st.st_mtime,
                    "path": path,
                    "result": f"Size: {st.st_size} bytes"
                }

            elif action == "delete":
                if os.path.isfile(path):
                    os.remove(path)
                    return {"result": f"Successfully deleted file {path}", "deleted": True}
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    return {"result": f"Successfully deleted directory {path}", "deleted": True}
                return {"result": f"Path did not exist: {path}", "deleted": False}

            else:
                raise ValueError(f"Unknown filesystem action: {action}")
        except Exception as e:
            return {"error": str(e), "path": path}

