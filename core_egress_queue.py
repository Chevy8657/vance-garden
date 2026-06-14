import json
import hashlib
import hmac
import datetime
import os

EGRESS_SPOOL_PATH = '/home/rick/pet_alpha/egress_spool.json'
CORE_SECRET = "FOUNDRY_SECRET_SECURE_TOKEN_2026"

class CoreEgressQueue:
    def __init__(self, origin_node="NODE-ALPHA-001"):
        self.origin_node = origin_node

    def spool_outbound_state_sync(self, config_key: str, config_value: str, target_routing_context: str) -> str:
        """
        Packages an internal state mutation into a signed outbound evidence envelope
        and appends it to the non-blocking egress network spool.
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        outbound_id = f"OUT-PKT-{hashlib.md5(f'{config_key}-{timestamp}'.encode()).hexdigest()[:8].upper()}"

        # 1. Structure the crisp internal payload body
        sync_payload = {
            "origin_node": self.origin_node,
            "routing_context": target_routing_context,
            "mutated_key": config_key,
            "mutated_value": config_value,
            "state_timestamp": timestamp
        }
        serialized_body = json.dumps(sync_payload, sort_keys=True)

        # 2. Cryptographically seal the outgoing envelope
        signature = hmac.new(
            CORE_SECRET.encode('utf-8'),
            serialized_body.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        envelope = {
            "outbound_packet_id": outbound_id,
            "serialized_payload": serialized_body,
            "egress_signature": signature,
            "spooled_at": timestamp
        }

        # 3. Read-Modify-Write safe append to local file queue
        spool_data = []
        if os.path.exists(EGRESS_SPOOL_PATH):
            try:
                with open(EGRESS_SPOOL_PATH, 'r') as f:
                    spool_data = json.load(f)
            except json.JSONDecodeError:
                spool_data = []

        spool_data.append(envelope)

        with open(EGRESS_SPOOL_PATH, 'w') as f:
            json.dump(spool_data, f, indent=4)

        return outbound_id
