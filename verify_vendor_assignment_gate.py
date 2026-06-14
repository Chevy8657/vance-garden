import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from vendor_assignment_gate import VendorAssignmentGate

# Test Case 1: Verified Vendor
v1 = {"trust_status": "VERIFIED"}
assert VendorAssignmentGate.check_eligibility(v1)["status"] == "APPROVED"

# Test Case 2: Probation Vendor
v2 = {"trust_status": "PROBATION"}
assert VendorAssignmentGate.check_eligibility(v2)["status"] == "DENIED_MANAGER_OVERRIDE_REQUIRED"

# Test Case 3: Suspended Vendor
v3 = {"trust_status": "SUSPENDED"}
assert VendorAssignmentGate.check_eligibility(v3)["status"] == "DENIED_VENDOR_SUSPENDED"

print("[★] VENDOR ASSIGNMENT GATE VERIFY: SUCCESS")
