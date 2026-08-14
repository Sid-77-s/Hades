from typing import List, Dict, Optional, Any

class BaseAdapter:
    async def execute(self, objective: str, context: Dict[str, Any]) -> Any:
        raise NotImplementedError
        
    async def observe(self) -> Any:
        raise NotImplementedError
        
    async def validate(self) -> bool:
        raise NotImplementedError

class CapabilityRegistry:
    def __init__(self):
        self.adapters: Dict[str, List[BaseAdapter]] = {}
        
    def register(self, category: str, adapter: BaseAdapter):
        if category not in self.adapters:
            self.adapters[category] = []
        self.adapters[category].append(adapter)
        
    def get_best_adapter(self, allowed_categories: List[str]) -> Optional[BaseAdapter]:
        for category in allowed_categories:
            if category in self.adapters and len(self.adapters[category]) > 0:
                # For demo, just return the first registered adapter for the category
                return self.adapters[category][0]
        return None
