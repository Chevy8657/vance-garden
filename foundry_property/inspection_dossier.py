import json
import os
from datetime import datetime, timezone

class DossierGenerator:
    def __init__(self, property_file="foundry_property/properties.json", inspection_file="foundry_property/property_events.json", output_dir="inspection_dossiers"):
        self.property_file = property_file
        self.inspection_file = inspection_file
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, property_id):
        with open(self.property_file, "r") as f:
            properties = json.load(f)
        with open(self.inspection_file, "r") as f:
            inspections = json.load(f)

        property_record = next((p for p in properties if p.get("property_id") == property_id), None)
        if not property_record:
            raise ValueError(f"Property not found: {property_id}")

        related_inspections = [i for i in inspections if i.get("property_id") == property_id]

        dossier = {
            "dossier_type": "PROPERTY_INSPECTION_DOSSIER",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "property": property_record,
            "inspection_count": len(related_inspections),
            "inspections": related_inspections,
            "status": "DOSSIER_GENERATED"
        }

        output_path = os.path.join(self.output_dir, f"inspection_dossier_{property_id}.json")
        with open(output_path, "w") as f:
            json.dump(dossier, f, indent=4)
        return output_path
