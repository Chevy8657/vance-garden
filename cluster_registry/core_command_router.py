from cluster_state_view import ClusterStateView
from command_permissions import can_execute_command
import json

class CommandRouter:
    def __init__(self, registry_path):
        self.view = ClusterStateView(registry_path)

    def route_command(self, command, required_role):
        print(f"--- ROUTING COMMAND: {command} ---")
        eligible_nodes = self.view.get_eligible_nodes(required_role=required_role)
        
        if not eligible_nodes:
            print(f"[✕] ROUTING FAILED: No active/trusted nodes found for role {required_role}")
            return False

        for node in eligible_nodes:
            # Secondary check: Validate command scope against role permissions
            if can_execute_command(node, command):
                print(f"[✓] COMMAND DISPATCHED: {command} -> {node['node_id']}")
            else:
                print(f"[!] PERMISSION DENIED: {node['node_id']} cannot execute {command}")
        
        return True

if __name__ == "__main__":
    router = CommandRouter('cluster_registry/sample_nodes.json')
    # Test valid route
    router.route_command("READ_TELEMETRY", "SYNC_OPERATOR")
    # Test unauthorized command attempt
    router.route_command("ALL_COMMANDS", "SYNC_OPERATOR")
