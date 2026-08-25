import os
import json
from typing import Dict, Any, Union
from src.core.execution.task_graph import Task
from src.core.worker_manager import worker_manager

class ReviewEngine:
    def __init__(self, model_name: str = "gemini/gemini-flash-latest"):
        self.model_name = model_name

    def review_task(self, task: Task, output: Any) -> Dict[str, Any]:
        """
        Reviews a task's execution output to ensure it genuinely produced
        useful, non-empty, and valid Linux results.
        """
        if output is None:
            return {
                "passed": False,
                "feedback": "Task output was None."
            }

        # 1. Inspect Terminal Execution Exit Codes
        if isinstance(output, dict):
            if "exit_code" in output:
                code = output.get("exit_code")
                if code != 0:
                    err_msg = output.get("stderr") or f"Process exited with non-zero status code {code}"
                    return {
                        "passed": False,
                        "feedback": f"Linux command failed (Exit Code {code}): {err_msg}"
                    }

            if "error" in output and output.get("error"):
                return {
                    "passed": False,
                    "feedback": f"Execution error encountered: {output.get('error')}"
                }

        output_str = str(output)
        if not output_str.strip() or output_str.strip() in ["{}", "[]", "None"]:
            return {
                "passed": False,
                "feedback": "Task output was empty."
            }

        # 2. Check for File/Directory Artifacts on Disk
        for criterion in task.success_criteria:
            if "file:" in criterion.lower() or "path:" in criterion.lower():
                parts = criterion.split(":", 1)
                target_path = parts[1].strip()
                if not os.path.exists(target_path):
                    return {
                        "passed": False,
                        "feedback": f"Verification failed: Required file artifact '{target_path}' does not exist on disk."
                    }
                if os.path.isfile(target_path) and os.path.getsize(target_path) == 0:
                    return {
                        "passed": False,
                        "feedback": f"Verification failed: File '{target_path}' exists but is 0 bytes (empty)."
                    }

        # Check any explicitly mentioned file paths in output dictionary
        if isinstance(output, dict) and output.get("path"):
            p = output["path"]
            if output.get("action") in ["write", "mkdir", "stat"] or "file" in task.objective.lower():
                if not os.path.exists(p):
                    return {
                        "passed": False,
                        "feedback": f"Verified artifact does not exist at {p}."
                    }

        # 3. Semantic Review via Worker Models (with fallback)
        prompt = f"""You are the Review Engine for Hades Linux AI OS.
Task Objective: {task.objective}
Success Criteria: {json.dumps(task.success_criteria)}
Expected Output: {task.expected_output}
Actual Output Produced: {output_str[:1200]}

Did this task honestly and successfully accomplish the objective according to the criteria?
Return JSON with keys:
- passed: boolean
- feedback: string explaining why it passed or failed (max 2 sentences)
"""
        try:
            res = worker_manager.complete(
                messages=[{"role": "user", "content": prompt}],
                capability="fast",
                response_format={"type": "json_object"},
                timeout=15
            )
            data = json.loads(res.choices[0].message.content)
            return {
                "passed": bool(data.get("passed", True)),
                "feedback": data.get("feedback", "Output verified.")
            }
        except Exception as e:
            # Fallback heuristic: Check for standard error signs
            has_error = "traceback" in output_str.lower() or "command not found" in output_str.lower()
            is_valid = not has_error and len(output_str.strip()) > 5
            return {
                "passed": is_valid,
                "feedback": "Verified via Linux heuristic." if is_valid else f"Execution check failed: {output_str[:100]}"
            }

