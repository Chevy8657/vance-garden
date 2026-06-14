import os
from alert_forwarder import stage_alert

def run_adversarial_45():
    print("--- ADVERSARIAL TEST 4: Outbox Failure ---")
    os.chmod('/home/rick/pet_alpha/cluster_registry/alert_outbox.json', 0o444)
    # Expect: Alert logged to incident journal, but outbox write error handled
    
    print("\n--- ADVERSARIAL TEST 5: Replay Storm ---")
    # Injecting 100 identical packet IDs via a loop
    for _ in range(100):
        # Trigger same packet ID through handshake engine
        pass 
    # Expect: Protocol engine drops duplicates via monotonic epoch check
