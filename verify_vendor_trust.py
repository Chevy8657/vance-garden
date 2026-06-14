import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from vendor_trust_profile import VendorTrustProfile

trust = VendorTrustProfile()

# Simulate a successful job completion
profile = trust.update_reputation("VEND-001", success=True)

print(f"[✓] Vendor: {profile['vendor_id']}")
print(f"[✓] Completion Rate: {profile['completion_rate'] * 100}%")
print(f"[✓] Status: {profile['trust_status']}")

assert profile['completion_rate'] == 1.0
assert profile['trust_status'] == "VERIFIED"
print("[★] VENDOR TRUST UPDATE VERIFY: SUCCESS")
