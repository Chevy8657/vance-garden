import sys
import os
sys.path.append(os.getcwd())
from foundry_marketplace.manager_trust_profile import ManagerTrustProfile

manager_id = "ROGUE-PM-001"
tracker = ManagerTrustProfile()

print(f"--- STRESS TEST: ROGUE MANAGER ({manager_id}) ---")

for i in range(1, 4):
    profile = tracker.update_manager_risk(manager_id, success=False)
    print(f"Override #{i} | Outcome: FAILURE | Status: {profile['status']}")

assert profile['status'] == "RESTRICTED_MANAGER"
print("--- STRESS TEST COMPLETE: GOVERNANCE ENFORCED ---")
