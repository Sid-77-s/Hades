import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.skills.registry import registry
import asyncio

def run_verification():
    print("============================================================")
    print("HADES SKILL VERIFICATION")
    print("============================================================\n")
    
    registry.discover_skills()
    skills = registry.get_all_skills()
    
    if not skills:
        print("No skills found in the registry.")
        return
        
    counts = {
        "READY": 0,
        "PARTIAL": 0,
        "FAILED": 0,
        "CONFIGURATION_REQUIRED": 0,
        "REQUIRES_PAID_SERVICE": 0,
        "UNAVAILABLE": 0
    }
    
    for skill in skills:
        meta = skill.metadata
        status = meta.health_status
        if status in counts:
            counts[status] += 1
            
        icon = "[OK]" if status == "READY" else "[WARN]" if status in ["PARTIAL", "CONFIGURATION_REQUIRED"] else "[FAIL]"
        
        print(f"{icon} {meta.name} ({meta.skill_id})")
        print(f"   Provider: {', '.join(meta.supported_providers) if meta.supported_providers else 'Local'}")
        print(f"   Status: {status}")
        if meta.required_credentials:
            print(f"   Required Credentials: {', '.join(meta.required_credentials)}")
        print(f"   Risk: {meta.risk_level} | Cost: {meta.estimated_cost}")
        print()
        
    print("============================================================")
    print("SUMMARY")
    print("============================================================")
    for k, v in counts.items():
        if v > 0 or k in ["READY", "FAILED", "CONFIGURATION_REQUIRED"]:
            print(f"{k}: {v}")

if __name__ == "__main__":
    run_verification()
