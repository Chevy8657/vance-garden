import json
import hashlib
import datetime

class TargetIntakeNormalizer:
    def __init__(self):
        # Explicit mandatory keys required to clear the airlock boundary
        self.required_fields = [
            "source_system", 
            "event_type", 
            "broker_id", 
            "property_id", 
            "timestamp"
        ]

    def normalize_external_payload(self, raw_data: dict) -> dict:
        """
        Translates unpredictable real estate technology payloads into sterile standard objects.
        Throws ValueError if structural integrity requirements are unmet.
        """
        # 1. Map external broker/platform variance to internal standard fields
        normalized = {
            "source_system": raw_data.get("originating_platform"),
            "event_type": raw_data.get("action_name"),
            "broker_id": raw_data.get("operator_identifier"),
            "property_id": raw_data.get("asset_num"),
            "timestamp": raw_data.get("event_time_iso")
        }

        # 2. Structural Field Validation Guard
        missing_fields = [field for field in self.required_fields if not normalized[field]]
        if missing_fields:
            raise ValueError(f"Airlock Ingestion Rejected. Missing required parameters: {missing_fields}")

        # 3. Generate Inner Payload Hash for Immutable Tracking
        inner_str = json.dumps(raw_data.get("meta_payload", {}), sort_keys=True)
        payload_hash = hashlib.sha256(inner_str.encode('utf-8')).hexdigest()

        # 4. Compile Sterile, Engine-Ready Object
        normalized["payload_hash"] = payload_hash
        normalized["raw_payload_reference"] = raw_data.get("meta_payload", {})

        return normalized
