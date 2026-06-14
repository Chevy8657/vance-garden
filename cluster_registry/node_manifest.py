import datetime
import json

class NodeManifest:
    def __init__(self, node_id, node_role, command_scope, integrity_hash="INIT"):
        self.node_id = node_id
        self.node_role = node_role
        self.trust_status = "PENDING_HANDSHAKE"
        self.command_scope = command_scope  # List of allowed command strings
        self.last_seen = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.last_integrity_hash = integrity_hash
        self.operator_override_required = False

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "node_role": self.node_role,
            "trust_status": self.trust_status,
            "command_scope": self.command_scope,
            "last_seen": self.last_seen,
            "last_integrity_hash": self.last_integrity_hash,
            "operator_override_required": self.operator_override_required
        }

if __name__ == "__main__":
    # Example node registration: Sync operator with limited command scope
    test_node = NodeManifest(
        node_id="NODE-ALPHA-001",
        node_role="SYNC_OPERATOR",
        command_scope=["READ_TELEMETRY", "PROPOSE_CONSENSUS"]
    )
    print(json.dumps(test_node.to_dict(), indent=4))
