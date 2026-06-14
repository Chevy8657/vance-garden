import sqlite3

def initialize_sovereign_node():
    DB_PATH = "district.db"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS district_ledger (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        district_identity_key TEXT NOT NULL,
        node_source TEXT NOT NULL,
        action_type TEXT NOT NULL,
        process_latency_seconds REAL,
        payload_hash TEXT NOT NULL,
        is_verified INTEGER DEFAULT 1
    );
    """)
    
    conn.commit()
    conn.close()
    print("💎 Sovereign database 'district.db' initialized with ironclad schema.")

if __name__ == "__main__":
    initialize_sovereign_node()
