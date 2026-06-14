import json
from datetime import datetime, timezone

class InsuranceExporter:
    @staticmethod
    def export(dossier):
        # Maps internal intelligence to external underwriting requirements
        return {
            "dossier_type": "INSURANCE_UNDERWRITING_DOSSIER",
            "property_id": dossier.get("property_id"),
            
            "health_score": dossier.get("health_score"),
            "risk_classification": dossier.get("risk_classification"),
            
            "inspection_status": dossier.get("inspection_status"),
            "maintenance_status": "CURRENT" if dossier["maintenance_status"]["open"] == 0 else "AT_RISK",
            "occupancy_status": dossier.get("occupancy_status"),
            
            "manager_attestation": "COMPLETE" if dossier.get("manager_attestation") else "PENDING",
            "chain_integrity": dossier.get("chain_integrity"),
            
            "underwriting_confidence": "HIGH" if dossier.get("health_score", 0) >= 90 else "LOW",
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
