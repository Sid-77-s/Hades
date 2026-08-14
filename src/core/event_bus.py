import asyncio
import json
from typing import Dict, Any, Callable, List

class EventBus:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance.queues: List[asyncio.Queue] = []
        return cls._instance
        
    async def subscribe(self) -> asyncio.Queue:
        q = asyncio.Queue()
        self.queues.append(q)
        return q
        
    def unsubscribe(self, q: asyncio.Queue):
        if q in self.queues:
            self.queues.remove(q)
            
    async def publish(self, event_type: str, payload: Dict[str, Any]):
        """Publish an event to all connected SSE clients."""
        event = {
            "type": event_type,
            "data": payload
        }
        event_str = json.dumps(event)
        
        # We must push to queues
        for q in self.queues:
            await q.put(event_str)
            
    def publish_sync(self, event_type: str, payload: Dict[str, Any]):
        """Helper to publish from synchronous code by creating a task."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.publish(event_type, payload))
        except RuntimeError:
            # If no running loop, we just ignore for now, though we should always have one in FastAPI
            pass
