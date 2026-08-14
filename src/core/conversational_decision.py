import json
import litellm
from typing import Optional
from src.models.conversation import Conversation
from src.models.mission import MissionUnderstanding, ConversationalDecision

class ConversationalDecisionSystem:
    def __init__(self, model_name: str = "gemini/gemini-3.5-flash"):
        self.model_name = model_name
        
    def decide(self, conversation: Conversation, understanding: MissionUnderstanding, is_ready_for_lock: bool) -> ConversationalDecision:
        system_prompt = f"""You are the Conversational Decision Engine for Hades.
Your job is to decide the next conversational action and generate the response.

There are 5 possible actions:
1. ASK: Use when the user likely knows missing CRITICAL information but hasn't provided it. Do not ask about non-critical details.
2. PROPOSE: Use when Hades has useful domain knowledge and can present reasonable approaches. (e.g. "We could do A, B, or C. Which do you prefer?")
3. EXPLORE: Use when neither the user nor Hades has a defined direction (e.g. user says "I don't know what to build").
4. CHALLENGE: Use when the user's assumption is weak, contradictory, or likely to produce a bad outcome. Respectfully push back and explain trade-offs.
5. ACKNOWLEDGE: Use when summarizing understanding to check alignment, or when the mission is fully understood and ready to lock.

If `is_ready_for_lock` is TRUE, the user has aligned with the summary and the mission is completely understood. In this case, simply ACKNOWLEDGE and confirm you are ready to work.

If `is_ready_for_lock` is FALSE but you have a good summary of the critical requirements, you should ACKNOWLEDGE by summarizing your understanding and asking if the user agrees. (e.g., "I think I have what I need. You want X and Y. I will work on that. Does that sound right?")

Otherwise, determine whether you need to ASK, PROPOSE, EXPLORE, or CHALLENGE based on what is currently UNKNOWN or contradictory in the Mission Understanding.

Keep your response conversational, concise, and professional.

Only output the requested JSON format."""

        conversation_text = "\n".join([f"{msg.role.value.upper()}: {msg.content}" for msg in conversation.messages])
        
        user_prompt = f"""Current Mission Understanding:
{understanding.model_dump_json(indent=2)}

Is Ready For Lock? {is_ready_for_lock}

Recent Conversation:
{conversation_text}

Provide your decision and the response text."""

        response = litellm.completion(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=ConversationalDecision,
        )
        
        try:
            if hasattr(response.choices[0].message, "content"):
                parsed_json = json.loads(response.choices[0].message.content)
                return ConversationalDecision(**parsed_json)
        except Exception as e:
            print(f"Error parsing JSON from LLM: {e}")
            raise e
