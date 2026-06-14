import sys
import os
sys.path.append(os.getcwd())

from foundry_insurance.carrier_property_link import CarrierPropertyLink

linker = CarrierPropertyLink()
# Register the link
link = linker.create_link("CPL-001", "CAR-001", "PROP-001", "UNDERWRITING_REVIEW")

print(f"[✓] Link Created: {link['link_id']} | Carrier {link['carrier_id']} -> Property {link['property_id']}")
print(f"[✓] Authorization Hash: {link['authorization_hash'][:16]}...")

# Verify Access Rule
assert linker.is_authorized("CAR-001", "PROP-001") == True
assert linker.is_authorized("CAR-999", "PROP-001") == False

print("[★] SPRINT 44: CARRIER-PROPERTY LINKING VERIFIED")
