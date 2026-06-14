class BrokerEventMapper:
    def __init__(self):
        # Maps raw external platform definitions to internal operational events
        self.event_translation_matrix = {
            "escrow_contract_signed": "STATE_UPDATE_RECORD",
            "lead_lock_submission": "DATA_INTAKE_EVENT",
            "agent_node_provisioned": "PEER_CONFIG_CHANGE",
            "commission_fee_adjusted": "GOVERNANCE_MUTATION"
        }

    def map_to_internal_spec(self, normalized_payload: dict) -> dict:
        """
        Translates real estate domain language into hardened structural categories.
        """
        external_event = normalized_payload.get("event_type")
        internal_event = self.event_translation_matrix.get(external_event)

        if not internal_event:
            # If an incoming event shape doesn't match an active rule, force a safe default classification
            internal_event = "UNCLASSIFIED_EXTERNAL_RECORD"

        # Deep copy and enrich the dictionary with internal structural metrics
        mapped_data = normalized_payload.copy()
        mapped_data["internal_event_type"] = internal_event
        
        # Enforce deterministic tracking context tags
        mapped_data["routing_context"] = f"REGISTRY-{normalized_payload['broker_id']}"
        
        return mapped_data
