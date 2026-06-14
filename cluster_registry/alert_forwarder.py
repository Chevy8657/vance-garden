import json
import datetime
import uuid
import os

OUTBOX = '/home/rick/pet_alpha/cluster_registry/alert_outbox.json'
DELIVERY_LOG = '/home/rick/pet_alpha/cluster_registry/alert_delivery_log.json'

def stage_alert(incident):
    alert = {
        "alert_id": str(uuid.uuid4()),
        "incident_id": incident['incident_id'],
        "node_id": incident['node_id'],
        "severity": "CRITICAL" if incident['new_status'] in ['QUARANTINED', 'SUSPENDED'] else "WARNING",
        "message": f"Node {incident['node_id']} state transition: {incident['previous_status']} -> {incident['new_status']}",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "delivery_status": "PENDING",
        "delivery_attempts": 0,
        "last_attempt_at": None
    }
    
    # Stage to outbox
    with open(OUTBOX, 'a') as f:
        f.write(json.dumps(alert) + '\n')
    print(f"[➔] ALERT STAGED: {alert['alert_id']} (Severity: {alert['severity']})")

def process_outbox():
    """Simulates a local-first delivery attempt (file-to-file shift)."""
    if not os.path.exists(OUTBOX): return
    
    with open(OUTBOX, 'r') as f:
        alerts = [json.loads(line) for line in f if line.strip()]
        
    for alert in alerts:
        # Simulation: Moving to delivery log
        alert['delivery_status'] = "DELIVERED"
        alert['delivery_attempts'] += 1
        alert['last_attempt_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        with open(DELIVERY_LOG, 'a') as f:
            f.write(json.dumps(alert) + '\n')
            
    # Clear outbox
    open(OUTBOX, 'w').close()
    print("[✓] OUTBOX PROCESSED: Alerts cleared to delivery log.")
