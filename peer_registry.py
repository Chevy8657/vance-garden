import sqlite3
import datetime
from policy_engine import DeterministicPolicyEngine

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class PeerImmuneSystem:
    def __init__(self):
        self.db_path = DB_PATH

    def update_peer_heartbeat(self, node_id, packet_id=None, accepted_hash=None):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO peer_registry (node_id, first_seen, last_seen, trust_status)
            VALUES (?, ?, ?, 'TRUSTED')
            ON CONFLICT(node_id) DO UPDATE SET last_seen = ?;
        """, (node_id, now, now, now))
        
        if accepted_hash:
            cursor.execute("""
                UPDATE peer_registry 
                SET last_packet_id = ?, last_accepted_hash = ? 
                WHERE node_id = ?;
            """, (packet_id, accepted_hash, node_id))
        conn.commit()
        conn.close()
        
        self.enforce_policy(node_id)

    def append_ledger_entry(self, node_id, direction, packet_id, outcome_category):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO peer_sync_ledger (node_id, direction, packet_id, outcome_category, timestamp_utc)
            VALUES (?, ?, ?, ?, ?);
        """, (node_id, direction.upper(), packet_id, outcome_category.upper(), now))
        conn.commit()
        conn.close()
        
        self.enforce_policy(node_id)

    def enforce_policy(self, node_id):
        """
        Adjudicates behavior based on policy config. 
        Only prints/updates if an actual status transition occurs.
        """
        # 1. Check existing status from the registry
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT trust_status FROM peer_registry WHERE node_id = ?;", (node_id,))
        row = cursor.fetchone()
        current_status = row[0] if row else "TRUSTED"
        conn.close()

        # 2. Evaluate current ledger data against rules
        engine = DeterministicPolicyEngine()
        verdict = engine.evaluate_peer_reputation(node_id)
        target_action = verdict['action']

        # 3. Only act if the peer is transitioning states
        if target_action != "MAINTAIN_STATUS" and target_action != current_status:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE peer_registry 
                SET trust_status = ? 
                WHERE node_id = ?;
            """, (target_action, node_id))
            conn.commit()
            conn.close()
            
            COLOR = "\033[38;5;196m" if "SUSPENDED" in target_action else "\033[38;5;214m" if "QUARANTINED" in target_action else "\033[38;5;44m"
            print(f"  {COLOR}[⚖️  POLICY ENGINE TRANSITION] Node {node_id} shifted [{current_status}] -> [{target_action}]. Reason: {verdict['reason']}\033[0m")
