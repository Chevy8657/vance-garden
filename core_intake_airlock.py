import json
import hashlib
import hmac
import datetime

class CoreIntakeAirlock:
    def __init__(self):
        # Enforce structural parameter validations required for internal system pipelines
        self.required_fields = ["source_system", "event_type", "broker_id", "property_id"]
        
    def process_external_ingress(self, raw_json_payload: str) -> dict:
        """
        Parses untrusted external JSON data, verifies schema integrity, 
        and normalizes structural fields to match internal node specifications.
        """
        try:
            payload = json.loads(raw_json_payload)
        except json.JSONDecodeError:
            raise ValueError("Airlock Ingestion Rejected. Invalid JSON formatting format.")

        # Enforce structural defense perimeter
        missing_fields = [field for field in self.required_fields if field not in payload]
        if missing_fields:
            raise SecurityException(f"Airlock Ingestion Rejected. Missing required parameters: {missing_fields}")

        # Execute internal normalization and field mapping
        normalized_data = {
            "source_platform": payload.get("source_system"),
            "external_event": payload.get("event_type"),
            "routing_context": f"REGISTRY-{payload.get('broker_id')}",
            "payload_hash": hashlib.sha256(raw_json_payload.encode('utf-8')).hexdigest(),
            "extracted_body": payload
        }
        
        return normalized_data

class SecurityException(Exception):
    """Custom exception vector to flag inbound policy violations."""
    pass

if __name__ == "__main__":
    print("="*90)
    print("RUNNING INBOUND DATA INTAKE AIRLOCK INTEGRATION TEST")
    print("="*90)
    
    airlock = CoreIntakeAirlock()
    
    # Mocking an untrusted incoming payload (e.g., from an escrow event tracker)
    valid_sample_payload = {
        "source_system": "KW_MegaCamp_Ingest_2026",
        "event_type": "escrow_contract_signed",
        "broker_id": "BRK-9921",
        "property_id": "PROP-NEVADA-88211",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "raw_payload_reference": {
            "client_type": "high-trust operational partner",
            "agreed_reduction_logic": "10-to-Zero hook",
            "escrow_agent": "Joy Grimmer"
        }
    }
    
    # 1. Test nominal valid path execution
    raw_input = json.dumps(valid_sample_payload, indent=4)
    try:
        cleared_packet = airlock.process_external_ingress(raw_input)
        print("\033[38;5;44m[✓] INTAKE NORMALIZATION SUCCESSFUL:\033[0m")
        print(json.dumps(cleared_packet, indent=4))
    except (ValueError, SecurityException) as e:
        print(f"[✕] Unexpected Nominal Path Failure: {e}")
        
    print("\n" + "="*90)
    print("TESTING STRUCTURAL DEFENSE INGESTION BLOCK")
    print("="*90)
    
    # 2. Test defense perimeter path by intentionally dropping the mandatory 'property_id' tag
    invalid_sample_payload = valid_sample_payload.copy()
    del invalid_sample_payload["property_id"]
    raw_invalid_input = json.dumps(invalid_sample_payload)
    
    try:
        airlock.process_external_ingress(raw_invalid_input)
        print("[✕] Perimeter Failure: Invalid payload leaked through security airlock filters.")
    except SecurityException as e:
        print(f"\033[38;5;214m[✓] Expected Security Exception Intercepted successfully:\033[0m")
        print(f"    └── {e}")
    print("="*90)
