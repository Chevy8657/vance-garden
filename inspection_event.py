import hashlib
import datetime
from core_forensic_logger import CoreForensicLogger

class InspectionEvent:
    def __init__(self):
        # Hooks into your existing Forensic Ledger
        self.ledger = CoreForensicLogger()

    def record_inspection(self, inspection_data):
        """
        Captures an inspection event and commits it to the forensic ledger.
        """
        # 1. Enrich data with timestamp
        inspection_data['date'] = datetime.datetime.utcnow().isoformat()
        
        # 2. Generate Attestation Hash
        # Seals the inspection data so it cannot be tampered with later
        data_string = f"{inspection_data['inspection_id']}{inspection_data['property_id']}{inspection_data['findings']}"
        inspection_data['attestation_hash'] = hashlib.sha256(data_string.encode()).hexdigest()

        # 3. Commit to Ledger
        event_payload = {
            "event_type": "PROPERTY_INSPECTION",
            "data": inspection_data
        }
        
        self.ledger.record(event_payload)
        
        return inspection_data['attestation_hash']
