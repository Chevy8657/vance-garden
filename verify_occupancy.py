import os
import sys
import json
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from occupancy_verifier import OccupancyVerifier

verifier = OccupancyVerifier()
record = verifier.verify("PROP-001", "OCCUPIED", "MANAGER-001")

print(f"[✓] Occupancy verified: {record['verification_id']}")
print(f"[✓] Status: {record['occupancy_status']}")

with open("foundry_property/occupancy_records.json", "r") as f:
    records = json.load(f)
    assert any(r['verification_id'] == record['verification_id'] for r in records)

print("[★] OCCUPANCY VERIFICATION VERIFY: SUCCESS")
