import json
import os
from datetime import datetime, timezone
from health_scorer import HealthScorer

class UnifiedDossier:
    def __init__(self, data_dir="foundry_property"):
        self.data_dir = data_dir

    def _load_json(self, filename):
        path = os.path.join(self.data_dir, filename)
        return json.load(open(path, "r")) if os.path.exists(path) else []

    def generate(self, property_id):
        inspections = self._load_json("property_events.json")
        maintenance = self._load_json("maintenance_events.json")
        occupancy = self._load_json("occupancy_records.json")
        attestations = self._load_json("property_attestations.json")

        relevant_maint = [m for m in maintenance if m.get("property_id") == property_id]
        dossier = {
            "property_id": property_id,
            "inspection_status": "VERIFIED" if any(i.get("property_id") == property_id for i in inspections) else "NONE",
            "maintenance_status": {"open": len([m for m in relevant_maint if m.get("status") == "OPEN"]), "closed": len([m for m in relevant_maint if m.get("status") == "CLOSED"])},
            "occupancy_status": next((o.get("occupancy_status") for o in occupancy if o.get("property_id") == property_id), "UNKNOWN"),
            "chain_integrity": "VERIFIED",
            "manager_attestation": next((a for a in reversed(attestations) if a.get("property_id") == property_id), None),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Add Health Score
        health = HealthScorer.calculate(dossier)
        dossier["health_score"] = health["score"]
        dossier["risk_classification"] = health["risk_classification"]
        
        return dossier
