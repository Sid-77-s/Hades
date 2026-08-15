from typing import Dict, List, Optional
from src.skills.base import BaseSkill, SkillStatus
import importlib
import pkgutil
import inspect

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        self._categories: Dict[str, List[str]] = {}

    def register(self, skill: BaseSkill):
        meta = skill.metadata
        self._skills[meta.skill_id] = skill
        if meta.category not in self._categories:
            self._categories[meta.category] = []
        self._categories[meta.category].append(meta.skill_id)

    def get_skill(self, skill_id: str) -> Optional[BaseSkill]:
        return self._skills.get(skill_id)

    def get_skills_by_category(self, category: str) -> List[BaseSkill]:
        skill_ids = self._categories.get(category, [])
        return [self._skills[sid] for sid in skill_ids]

    def get_all_skills(self) -> List[BaseSkill]:
        return list(self._skills.values())

    def get_healthy_skills(self) -> List[BaseSkill]:
        return [s for s in self._skills.values() if s.metadata.health_status == SkillStatus.READY]

    def discover_skills(self, package_path: str = "src.skills"):
        """Dynamically load and register all BaseSkill subclasses in the package."""
        try:
            package = importlib.import_module(package_path)
        except ModuleNotFoundError:
            print(f"[SkillRegistry] Package {package_path} not found.")
            return

        # Recursively walk packages
        for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            if "base" in module_name or "registry" in module_name:
                continue
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BaseSkill) and obj is not BaseSkill:
                        # Instantiate and register
                        try:
                            skill_instance = obj()
                            self.register(skill_instance)
                        except Exception as e:
                            print(f"[SkillRegistry] Error instantiating {name}: {e}")
            except Exception as e:
                print(f"[SkillRegistry] Error loading module {module_name}: {e}")

# Global singleton
registry = SkillRegistry()
