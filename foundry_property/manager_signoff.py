import json
import os
from datetime import datetime, timezone
import uuid

class ManagerSignOff:
    def __init__(self, attestation_file="foundry_property/property_attestations.json"):
        self.attestation_file = attestation_file
        if not os.path.exists(self.attestation_file):
            with open(self.attestation_file, "w") as f:
                json.dump([], f)

    def attest(self, property_id, manager_id, note, dossier_hash):
        record = {
            "attestation_id": f"ATT-{uuid.uuid4().hex[:8].upper()}",
            "property_id": property_id,
            "manager_id": manager_id,
            "manager_note": note,
            "signed_at": datetime.now(timezone.utc).isoformat(),
            "dossier_hash": dossier_hash,
            "status": "CLOSED_ATTESTED"
        }
        
        with open(self.attestation_file, "r+") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=4)
            
        return record
