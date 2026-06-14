import json
import hashlib
import hmac
import sqlite3
import datetime

DB_PATH = '/home/rick/pet_alpha/telemetry.db'
CORE_SECRET = "FOUNDRY_SECRET_SECURE_TOKEN_2026"

def verify_and_ingest_packet(sealed_envelope: dict) -> tuple:
    """
    Core Ingestion Sink: Processes incoming sterile adapter envelopes.
    Verifies signature integrity, prevents replays, and commits records to state.
    """
    packet_id = sealed_envelope.get("packet_id")
    origin_node = sealed_envelope.get("origin_node")
    serialized_body = sealed_envelope.get("serialized_body")
    provided_signature = sealed_envelope.get("transit_signature")

    # 1. Cryptographic Line Defense
    expected_sig = hmac.new(
        CORE_SECRET.encode('utf-8'),
        serialized_body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, provided_signature):
        return "REJECTED_SIGNATURE_MISMATCH", "Packet signature verification failed. Payload untrusted."

    # 2. Open State Ledger Connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 3. Anti-Replay Guard Check
    # Ensure tables exist for audit trail if missing
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_ledger (
            packet_id TEXT PRIMARY KEY,
            origin_node TEXT,
            payload_type TEXT,
            committed_at TEXT,
            body TEXT
        );
    ''')
    
    cursor.execute("SELECT 1 FROM transaction_ledger WHERE packet_id = ?;", (packet_id,))
    if cursor.fetchone():
        conn.close()
        return "REJECTED_REPLAY_ATTACK", f"Packet ID [{packet_id}] already exists in sync ledger."

    # 4. Commit Package to Immutable Audit Trail
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute('''
        INSERT INTO transaction_ledger (packet_id, origin_node, payload_type, committed_at, body)
        VALUES (?, ?, ?, ?, ?);
    ''', (packet_id, origin_node, sealed_envelope.get("payload_type"), now, serialized_body))

    # 5. Update Operational Peer Records
    cursor.execute('''
        UPDATE peer_registry 
        SET last_seen = ? 
        WHERE node_id = ?;
    ''', (now, origin_node))

    conn.commit()
    conn.close()

    return "COMMITTED", f"Successfully ingested {sealed_envelope.get('payload_type')} into core ledger."
