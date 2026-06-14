import sqlite3
from offline_gap_detector import calculate_peer_drift

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

def inspect_ingress_clearance(node_id):
    """
    Perimeter Defense: Enforces strict behavioral policy checks and 
    temporal drift constraints dynamically at the boundary gate.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT trust_status FROM peer_registry WHERE node_id = ?;", (node_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return "PROVISIONAL_PASS", "New identity encountered. Proceeding to cryptographic staging."
        
    static_status = row['trust_status']
    
    # 1. Immediate Static Policy Ejection
    if static_status == "SUSPENDED":
        return "DENIED", "Identity is SUSPENDED due to severe behavioral policy violation."
    elif static_status == "QUARANTINED":
        return "DENIED", "Identity is QUARANTINED. Awaiting manual override."
        
    # 2. Dynamic Temporal Drift Intercept
    drift_condition, drift_hours = calculate_peer_drift(node_id)
    if drift_condition == "MANUAL_REVIEW_THRESHOLD_EXCEEDED":
        return "DENIED", f"Identity DENIED via Dynamic Policy. Temporal gap ({drift_hours:.2f} hrs) requires manual override."
        
    return "APPROVED", f"Identity cleared with status: {static_status}."
