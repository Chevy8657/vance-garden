import json
from registry_health_check import mark_stale_nodes
from core_command_router import CommandRouter

REGISTRY_PATH = '/home/rick/pet_alpha/cluster_registry/sample_nodes.json'

def run_reconciliation():
    print("--- LAUNCHING CONSENSUS RECONCILIATION DAEMON ---")
    
    # 1. Load and Audit
    with open(REGISTRY_PATH, 'r+') as f:
        nodes = json.load(f)
        updated_nodes = mark_stale_nodes(nodes)
        
        # 2. Persist reconciled state
        f.seek(0)
        json.dump(updated_nodes, f, indent=4)
        f.truncate()
        
    print("[✓] Registry state reconciled with network pulse.")
    
    # 3. Proceed with Router
    router = CommandRouter(REGISTRY_PATH)
    router.route_command("READ_TELEMETRY", "SYNC_OPERATOR")

if __name__ == "__main__":
    run_reconciliation()
