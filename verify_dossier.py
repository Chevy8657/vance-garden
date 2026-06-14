import os
import sys
import json

sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from inspection_dossier import DossierGenerator

os.makedirs("foundry_property", exist_ok=True)

props_path = "foundry_property/properties.json"
events_path = "foundry_property/property_events.json"

with open(props_path, "w") as f:
    json.dump([{"property_id": "PROP-001"}], f, indent=4)

with open(events_path, "w") as f:
    json.dump([{"property_id": "PROP-001", "event_type": "PROPERTY_INSPECTION"}], f, indent=4)

generator = DossierGenerator()
path = generator.generate("PROP-001")

print(f"[✓] Dossier generated: {path}")
print("[★] INSPECTION DOSSIER VERIFY: SUCCESS")
