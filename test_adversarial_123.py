import json, os, shutil
from deployment.run_all_health_checks import perform_readiness_freeze

def run_adversarial_suite():
    print("--- ADVERSARIAL TEST 1: Corrupted Manifest ---")
    with open('/home/rick/pet_alpha/builds/REL-LATEST/appliance_manifest.json', 'r+') as f:
        data = json.load(f)
        data['status'] = 'FROZEN_FOR_DEPLOYMEN'
        f.seek(0); json.dump(data, f); f.truncate()
    # Expect: Readiness Check to fail
    
    print("\n--- ADVERSARIAL TEST 2: Broken Chain of Custody ---")
    with open('/home/rick/pet_alpha/forensic_ledger.json', 'r+') as f:
        ledger = json.load(f)
        ledger.pop(1) # Break the link
        f.seek(0); json.dump(ledger, f); f.truncate()
    
    print("\n--- ADVERSARIAL TEST 3: Stale Injection ---")
    # Force trust on stale node
    with open('/home/rick/pet_alpha/cluster_registry/sample_nodes.json', 'r+') as f:
        nodes = json.load(f)
        nodes[2]['trust_status'] = "TRUSTED"
        f.seek(0); json.dump(nodes, f); f.truncate()
    # Expect: Reconciler to catch it and trigger quarantine
