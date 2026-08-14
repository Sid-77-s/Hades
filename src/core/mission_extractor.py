import json
import os
import litellm
from typing import List
from src.models.conversation import Conversation, Message
from src.models.mission import MissionUnderstanding

class MissionExtractor:
    def __init__(self, model_name: str = "gemini/gemini-3.5-flash"):
        self.model_name = model_name

    def extract(self, conversation: Conversation, current_understanding: MissionUnderstanding) -> MissionUnderstanding:
        system_prompt = """You are the Mission Extractor for the Hades AI Operating System.
Your job is to read the conversation between the USER and HADES, and update the Mission Understanding state.

Rules for updating the state:
1. For each field (objective, desired_outcome, success_criteria, context, constraints, priorities, preferences, important_decisions):
   - Set the `value` to the clearest summary of what is known.
   - Set `source` to "EXPLICIT" if the user directly stated it.
   - Set `source` to "INFERRED" if it is reasonably implied but not explicitly stated.
   - Set `source` to "UNKNOWN" if we don't have enough information to make a reasonable guess.
   - Do NOT turn an inferred guess into a fact. If the user hasn't explicitly confirmed it, it is INFERRED or UNKNOWN.
2. Identify any assumptions Hades is making and list them in `assumptions`.
3. Identify what remains unknown and list them in `open_questions`.
4. Identify any contradictions in the user's requests and list them in `contradictions`.
5. If Hades has summarized the mission and the user naturally confirmed it (e.g., "Exactly", "Yes", "That's right"), set `mutual_understanding_reached` to `true`. If the user corrects Hades, or if understanding is still being built, it remains `false`.

Only output the requested JSON format."""

        conversation_text = "\n".join([f"{msg.role.value.upper()}: {msg.content}" for msg in conversation.messages])
        
        user_prompt = f"""Current Mission Understanding:
{current_understanding.model_dump_json(indent=2)}

Recent Conversation:
{conversation_text}

Update the Mission Understanding based on the conversation so far."""

        response = litellm.completion(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=MissionUnderstanding,
        )
        
        try:
            # LiteLLM parses the Pydantic model directly when response_format is provided.
            if hasattr(response.choices[0].message, "content"):
                parsed_json = json.loads(response.choices[0].message.content)
                return MissionUnderstanding(**parsed_json)
        except Exception as e:
            # Fallback or pass through error
            print(f"Error parsing JSON from LLM: {e}")
            raise e
