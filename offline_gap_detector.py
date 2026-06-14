import sqlite3
import datetime

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

def calculate_peer_drift(node_id):
    """
    Computes precise timestamp delta of re-emerging mesh peers against 4h/24h/7d parameters.
    Guarantees cross-platform timezone compatibility.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT last_seen FROM peer_registry WHERE node_id = ?;", (node_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row or not row['last_seen']:
        return "NEW_PEER_INITIAL_SYNC", 0.0
        
    last_seen_raw = row['last_seen']
    
    # Standardize incoming string format to ensure offset-awareness
    try:
        last_seen_dt = datetime.datetime.fromisoformat(last_seen_raw)
        if last_seen_dt.tzinfo is None:
            # Force naive strings to map directly to explicit UTC
            last_seen_dt = last_seen_dt.replace(tzinfo=datetime.timezone.utc)
    except Exception:
        return "MALFORMED_TIMESTAMP_ERROR", 0.0
        
    now = datetime.datetime.now(datetime.timezone.utc)
    drift_hours = (now - last_seen_dt).total_seconds() / 3600.0
    
    # Evaluate risk profile based on disconnection depth
    if drift_hours >= 168.0: # 7 Days
        return "MANUAL_REVIEW_THRESHOLD_EXCEEDED", drift_hours
    elif drift_hours >= 24.0:
        return "STALE_PEER_RECONCILIATION_REQUIRED", drift_hours
    elif drift_hours >= 4.0:
        return "STANDARD_OFFLINE_GAP", drift_hours
        
    return "HEALTHY_WINDOW", drift_hours
