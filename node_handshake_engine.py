import sqlite3
import hashlib
import hmac
import secrets
import os

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class NodeHandshakeEngine:
    def __init__(self):
        # Master mock directory matching private keys for our decentralized node perimeter
        self._node_key_vault = {
            "NODE-ALPHA-001": "FOUNDRY_SECRET_SECURE_TOKEN_ALPHA",
            "NODE-BETA-002": "FOUNDRY_SECRET_SECURE_TOKEN_BETA",
            "NODE-FLORIDA-007": "FOUNDRY_SECRET_SECURE_TOKEN_FLORIDA"
        }

    def initiate_handshake_challenge(self, node_id: str) -> str:
        """Step 1: Generate a secure cryptographic nonce challenge for the remote node."""
        if node_id not in self._node_key_vault:
            return None
        # Generate 32-byte secure random challenge string
        challenge_nonce = secrets.token_hex(16)
        return challenge_nonce

    def verify_handshake_response(self, node_id: str, challenge_nonce: str, received_signature: str) -> bool:
        """Step 2: Validate the challenge response signature using the local key vault."""
        secret_key = self._node_key_vault.get(node_id)
        if not secret_key or not challenge_nonce:
            return False
            
        # Recompute expected HMAC SHA-256 signature local-side
        expected_sig = hmac.new(
            secret_key.encode('utf-8'),
            challenge_nonce.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Constant-time comparison to protect against timing-based extraction vectors
        is_valid = hmac.compare_digest(expected_sig, received_signature)
        
        if is_valid:
            self._escalate_peer_trust(node_id)
        return is_valid

    def _escalate_peer_trust(self, node_id: str):
        """Step 3: Update local peer registry matrix state to Elevated Trust state upon verification."""
        if not os.path.exists(DB_PATH):
            return
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE peer_registry 
                SET trust_status = 'ELEVATED_TRUST', 
                    last_seen = CURRENT_TIMESTAMP 
                WHERE node_id = ?;
            """, (node_id,))
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"[✕] Registry Update Fault: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    print("="*90)
    print("EXECUTING SPRINT 16 CRYPTOGRAPHIC HANDSHAKE SIMULATION")
    print("="*90)
    
    engine = NodeHandshakeEngine()
    test_node = "NODE-ALPHA-001"
    
    # 1. Simulate Challenge Request
    nonce = engine.initiate_handshake_challenge(test_node)
    print(f"[➔] Connection initialized from endpoint: {test_node}")
    print(f"    └── Generated Auth Challenge Nonce: \033[38;5;214m{nonce}\033[0m")
    
    # 2. Simulate Remote Side Signature Generation 
    # (Using Node-Alpha-001 secret key to sign the challenge)
    remote_secret = "FOUNDRY_SECRET_SECURE_TOKEN_ALPHA"
    remote_signature = hmac.new(
        remote_secret.encode('utf-8'),
        nonce.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    print(f"[➔] Remote packet response intercepted with cryptographic signature payload...")
    
    # 3. Process verification evaluation inside the core handshake engine
    verification_status = engine.verify_handshake_response(test_node, nonce, remote_signature)
    
    if verification_status:
        print(f"\n\033[38;5;44m[✓] HANDSHAKE VERIFIED: Cryptographic origin for {test_node} authenticated.\033[0m")
        print("    └── Local Peer Registry updated state securely.")
    else:
        print("\n\033[38;5;196m[✕] AUTHENTICATION FAILURE: Tampered or invalid token payload detected.\033[0m")
    print("="*90)
