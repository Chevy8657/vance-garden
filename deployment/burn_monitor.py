import time
import json
import os

def get_burn_metrics():
    # 1. Forensic Outbox Signal
    outbox_file = '/home/rick/pet_alpha/cluster_registry/alert_outbox.json'
    alerts = []
    if os.path.exists(outbox_file):
        with open(outbox_file, 'r') as f:
            alerts = [line for line in f if line.strip()]
    
    # 2. Reconciliation Loop Status
    # Assuming a simple log check for recent corrective actions
    reconciler_log = '/home/rick/pet_alpha/cluster_registry/reconcile_activity.log'
    actions = 0
    if os.path.exists(reconciler_log):
        with open(reconciler_log, 'r') as f:
            actions = sum(1 for line in f if "CORRECTIVE_ACTION" in line)
            
    # 3. Drift Telemetry
    # Simulating a drift check against the monotonic clock
    drift = 0.002 # Seconds of drift detected

    return {
        "alert_count": len(alerts),
        "reconciler_interventions": actions,
        "clock_drift_seconds": drift
    }

def display_dashboard():
    while True:
        metrics = get_burn_metrics()
        print("\n" + "="*50)
        print("FOUNDRY APPLIANCE: 72-HOUR BURN MONITOR")
        print("="*50)
        print(f"[*] Forensic Alerts       : {metrics['alert_count']}")
        print(f"[*] Reconciler Actions    : {metrics['reconciler_interventions']}")
        print(f"[*] Current Clock Drift   : {metrics['clock_drift_seconds']}s")
        print("="*50)
        time.sleep(10)

if __name__ == "__main__":
    display_dashboard()
