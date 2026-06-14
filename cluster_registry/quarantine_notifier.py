import json
import datetime
import uuid

INCIDENT_LOG = '/home/rick/pet_alpha/cluster_registry/quarantine_events.json'

def create_incident(node_id, old_status, new_status, reason):
    incident = {
        "incident_id": str(uuid.uuid4()),
        "node_id": node_id,
        "previous_status": old_status,
        "new_status": new_status,
        "reason": reason,
        "detected_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "operator_action_required": True
    }
    
    # Append to incident record
    try:
        with open(INCIDENT_LOG, 'r+') as f:
            data = json.load(f)
            data.append(incident)
            f.seek(0)
            json.dump(data, f, indent=4)
    except FileNotFoundError:
        with open(INCIDENT_LOG, 'w') as f:
            json.dump([incident], f, indent=4)
            
    print(f"[!] QUARANTINE INCIDENT LOGGED: {node_id} marked as {new_status} (Reason: {reason})")
