import os
import json
import sys
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from maintenance_event import MaintenanceLogger

logger = MaintenanceLogger()
event = logger.log_maintenance("PROP-001", "Fix leaky faucet in Unit 4B", "URGENT", "MANAGER-001")

print(f"[✓] Maintenance event created: {event['maintenance_id']}")
print(f"[✓] Linked to Property: {event['property_id']}")

with open("foundry_property/maintenance_events.json", "r") as f:
    events = json.load(f)
    assert any(e['maintenance_id'] == event['maintenance_id'] for e in events)

print("[★] MAINTENANCE WORKFLOW VERIFY: SUCCESS")
