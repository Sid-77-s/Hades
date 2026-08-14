import litellm
import json
from src.core.execution.task_graph import Task

class ReviewEngine:
    def __init__(self, model_name: str = "gemini/gemini-3.5-flash"):
        self.model_name = model_name

    def review_task(self, task: Task, output_context: str) -> dict:
        """
        Uses the LLM to verify if the task outputs meet the success criteria.
        Returns a dict: {"passed": bool, "feedback": str}
        """
        system_prompt = """You are the Hades Review Engine.
Your job is to review execution output against strict success criteria.
Evaluate the provided output. Does it satisfy the objective and criteria?
Return a JSON object: {"passed": boolean, "feedback": "string explaining why passed or what failed"}
"""
        user_prompt = f"""
Task Objective: {task.objective}
Success Criteria: {task.success_criteria}
Output Received/Observed: {output_context}

Evaluate now.
"""
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            return {"passed": False, "feedback": f"Review Engine failure: {e}"}
