from quarantine_notifier import create_incident
from registry_health_check import mark_stale_nodes
import json

def run_safe_reconciliation(registry_path):
    with open(registry_path, 'r+') as f:
        nodes = json.load(f)
        for node in nodes:
            # Check for staleness transition
            if node['trust_status'] == "TRUSTED":
                # Re-run check (simplified for demo)
                updated_nodes = mark_stale_nodes([node])
                if updated_nodes[0]['trust_status'] == "STALE":
                    create_incident(
                        node['node_id'], 
                        "TRUSTED", 
                        "STALE_QUARANTINED", 
                        "Heartbeat threshold exceeded"
                    )
                    node['trust_status'] = "STALE_QUARANTINED"
        
        f.seek(0)
        json.dump(nodes, f, indent=4)
        f.truncate()

if __name__ == "__main__":
    run_safe_reconciliation('sample_nodes.json')
