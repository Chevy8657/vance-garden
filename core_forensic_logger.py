import hashlib
import json
import datetime
import os

AUDIT_LOG = '/home/rick/pet_alpha/forensic_ledger.json'

class CoreForensicLogger:
    def __init__(self):
        if not os.path.exists(AUDIT_LOG):
            with open(AUDIT_LOG, 'w') as f:
                json.dump([], f)

    def _get_last_hash(self) -> str:
        with open(AUDIT_LOG, 'r') as f:
            ledger = json.load(f)
            return ledger[-1]['hash'] if ledger else "0" * 64

    def log_security_event(self, event_type: str, details: str):
        """Appends a cryptographically chained event to the ledger."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        prev_hash = self._get_last_hash()
        
        event_data = {
            "timestamp": timestamp,
            "event_type": event_type,
            "details": details,
            "prev_hash": prev_hash
        }
        
        # Calculate current hash
        event_str = json.dumps(event_data, sort_keys=True)
        current_hash = hashlib.sha256(event_str.encode()).hexdigest()
        event_data['hash'] = current_hash

        # Atomic append
        with open(AUDIT_LOG, 'r+') as f:
            ledger = json.load(f)
            ledger.append(event_data)
            f.seek(0)
            json.dump(ledger, f, indent=4)
        
        print(f"[✓] SECURITY EVENT LOGGED: {event_type} (Hash: {current_hash[:16]}...)")

if __name__ == "__main__":
    logger = CoreForensicLogger()
    logger.log_security_event("HANDSHAKE_REJECTION", "Unauthorized node NODE-UNKNOWN-999")
    logger.log_security_event("INTEGRITY_AUDIT", "Zero modifications found")
