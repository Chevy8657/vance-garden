import sqlite3
import hashlib
import json
import os

DB_PATH = '/home/rick/pet_alpha/telemetry.db'
MANIFEST_PATH = '/home/rick/pet_alpha/state_manifest.sig'

class CoreChecksumAuditor:
    def __init__(self):
        pass

    def calculate_active_state_hash(self) -> str:
        """
        Queries active tables, standardizes row ordering, and calculates a 
        unified SHA-256 hash representing the complete local database state.
        """
        if not os.path.exists(DB_PATH):
            return None

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        state_buffer = []

        # 1. Digest Active System Configurations (Ordered explicitly)
        try:
            cursor.execute("SELECT config_key, config_value FROM active_system_config ORDER BY config_key ASC;")
            configs = cursor.fetchall()
            for key, val in configs:
                state_buffer.append(f"CONFIG:{key}:{val}")
        except sqlite3.OperationalError:
            pass

        # 2. Digest Peer Identity Matrix Statuses (Ordered explicitly)
        try:
            cursor.execute("SELECT node_id, trust_status FROM peer_registry ORDER BY node_id ASC;")
            peers = cursor.fetchall()
            for node_id, status in peers:
                state_buffer.append(f"PEER:{node_id}:{status}")
        except sqlite3.OperationalError:
            pass

        conn.close()

        # Build raw string baseline and calculate high-entropy signature
        unified_string = "|".join(state_buffer)
        return hashlib.sha256(unified_string.encode('utf-8')).hexdigest()

    def seal_initial_manifest_baseline(self) -> str:
        """Saves the current database checksum as the authorized baseline signature."""
        current_hash = self.calculate_active_state_hash()
        if not current_hash:
            return None
            
        with open(MANIFEST_PATH, 'w') as f:
            f.write(current_hash)
        return current_hash

    def execute_integrity_audit(self) -> bool:
        """
        Compares live runtime table hashes against the recorded manifest baseline.
        Returns True if perfectly matching, False if unauthorized data changes occur.
        """
        print("="*90)
        print("LAUNCHING CRYPTOGRAPHIC PERSISTENCE LAYER INTEGRITY AUDIT")
        print("="*90)

        if not os.path.exists(MANIFEST_PATH):
            print("[i] Notice: Initial configuration baseline missing. Sealing active state manifest...")
            self.seal_initial_manifest_baseline()

        with open(MANIFEST_PATH, 'r') as f:
            baseline_hash = f.read().strip()

        runtime_hash = self.calculate_active_state_hash()

        print(f"[➔] Authorized State Baseline : {baseline_hash[:32]}...")
        print(f"[➔] Live Runtime State Digested: {runtime_hash[:32]}...")

        if runtime_hash == baseline_hash:
            print(f"\n\033[38;5;44m[✓] STATE INTEGRITY VERIFIED: Zero unauthorized modifications caught.\033[0m")
            print("="*90)
            return True
        else:
            print(f"\n\033[38;5;196m[🚨 CRITICAL FAULT] STATE INTEGRITY VIOLATION DETECTED!\033[0m")
            print("    └── Threat Vector: SQLite database files altered outside verified pipelines.")
            print("="*90)
            return False

if __name__ == "__main__":
    auditor = CoreChecksumAuditor()
    # Execute verification sweep
    auditor.execute_integrity_audit()
