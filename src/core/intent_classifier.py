import json
import litellm
from pydantic import BaseModel
from src.models.conversation import Conversation, ConversationIntent

class IntentClassification(BaseModel):
    intent: ConversationIntent
    reasoning: str

class IntentClassifier:
    def __init__(self, model_name: str = "gemini/gemini-3.5-flash"):
        self.model_name = model_name

    def classify(self, conversation: Conversation, user_message: str) -> IntentClassification:
        system_prompt = """You are the Intent Classification Engine for Hades.
Your job is to determine the intent of the user's latest message given the conversation context.

Classify the intent into one of the following:
1. CASUAL_CONVERSATION: Greetings, small talk, casual chatting (e.g., "Good morning", "How are you?").
2. QUICK_INFORMATION: Direct, simple factual queries that can be answered immediately or with a quick tool lookup (e.g., "What time is it?", "Calculate 25% of 400", "What's the weather?").
3. KNOWLEDGE_QUESTION: General knowledge questions that the LLM can answer directly (e.g., "Who is the CEO of X?").
4. FOLLOW_UP: A continuation of the current context that doesn't change the primary intent but asks for more details (e.g., "And how much time do we have left?", "What about the other one?").
5. GOAL_EXPLORATION: The user is discussing a potential goal, idea, or project without fully committing yet (e.g., "I want to build a website for my startup").
6. MISSION_CANDIDATE: The user explicitly states a goal that requires planning, sustained work, and multiple steps (e.g., "Let's build the backend using PostgreSQL").
7. RESEARCH_REQUIRED: The user asks for external information that requires deep research, comparison, or checking external sources (e.g., "Can you compare PostgreSQL and MongoDB for our architecture?").
8. EXECUTION_REQUEST: The user commands execution of an already discussed plan (e.g., "Do it.", "Start the build.").

Only output the requested JSON format."""

        conversation_text = "\n".join([f"{msg.role.value.upper()}: {msg.content}" for msg in conversation.messages[-10:]])
        
        user_prompt = f"""Recent Conversation:
{conversation_text}

Latest User Message: {user_message}

Classify the intent."""

        response = litellm.completion(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=IntentClassification,
        )
        
        try:
            if hasattr(response.choices[0].message, "content"):
                parsed_json = json.loads(response.choices[0].message.content)
                return IntentClassification(**parsed_json)
        except Exception as e:
            print(f"Error parsing JSON from LLM: {e}")
            # Fallback to general conversational
            return IntentClassification(intent=ConversationIntent.CASUAL_CONVERSATION, reasoning="Fallback")
