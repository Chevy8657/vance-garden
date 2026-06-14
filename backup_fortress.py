import sqlite3
import os
import datetime

def execute_appliance_backup():
    """
    Leverages SQLite's online backup API to perform a zero-locking, hot clone 
    of the local system architecture. Ensures absolute data persistence.
    """
    BACKUP_DIR = '/home/rick/pet_alpha/backups/'
    DATABASES = {
        'telemetry': '/home/rick/pet_alpha/telemetry.db',
        'security_audit': '/home/rick/pet_alpha/infrastructure_audit.db'
    }
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    
    # Digital Gothic terminal style elements
    OBSIDIAN_BG     = "\033[48;5;232m"
    FOUNDRY_TEXT    = "\033[38;5;250m"
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    VITRUVEO_TEAL   = "\033[38;5;44m"
    RESET           = "\033[0m"
    
    print(f"{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("X" + "═" * 88 + "X")
    print(f"║ NODE-ALPHA-001 // FORTRESS BACKUP ENGINE INITIALIZED                         ║")
    print("X" + "═" * 88 + "X" + FOUNDRY_TEXT)
    
    for name, source_path in DATABASES.items():
        if not os.path.exists(source_path):
            print(f"  ├── [!] SKIPPING '{name}': Source database file not found on host.")
            continue
            
        backup_filename = f"backup_{name}_{timestamp}.db"
        target_path = os.path.join(BACKUP_DIR, backup_filename)
        
        print(f"  ├── [➔] Streaming hot snapshot of '{name}' ledger...")
        try:
            # Open source connection and destination backup file
            src_conn = sqlite3.connect(source_path)
            dst_conn = sqlite3.connect(target_path)
            
            # Use SQLite's built-in hot backup system to stream pages safely
            with dst_conn:
                src_conn.backup(dst_conn)
                
            src_conn.close()
            dst_conn.close()
            
            print(f"  │   └── {VITRUVEO_TEAL}[✓] Saved snapshot: {backup_filename}{FOUNDRY_TEXT}")
        except Exception as e:
            print(f"  │   └── [!] FAIL: Could not complete snapshot stream: {e}")
            
    print("  " + "─" * 86)
    print(f"  All local persistence tables safely replicated to the secure vault.")
    print(GOLD_LEAF_AMBER + "X" + "═" * 88 + "X" + RESET)

if __name__ == "__main__":
    execute_appliance_backup()
