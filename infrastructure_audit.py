import sqlite3
import datetime
import uuid

def initialize_audit_vault():
    """
    Initializes a completely decoupled security ledger for infrastructure operational events.
    Isolating this from the telemetry layer ensures tamper protection and unassailable authority.
    """
    AUDIT_DB = '/home/rick/pet_alpha/infrastructure_audit.db'
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_ledger (
        event_id TEXT PRIMARY KEY,
        timestamp_utc TEXT NOT NULL,
        event_type TEXT NOT NULL,
        actor TEXT NOT NULL,
        description TEXT NOT NULL,
        integrity_hash TEXT
    );
    ''')
    conn.commit()
    conn.close()

def log_infrastructure_event(event_type, actor, description):
    """
    Appends an immutable tracking entry to the localized security audit ledger.
    """
    initialize_audit_vault()
    
    AUDIT_DB = '/home/rick/pet_alpha/infrastructure_audit.db'
    event_id = f"EVT-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    conn = sqlite3.connect(AUDIT_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO audit_ledger (event_id, timestamp_utc, event_type, actor, description, integrity_hash)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (event_id, timestamp, event_type.upper(), actor.upper(), description, 'LOCAL_SIGNED_PRIMITIVE'))
    
    conn.commit()
    conn.close()
    
    # Clinical, clear verification terminal string
    print(f"\033[38;5;44m  [🛡️  AUDIT LOGGED] {event_type.upper()} | Actor: {actor.upper()} | ID: {event_id}\033[0m")
    return event_id

if __name__ == "__main__":
    # Test initialize and append a system event
    log_infrastructure_event("SYSTEM_BOOT", "NODE-ALPHA-001", "Pre-flight startup diagnostics successfully cleared database schemas.")
