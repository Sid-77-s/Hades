from typing import Dict, Any
import os
import json
import litellm
from src.core.execution.task_graph import Task

class ReviewEngine:
    def __init__(self, model_name: str = "gemini/gemini-flash-latest"):
        self.model_name = model_name

    def review_task(self, task: Task, output: str) -> Dict[str, Any]:
        """
        Reviews a task's execution output to ensure it genuinely produced
        useful, non-empty, and valid results.
        """
        if not output or str(output).strip() in ["None", "", "{}"]:
            return {
                "passed": False,
                "feedback": "Task output was empty or invalid."
            }

        # Check for filesystem artifacts if mentioned in task
        if "file" in task.objective.lower() or "report" in task.objective.lower():
            # If output mentions a file path, verify it exists and is not empty
            words = str(output).split()
            for w in words:
                clean_w = w.strip('",\'()[]<>')
                if os.path.exists(clean_w) and os.path.isfile(clean_w):
                    if os.path.getsize(clean_w) > 0:
                        return {"passed": True, "feedback": f"Verified artifact exists ({clean_w}, {os.path.getsize(clean_w)} bytes)."}

        # Quick LLM verification for semantic completion
        prompt = f"""You are the Review Engine for Hades AI Operating System.
Task Objective: {task.objective}
Expected Output: {task.expected_output}
Actual Output Produced: {output[:1000]}

Did this task successfully and honestly produce the required output?
Return JSON with:
- passed: boolean
- feedback: string
"""
        try:
            res = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                timeout=15
            )
            data = json.loads(res.choices[0].message.content)
            return {
                "passed": bool(data.get("passed", True)),
                "feedback": data.get("feedback", "Review completed.")
            }
        except Exception as e:
            # If LLM review fails, fallback to basic non-empty heuristic
            is_valid = len(str(output).strip()) > 20 and "error" not in str(output).lower()[:50]
            return {
                "passed": is_valid,
                "feedback": "Output verified via heuristic review." if is_valid else "Output failed basic check."
            }
