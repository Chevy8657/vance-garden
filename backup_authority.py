#!/usr/bin/env python3
import sqlite3
import os
import time
from datetime import datetime

DB_FILE = "district.db"
BACKUP_DIR = "backups"
BACKUP_INTERVAL = 3600  # Run every hour (3600 seconds)
MAX_BACKUPS = 24        # Keep rolling 24 hours of local history

def execute_hardened_backup():
    """Safely replicates the live database without locking active transactions."""
    if not os.path.exists(DB_FILE):
        print(f"⚠️  [Backup] Primary ledger '{DB_FILE}' not found yet. Skipping cycle.")
        return

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"district_backup_{timestamp}.db")

    try:
        # Connect to the live ledger
        src_conn = sqlite3.connect(DB_FILE)
        
        # Open a connection to the new backup destination file
        dst_conn = sqlite3.connect(backup_file)
        
        # Use SQLite's native online backup API to copy pages without locking the parent authority
        with dst_conn:
            src_conn.backup(dst_conn)
            
        dst_conn.close()
        src_conn.close()
        
        print(f"💾 [Backup] Sovereign Ledger replicated successfully: {backup_file}")
        
        # Enforce the rolling historical retention limit
        clean_old_backups()
        
    except Exception as e:
        print(f"❌ [Backup Error] Replication failed: {str(e)}")

def clean_old_backups():
    """Prunes older files to maintain a strict, local storage envelope."""
    try:
        files = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
        # Sort files oldest to newest
        files.sort(key=os.path.getmtime)
        
        while len(files) > MAX_BACKUPS:
            oldest_file = files.pop(0)
            os.remove(oldest_file)
            print(f"🗑️  [Backup] Pruned historical archive: {oldest_file}")
    except Exception as e:
        print(f"⚠️  [Backup] Error cleaning historical archives: {str(e)}")

if __name__ == "__main__":
    print(f"🛡️  V.A.N.C.E. Backup Daemon initialized. Interval: {BACKUP_INTERVAL}s | Retention: {MAX_BACKUPS} slots.")
    try:
        while True:
            execute_hardened_backup()
            time.sleep(BACKUP_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Backup Daemon safely halted.")
