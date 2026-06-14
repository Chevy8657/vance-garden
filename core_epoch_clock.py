import sqlite3
import os
import datetime

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class CoreEpochClock:
    def __init__(self):
        self._initialize_epoch_table()

    def _initialize_epoch_table(self):
        """Ensures the core system configuration table supports epoch tracking."""
        if not os.path.exists(DB_PATH):
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_system_config (
                config_key TEXT PRIMARY KEY,
                config_value TEXT,
                last_mutation_timestamp TEXT
            );
        """)
        # Seed initial epoch sequence at 0 if missing
        cursor.execute("""
            INSERT INTO active_system_config (config_key, config_value, last_mutation_timestamp)
            VALUES ('CURRENT_EPOCH_SEQUENCE', '0', datetime('now'))
            ON CONFLICT(config_key) DO NOTHING;
        """)
        conn.commit()
        conn.close()

    def get_current_epoch(self) -> int:
        """Retrieves the current synchronized network epoch index."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT config_value FROM active_system_config WHERE config_key = 'CURRENT_EPOCH_SEQUENCE';")
        row = cursor.fetchone()
        conn.close()
        return int(row[0]) if row else 0

    def advance_network_epoch(self) -> int:
        """Atomically bumps the monotonic network epoch sequence counter by 1."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        try:
            cursor.execute("BEGIN TRANSACTION;")
            current = self.get_current_epoch()
            next_epoch = current + 1
            
            cursor.execute("""
                UPDATE active_system_config 
                SET config_value = ?, last_mutation_timestamp = ?
                WHERE config_key = 'CURRENT_EPOCH_SEQUENCE';
            """, (str(next_epoch), timestamp))
            
            conn.commit()
            print(f"\033[38;5;44m[✓] MONOTONIC CLOCK ADVANCED: Network Epoch bumped to {next_epoch}\033[0m")
            return next_epoch
        except sqlite3.Error as e:
            conn.rollback()
            print(f"[✕] Clock Fault: Unable to advance sequence: {e}")
            return self.get_current_epoch()
        finally:
            conn.close()

    def validate_incoming_packet_epoch(self, packet_id: str, claimed_epoch: int) -> bool:
        """Verifies if an inbound message sits strictly within the node's active sync window."""
        current_epoch = self.get_current_epoch()
        print(f" ❖ Sync Audit: Packet {packet_id} | Claimed Epoch: {claimed_epoch} | Node Epoch: {current_epoch}")
        
        if claimed_epoch == current_epoch:
            print("   └── \033[38;5;44m[PASS]\033[0m Temporal window aligned. Processing cleared.")
            return True
        elif claimed_epoch < current_epoch:
            print("   └── \033[38;5;196m[REJECT]\033[0m Stale data packet detected. Dropping to prevent sequence corruption.")
            return False
        else:
            print("   └── \033[38;5;214m[HOLD]\033[0m Future epoch signature identified. Staging packet for structural resync.")
            return False

if __name__ == "__main__":
    print("="*90)
    print("INITIALIZING MONOTONIC EPOCH CLOCK & SYNC WINDOW AUDIT")
    print("="*90)
    
    clock = CoreEpochClock()
    
    # 1. Inspect initial baseline epoch state
    print(f"[➔] Initialized Node State: Current Epoch = {clock.get_current_epoch()}\n")
    
    # 2. Simulate transaction sequencing verification passes
    clock.validate_incoming_packet_epoch("PKT-TX-201", claimed_epoch=0)
    clock.validate_incoming_packet_epoch("PKT-TX-202", claimed_epoch=0)
    
    # 3. Simulate a cluster commit advancing the network time horizon
    print("")
    clock.advance_network_epoch()
    print("")
    
    # 4. Re-evaluate windows against the updated epoch state
    # This proves that old packets are now blocked to preserve linear tracking integrity
    clock.validate_incoming_packet_epoch("PKT-TX-203", claimed_epoch=0)
    clock.validate_incoming_packet_epoch("PKT-TX-204", claimed_epoch=1)
    print("="*90)
