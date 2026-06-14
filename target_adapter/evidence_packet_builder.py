import json
import hashlib
import hmac

class EvidencePacketBuilder:
    def __init__(self, node_signing_key: str):
        # A 32-byte secret representing the local Node's private cryptographic key
        self.signing_key = node_signing_key.encode('utf-8')

    def seal_evidence_packet(self, mapped_payload: dict, simulated_packet_id: str) -> dict:
        """
        Wraps sterile real estate records into a cryptographically sealed network envelope.
        Generates an immutable signature verification seal for target gate clearance.
        """
        # Serialize the standard structural payload into a canonical string format
        canonical_body = json.dumps(mapped_payload, sort_keys=True)
        
        # Calculate the immutable transit signature using HMAC-SHA256
        signature = hmac.new(
            self.signing_key, 
            canonical_body.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()

        # Build the final wire envelope package
        sealed_envelope = {
            "packet_id": simulated_packet_id,
            "origin_node": "NODE-ALPHA-001",
            "routing_context": mapped_payload.get("routing_context"),
            "payload_type": mapped_payload.get("internal_event_type"),
            "serialized_body": canonical_body,
            "transit_signature": signature
        }
        
        return sealed_envelope
