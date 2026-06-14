import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from manager_override import ManagerOverride
from vendor_assignment_gate import VendorAssignmentGate

# 1. Gate is currently blocking
gate = VendorAssignmentGate()
probation_vendor = {"trust_status": "PROBATION"}
assert gate.check_eligibility(probation_vendor)["status"] == "DENIED_MANAGER_OVERRIDE_REQUIRED"

# 2. Manager provides override
override_engine = ManagerOverride()
override = override_engine.request_override("VEND-001", "PROP-001", "PM-001", "Emergency plumbing")

# 3. Success assertion
print(f"[✓] Override Granted: {override['override_id']}")
print(f"[✓] Reason: {override['work_order_reason']}")
assert override["status"] == "APPROVED_MANAGER_OVERRIDE"

print("[★] MANAGER OVERRIDE VERIFY: SUCCESS")
