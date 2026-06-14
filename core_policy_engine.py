import json
import sqlite3

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class CorePolicyEngine:
    def __init__(self):
        # Explicit white-list of valid business operational hooks
        self.approved_logic_hooks = ["10-to-Zero hook"]

    def evaluate_latest_ledger_entries(self) -> list:
        """
        Scans the transaction ledger for un-evaluated records, applies business
        rules, and mutates active system configurations upon validation clearance.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure the active configuration state table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_system_config (
                config_key TEXT PRIMARY KEY,
                config_value TEXT,
                last_mutation_timestamp TEXT
            );
        ''')

        # Extract committed transactions from the ledger
        cursor.execute("SELECT packet_id, body, committed_at FROM transaction_ledger;")
        records = cursor.fetchall()

        evaluation_log = []

        for packet_id, body_str, committed_at in records:
            try:
                body = json.loads(body_str)
                raw_ref = body.get("raw_payload_reference", {})
                reduction_hook = raw_ref.get("agreed_reduction_logic")

                # Policy Boundary Check
                if reduction_hook in self.approved_logic_hooks:
                    # Perform deterministic mutation of active system parameters
                    cursor.execute('''
                        INSERT INTO active_system_config (config_key, config_value, last_mutation_timestamp)
                        VALUES ('REFERRAL_FEE_LOGIC', ?, ?)
                        ON CONFLICT(config_key) DO UPDATE SET config_value = ?, last_mutation_timestamp = ?;
                    ''', (reduction_hook, committed_at, reduction_hook, committed_at))
                    
                    evaluation_log.append(f"[POLICY MATCH] Packet {packet_id} approved: Applied '{reduction_hook}' to system config.")
                else:
                    evaluation_log.append(f"[POLICY SKIP] Packet {packet_id}: No matching active rule target found.")

            except Exception as e:
                evaluation_log.append(f"[POLICY ERROR] Failed to evaluate packet {packet_id}: {e}")

        conn.commit()
        conn.close()
        return evaluation_log

if __name__ == "__main__":
    engine = CorePolicyEngine()
    results = engine.evaluate_latest_ledger_entries()
    print("\n".join(results))
