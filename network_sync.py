import sqlite3
import json
import datetime
import hashlib
import uuid

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class SovereignSyncEngine:
    @staticmethod
    def generate_packet(source_node, target_node, payload_type, payload_data):
        packet_id = f"PKT-{uuid.uuid4().hex[:8].upper()}"
        created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        payload_str = json.dumps(payload_data, sort_keys=True)
        artifact_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        
        mock_signature = hashlib.sha256(f"{packet_id}:{artifact_hash}:LOCAL_KEY".encode()).hexdigest()[:32]
        
        packet = {
            "packet_id": packet_id,
            "source_node_id": source_node,
            "target_node_id": target_node,
            "created_at": created_at,
            "payload_type": payload_type.upper(),
            "artifact_hash": artifact_hash,
            "signature": mock_signature,
            "payload": payload_data
        }
        return packet

    def enqueue_outbound(self, target_node, payload_type, payload_data):
        packet = self.generate_packet("NODE-ALPHA-001", target_node, payload_type, payload_data)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sync_outbound_queue (packet_id, target_node_id, payload_json, status, created_at)
            VALUES (?, ?, ?, 'PENDING', ?);
        """, (packet['packet_id'], target_node, json.dumps(packet), packet['created_at']))
        
        conn.commit()
        conn.close()
        print(f"\033[38;5;44m  [📤 OUTBOUND ENQUEUED] Packet {packet['packet_id']} sealed for {target_node}.\033[0m")
        return packet['packet_id']

    def stage_inbound_packet(self, raw_packet_json):
        try:
            packet = json.loads(raw_packet_json)
            packet_id = packet.get('packet_id')
            source_node = packet.get('source_node_id')
            received_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sync_inbound_staging (packet_id, source_node_id, payload_json, received_at, validation_status)
                VALUES (?, ?, ?, ?, 'UNVERIFIED');
            """, (packet_id, source_node, raw_packet_json, received_at))
            conn.commit()
            conn.close()
            print(f"  [📥 INBOUND STAGED] Packet {packet_id} isolated in security staging.")
            return packet_id
        except Exception as e:
            print(f"  \033[38;5;196m[!] FAIL: Network package dropped due to raw structural deformation: {e}\033[0m")
            return None

    def adjudicate_staging_gate(self, packet_id):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sync_inbound_staging WHERE packet_id = ?;", (packet_id,))
        staged_row = cursor.fetchone()
        
        if not staged_row:
            conn.close()
            return "REJECTED_NOT_FOUND"
            
        packet = json.loads(staged_row['payload_json'])
        payload = packet.get('payload')
        claimed_hash = packet.get('artifact_hash')
        
        payload_str = json.dumps(payload, sort_keys=True)
        actual_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        
        exchange_id = f"EXCH-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        if actual_hash != claimed_hash:
            outcome = "REJECTED_HASH_MUTATION"
            cursor.execute("""
                UPDATE sync_inbound_staging 
                SET validation_status = 'REJECTED', failure_reason = 'Cryptographic hash mismatch' 
                WHERE packet_id = ?;
            """, (packet_id,))
            print(f"\033[38;5;196m  [🛑 GATE REJECTION] Packet {packet_id} FAILED integrity audit! Corrupted data detected.\033[0m")
        else:
            outcome = "ACCEPTED_TRUSTED_HISTORY"
            cursor.execute("""
                UPDATE sync_inbound_staging 
                SET validation_status = 'ACCEPTED' 
                WHERE packet_id = ?;
            """, (packet_id,))
            print(f"\033[38;5;46m  [✓] GATE ACCEPTANCE: Packet {packet_id} verified. Committing entry to localized ledger.\033[0m")
            
        cursor.execute("""
            INSERT INTO sync_exchange_ledger (exchange_id, packet_id, direction, node_id, timestamp_utc, outcome)
            VALUES (?, ?, 'INBOUND', ?, ?, ?);
        """, (exchange_id, packet_id, packet.get('source_node_id'), timestamp, outcome))
        
        conn.commit()
        conn.close()
        return outcome

if __name__ == "__main__":
    engine = SovereignSyncEngine()
    print("=" * 90)
    print("Executing Patched Sprint 5 Pipeline Verification Test")
    print("=" * 90)
    
    # Test Path 1: Pure Unaltered Outbound to Inbound Flow
    mock_payload = {"cohort_id": "NEVADA_RURAL_04", "cpi_friction_index": 4.2}
    pkt_id = engine.enqueue_outbound("NODE-BETA-002", "TELEMETRY_EXCHANGE", mock_payload)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT payload_json FROM sync_outbound_queue WHERE packet_id = ?;", (pkt_id,))
    wire_data = cursor.fetchone()[0]
    conn.close()
    
    staged_id = engine.stage_inbound_packet(wire_data)
    engine.adjudicate_staging_gate(staged_id)
    
    # Test Path 2: Malicious Tampering Simulation (Altering payload AND modifying ID to bypass replay protection)
    print("\n[➔] Simulating network level contamination injection (Bypassing Replay)...")
    tampered_packet_dict = json.loads(wire_data)
    tampered_packet_dict['packet_id'] = f"PKT-{uuid.uuid4().hex[:8].upper()}"  # New ID to slip past unique filter
    tampered_packet_dict['payload']['cpi_friction_index'] = 999.9              # Modified payload
    tampered_wire_data = json.dumps(tampered_packet_dict)
    
    tampered_staged_id = engine.stage_inbound_packet(tampered_wire_data)
    engine.adjudicate_staging_gate(tampered_staged_id)
    print("=" * 90)
