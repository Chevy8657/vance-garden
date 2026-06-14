import sqlite3
import json
import os
import datetime

DB_PATH = '/home/rick/pet_alpha/telemetry.db'
ARCHIVE_PATH = '/home/rick/pet_alpha/ledger_archive_history.json'

class CoreLedgerArchiver:
    def __init__(self, max_retained_rows=10):
        self.max_retained_rows = max_retained_rows

    def execute_rotation_cycle(self) -> int:
        """
        Pulls excess committed rows from the live database ledger, transfers them 
        to cold storage, and clean-vacuums the active database.
        """
        if not os.path.exists(DB_PATH):
            return 0

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get total row count to determine if pruning is necessary
        cursor.execute("SELECT COUNT(*) FROM transaction_ledger;")
        total_rows = cursor.fetchone()[0]

        if total_rows <= self.max_retained_rows:
            conn.close()
            return 0

        # Identify target rows exceeding the retention limit
        excess_count = total_rows - self.max_retained_rows
        cursor.execute(f"SELECT packet_id, origin_node, routing_context, payload_type, body, committed_at FROM transaction_ledger ORDER BY committed_at ASC LIMIT ?;", (excess_count,))
        rows_to_archive = cursor.fetchall()

        archived_records = []
        packet_ids_to_purge = []

        for row in rows_to_archive:
            record = {
                "packet_id": row[0],
                "origin_node": row[1],
                "routing_context": row[2],
                "payload_type": row[3],
                "body": row[4],
                "committed_at": row[5],
                "archived_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
            archived_records.append(record)
            packet_ids_to_purge.append(row[0])

        # Read existing cold storage archive
        existing_archive = []
        if os.path.exists(ARCHIVE_PATH):
            try:
                with open(ARCHIVE_PATH, 'r') as f:
                    existing_archive = json.load(f)
            except json.JSONDecodeError:
                existing_archive = []

        # Merge and commit back to cold storage file
        existing_archive.extend(archived_records)
        with open(ARCHIVE_PATH, 'w') as f:
            json.dump(existing_archive, f, indent=4)

        # Atomic database purge execution
        cursor.executemany("DELETE FROM transaction_ledger WHERE packet_id = ?;", [(pid,) for pid in packet_ids_to_purge])
        conn.commit()
        
        # Reclaim empty disk pages
        cursor.execute("VACUUM;")
        conn.close()

        return len(packet_ids_to_purge)

if __name__ == "__main__":
    # Aggressive limit of 0 for testing to force rotation immediately on existing rows
    archiver = CoreLedgerArchiver(max_retained_rows=0)
    purged = archiver.execute_rotation_cycle()
    print(f"\n===========================================================================")
    print(f"[✓] CORE LEDGER ROTATION CYCLE COMPLETE")
    print(f"    └── Successfully moved {purged} rows to cold storage archive.")
    print(f"===========================================================================")
