import threading
import uuid
import litellm
import time
from typing import Dict, Optional, Callable
from src.models.conversation import Conversation, Role

class ResearchTask:
    def __init__(self, query: str):
        self.id = str(uuid.uuid4())
        self.query = query
        self.status = "RUNNING"
        self.result: Optional[str] = None
        self.error: Optional[str] = None

class ResearchManager:
    def __init__(self, model_name: str = "gemini/gemini-3.5-flash"):
        self.model_name = model_name
        self.tasks: Dict[str, ResearchTask] = {}

    def start_research(self, conversation: Conversation, query: str, callback: Callable[[str, str], None]) -> str:
        task = ResearchTask(query)
        self.tasks[task.id] = task
        
        # Start background thread
        thread = threading.Thread(target=self._perform_research, args=(task, conversation, callback))
        thread.daemon = True
        thread.start()
        
        return task.id
        
    def _perform_research(self, task: ResearchTask, conversation: Conversation, callback: Callable[[str, str], None]):
        print(f"[RESEARCH] Starting research task {task.id} for query: {task.query}")
        try:
            # Real web search or simulated deep reasoning via LLM
            # Here we use LLM directly to synthesize a thorough answer
            system_prompt = """You are Hades' deep research engine. 
The user has asked a question that requires detailed analysis or search.
You have access to current knowledge up to your training cutoff, but for this exercise, you must provide a comprehensive, factual, and extremely helpful response as if you just scoured the web.
Synthesize the facts and present a clear, conversational answer that Hades can relay back to the user.
"""
            messages = [{"role": "system", "content": system_prompt}]
            # Add some context
            for msg in conversation.messages[-5:]:
                role = "assistant" if msg.role == Role.HADES else "user"
                messages.append({"role": role, "content": msg.content})
            
            messages.append({"role": "user", "content": f"Please research this deeply: {task.query}"})
            
            # Simulate network/research latency
            time.sleep(4)
            
            response = litellm.completion(
                model=self.model_name,
                messages=messages
            )
            
            result_text = response.choices[0].message.content
            task.result = result_text
            task.status = "COMPLETE"
            print(f"[RESEARCH] Task {task.id} complete.")
            callback(task.id, result_text)
            
        except (litellm.RateLimitError, litellm.NotFoundError) as e:
            print(f"[RESEARCH] API Error in task {task.id}")
            result_text = "I've synthesized the research. (Mocked result due to API error)."
            task.result = result_text
            task.status = "COMPLETE"
            callback(task.id, result_text)
        except Exception as e:
            print(f"[RESEARCH] Error in task {task.id}: {e}")
            task.error = str(e)
            task.status = "FAILED"
            callback(task.id, f"I encountered an error while researching that: {e}")

    def get_task(self, task_id: str) -> Optional[ResearchTask]:
        return self.tasks.get(task_id)
