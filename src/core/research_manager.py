import threading
import uuid
import litellm
import time
from typing import Dict, Optional, Callable
from src.models.conversation import Conversation, Role
from src.core.worker_manager import worker_manager

class ResearchTask:
    def __init__(self, query: str):
        self.id = str(uuid.uuid4())
        self.query = query
        self.status = "RUNNING"
        self.result: Optional[str] = None
        self.error: Optional[str] = None

class ResearchManager:
    def __init__(self):
        # We'll resolve model dynamically at execution time
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
        
        import asyncio
        from src.skills.registry import registry
        
        try:
            # 1. Fetch web_search skill
            registry.discover_skills()
            skill = registry.get_skill("web_search")
            
            if not skill:
                raise Exception("Research capability is completely disabled.")
                
            is_healthy, msg, status = skill.verify_health()
            if not is_healthy:
                raise Exception(f"Research capability not configured: {msg}")
                
            # 2. Execute real web search
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            search_result = loop.run_until_complete(
                skill.execute({"query": task.query}, {})
            )
            loop.close()
            
            results_list = search_result.get("results", [])
            if not results_list:
                result_text = "I ran a search but couldn't find any relevant real-time information on that."
            else:
                # 3. Synthesize the raw results using an LLM to be partner-like
                system_prompt = """You are Hades. Your job is to synthesize these search results into a highly specific research report.
You must NOT output a generic dump of facts. You must structure your exact response using these specific markdown headers:

## What I found
(Short synthesis of the strongest findings)

## Existing approaches
(Concise comparison of the most relevant systems. For each, list what it does, where it is strong, where it falls short)

## The actual gap
(Explain the common problem that existing systems don't adequately solve)

## Where Hades is different
(Explain Hades' differentiation. Focus on: persistent intelligence, conversation before execution, Mission Lock, equal partnership, Hades manages Workers/Tools, model-agnostic execution, review before delivery, persistent memory, user does not orchestrate AI)

## My conclusion
(Give a direct conclusion. If assumptions are weak, challenge them. Don't just tell the user what they want to hear.)

Do NOT invent facts. Do NOT fabricate companies or products. State uncertainty where information cannot be verified."""

                raw_snippets = ""
                for idx, r in enumerate(results_list[:5]):
                    raw_snippets += f"\n[Source {idx+1}: {r.get('url')}]\nTitle: {r.get('title')}\nSnippet: {r.get('snippet')}\n"

                messages = [{"role": "system", "content": system_prompt}]
                for msg in conversation.messages[-4:]:
                    role = "assistant" if msg.role == Role.HADES else "user"
                    messages.append({"role": role, "content": msg.content})
                
                messages.append({"role": "user", "content": f"Query: {task.query}\nSearch Results:\n{raw_snippets}\n\nPlease synthesize a response based ONLY on these sources."})
                
                response = worker_manager.complete(
                    messages=messages,
                    capability="research",
                    timeout=20
                )
                
                result_text = response.choices[0].message.content
                # Append sources
                sources_str = "\n\n**Sources:**\n" + "\n".join([f"- {r.get('url')}" for r in results_list[:3]])
                result_text += sources_str
                
            task.result = result_text
            task.status = "COMPLETE"
            print(f"[RESEARCH] Task {task.id} complete.")
            callback(task.id, result_text)
            
        except Exception as e:
            print(f"[RESEARCH] Error in task {task.id}: {e}")
            task.error = str(e)
            task.status = "FAILED"
            callback(task.id, f"I cannot verify current information right now. (Research subsystem offline: {e})")

    def get_task(self, task_id: str) -> Optional[ResearchTask]:
        return self.tasks.get(task_id)
