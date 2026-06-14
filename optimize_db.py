#!/usr/bin/env python3
import sqlite3

DB_FILE = "district.db"

def optimize_ledger():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("🛠️  Optimizing database architecture for multi-node scaling...")
        
        # Create an index on node_id and timestamp to keep queries lightning fast
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_node_timestamp 
            ON telemetry_ledger (node_id, timestamp DESC);
        """)
        
        # Turn on Write-Ahead Logging (WAL) mode to handle concurrent multi-user writes safely
        cursor.execute("PRAGMA journal_mode=WAL;")
        wal_result = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        print(f"✨ Optimization complete. Database mode changed to: {wal_result.upper()}")
        print("🚀 Ready to support concurrent multi-tenant data pipelines safely.")
        
    except Exception as e:
        print(f"❌ Optimization failed: {str(e)}")

if __name__ == "__main__":
    optimize_ledger()

