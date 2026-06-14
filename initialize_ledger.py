import sqlite3

def build_sovereign_tables():
    conn = sqlite3.connect("/home/rick/pet_alpha/telemetry.db")
    cursor = conn.cursor()
    
    print("[*] Initializing sovereign database infrastructure...")
    
    # 1. Node Registry Table for Anniversary Tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS node_registry (
        node_id TEXT PRIMARY KEY,
        owner_name TEXT NOT NULL,
        tier TEXT NOT NULL,
        activation_date TEXT NOT NULL,
        status TEXT DEFAULT 'active'
    )
    """)
    
    # 2. Lead Registry Table for Target Outreach
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lead_registry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        broker_name TEXT NOT NULL,
        business_name TEXT,
        gatekeeper TEXT,
        physical_anchor TEXT,
        email_channel TEXT,
        real_scale TEXT,
        outreach_track TEXT,
        tactical_vulnerability TEXT,
        status TEXT DEFAULT 'Staging'
    )
    """)
    
    conn.commit()
    print("[✓] Tables established. Database locked and local-first.")
    conn.close()

if __name__ == "__main__":
    build_sovereign_tables()
