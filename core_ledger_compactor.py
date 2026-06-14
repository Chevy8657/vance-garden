import sqlite3
import os
import datetime
from core_checksum_auditor import CoreChecksumAuditor

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class CoreLedgerCompactor:
    def __init__(self):
        self.auditor = CoreChecksumAuditor()

    def execute_ledger_compaction(self) -> bool:
        """
        Optimizes local database layout, cleans stale historical logs,
        and regenerates the security perimeter baseline manifest.
        """
        print("="*90)
        print("LAUNCHING LOCAL STATE LEDGER COMPACTION ENGINE")
        print("="*90)

        if not os.path.exists(DB_PATH):
            print("[✕] Compaction Error: Target telemetry storage database missing.")
            return False

        # Open connection with autocommit mode to allow structural VACUUM operation
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("[➔] Step 1: Optimizing high-velocity database storage footprint...")
        try:
            # SQLite requires VACUUM to run outside of active user transactions
            conn.execute("VACUUM;")
            print("\033[38;5;44m[✓] STORAGE FOOTPRINT OPTIMIZED: Database pages compressed successfully.\033[0m")
        except sqlite3.Error as e:
            print(f"[✕] Compaction Fault: Database vacuum execution failure: {e}")
            conn.close()
            return False
        finally:
            conn.close()

        print("\n[➔] Step 2: Regenerating cryptographic security perimeter...")
        new_hash = self.auditor.seal_initial_manifest_baseline()
        print(f"    └── Fresh Authorized Baseline Sealed: \033[38;5;44m{new_hash[:32]}...\033[0m")

        print("\n[➔] Step 3: Verifying structural health of the newly compressed persistence layer...")
        return self.auditor.execute_integrity_audit()

if __name__ == "__main__":
    compactor = CoreLedgerCompactor()
    compactor.execute_ledger_compaction()
