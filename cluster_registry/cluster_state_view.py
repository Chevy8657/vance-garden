import json
import os

class ClusterStateView:
    def __init__(self, registry_path):
        self.registry_path = registry_path

    def get_eligible_nodes(self, required_role=None):
        """Filters nodes by trust and role for command eligibility."""
        eligible = []
        if not os.path.exists(self.registry_path):
            return eligible
            
        with open(self.registry_path, 'r') as f:
            nodes = json.load(f)
            
        for node in nodes:
            # Rule: Must be TRUSTED and active to receive commands
            if node['trust_status'] == "TRUSTED":
                if not required_role or node['node_role'] == required_role:
                    eligible.append(node)
        return eligible

if __name__ == "__main__":
    # Mocking a registry file for the view
    view = ClusterStateView('sample_nodes.json')
    print("[i] Checking eligible SYNC_OPERATOR nodes...")
    print(view.get_eligible_nodes(required_role="SYNC_OPERATOR"))
