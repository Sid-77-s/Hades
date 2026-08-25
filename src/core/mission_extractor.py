from typing import Dict, Any, List
import json
import litellm
from src.models.conversation import Conversation, Role
from src.models.mission import MissionUnderstanding, FieldState

class MissionExtractor:
    def __init__(self, model_name: str = "gemini/gemini-flash-latest"):
        self.model_name = model_name

    def extract(self, conversation: Conversation, current_understanding: MissionUnderstanding) -> MissionUnderstanding:
        system_prompt = """You are the Mission Extractor for Hades, an AI Operating System.
Your job is to read the conversation and extract the core mission details into structured fields:
- objective: Concise statement of the primary goal (or empty if unclear).
- desired_outcome: What the final deliverable should be.
- success_criteria: What defines success.
- context: Domain background, user preferences.
- constraints: Limitations, timelines, or restrictions.
- mutual_understanding_reached: Set to true ONLY if the objective and desired outcome are clear enough to begin execution without further clarification from the user.

Return ONLY valid JSON matching the exact structure of the provided current understanding state.
Each field MUST be a nested object with 'value' (string), 'source' (string enum), and 'criticality' (string enum).
"""
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation.messages[-6:]:
            role = "assistant" if msg.role == Role.HADES else msg.role.value
            messages.append({"role": role, "content": msg.content})

        messages.append({
            "role": "user",
            "content": f"Current understanding state: {current_understanding.model_dump_json()}\n\nUpdate the understanding from the conversation."
        })

        try:
            from src.core.worker_manager import worker_manager
            response = worker_manager.complete(
                messages=messages,
                capability="conversational",
                response_format={"type": "json_object"},
                timeout=25
            )
            data = json.loads(response.choices[0].message.content)
            return MissionUnderstanding(**data)
        except Exception as e:
            print(f"[MissionExtractor] Extraction error: {e}")
            if not current_understanding.objective.value:
                last_msg = conversation.messages[-1].content if conversation.messages else "User task"
                current_understanding.objective.value = last_msg
            return current_understanding
