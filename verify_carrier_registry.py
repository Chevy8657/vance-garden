import sys
import os
sys.path.append(os.getcwd())

from foundry_insurance.carrier_registry import CarrierRegistry

registry = CarrierRegistry()
carrier = registry.register("CAR-001", "Example Carrier", "PROPERTY_INSURANCE", "GA")

print(f"[✓] Carrier Registered: {carrier['carrier_name']} (ID: {carrier['carrier_id']})")
print(f"[✓] Registration Hash: {carrier['registration_hash'][:16]}...")

assert carrier['status'] == "ACTIVE"
assert 'registration_hash' in carrier
print("[★] SPRINT 43: CARRIER REGISTRY VERIFIED")
