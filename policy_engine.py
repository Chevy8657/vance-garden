import json
import sqlite3
from offline_gap_detector import calculate_peer_drift

DB_PATH = '/home/rick/pet_alpha/telemetry.db'
POLICY_PATH = '/home/rick/pet_alpha/policy_config.json'

class DeterministicPolicyEngine:
    def __init__(self):
        with open(POLICY_PATH, 'r') as f:
            self.config = json.load(f)['policies']

    def evaluate_peer_reputation(self, node_id):
        """
        Memory (Ledger) -> Judgment (Policy) -> Action Determination
        """
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Gather behavioral telemetry from append-only ledger
        cursor.execute("""
            SELECT outcome_category, COUNT(*) as cnt 
            FROM peer_sync_ledger 
            WHERE node_id = ? 
            GROUP BY outcome_category;
        """, (node_id,))
        
        tallies = {row['outcome_category']: row['cnt'] for row in cursor.fetchall()}
        conn.close()
        
        # Gather temporal drift metrics
        drift_condition, drift_hours = calculate_peer_drift(node_id)
        
        # 1. Evaluate Zero-Tolerance Mutation Policy
        if tallies.get('HASH_MUTATION_BLOCKED', 0) >= self.config['MUTATION_LIMIT']['threshold']:
            return {
                "action": self.config['MUTATION_LIMIT']['consequence'],
                "reason": self.config['MUTATION_LIMIT']['reason']
            }
            
        # 2. Evaluate Replay Attack Threshold Policy
        if tallies.get('REPLAY_BLOCKED', 0) >= self.config['REPLAY_LIMIT']['threshold']:
            return {
                "action": self.config['REPLAY_LIMIT']['consequence'],
                "reason": self.config['REPLAY_LIMIT']['reason']
            }
            
        # 3. Evaluate Chronological Drift Policy
        if drift_hours >= self.config['DRIFT_LIMIT']['threshold']:
            return {
                "action": self.config['DRIFT_LIMIT']['consequence'],
                "reason": self.config['DRIFT_LIMIT']['reason']
            }
            
        # 4. Evaluate Promotion Policy
        if tallies.get('ACCEPTED', 0) >= self.config['PROMOTION_TIER']['threshold']:
            return {
                "action": self.config['PROMOTION_TIER']['consequence'],
                "reason": self.config['PROMOTION_TIER']['reason']
            }
            
        return {"action": "MAINTAIN_STATUS", "reason": "Peer behavior within normal baseline standard."}
