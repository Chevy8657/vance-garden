import json
import hashlib
import argparse
import sys
from datetime import datetime, timezone

def generate_hash(data_dict):
    """Creates a deterministic hash of the signoff data."""
    json_string = json.dumps(data_dict, sort_keys=True)
    return hashlib.sha256(json_string.encode()).hexdigest()

def process_signoff(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # 1. Validate Incident Existence (Stub logic for now)
        print(f"--- Foundry Integrity Layer: Sign-Off Processor ---")
        print(f"Validating Incident: {data['incident_id']}")
        
        # 2. Logic Check: Ensure we aren't re-signing a closed case
        if data.get('final_case_status') == "CLOSED_ATTESTED":
            print("ERROR: This incident is already closed and attested.")
            return

        # 3. Generate Manager Attestation Hash
        attestation_data = {
            "incident_id": data['incident_id'],
            "manager_id": data['authorized_agent']['id'],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "note": data['manager_note']
        }
        
        attestation_hash = generate_hash(attestation_data)
        data['manager_attestation_hash'] = attestation_hash
        data['final_case_status'] = "CLOSED_ATTESTED"
        
        # 4. Save and Seal
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"SUCCESS: Incident {data['incident_id']} closed.")
        print(f"Attestation Hash: {attestation_hash}")
        print(f"Status: {data['final_case_status']}")
        print(f"--- Dossier Updated ---")

    except Exception as e:
        print(f"CRITICAL ERROR: Reconciliation failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Foundry Manager Sign-Off Utility")
    parser.add_argument("--signoff", required=True, help="Path to the signoff_ledger.json")
    args = parser.parse_args()
    process_signoff(args.signoff)
