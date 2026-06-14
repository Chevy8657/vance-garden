import hashlib
import hmac
import secrets
import os
import datetime
from core_epoch_clock import CoreEpochClock

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class CoreHandshakeEngine:
    def __init__(self):
        self.clock = CoreEpochClock()
        # Simulated node-level master security secret for signing tokens
        self._shared_cluster_salt = b"FORTRESS_PROTOCOL_HIGH_ENTROPY_SALT_77"

    def generate_handshake_challenge(self, remote_node_id: str) -> dict:
        """
        Generates an epoch-bounded challenge payload that an incoming peer
        must cryptographically sign to prove identity authenticity.
        """
        current_epoch = self.clock.get_current_epoch()
        nonce = secrets.token_hex(16)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Build raw challenge target string
        challenge_payload = f"CHALLENGE:{remote_node_id}:{current_epoch}:{nonce}:{timestamp}"
        
        return {
            "target_node": remote_node_id,
            "bound_epoch": current_epoch,
            "nonce": nonce,
            "timestamp": timestamp,
            "challenge_string": challenge_payload
        }

    def simulate_remote_peer_signature(self, challenge_string: str, secure_key: str) -> str:
        """Simulates how a remote node signs the challenge string with its private key secret."""
        digest = hmac.new(
            secure_key.encode('utf-8'),
            msg=challenge_string.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return digest

    def verify_peer_handshake_response(self, challenge_meta: dict, provided_signature: str, secure_key: str) -> bool:
        """
        Validates the inbound challenge signature, enforces epoch window limits,
        and authorizes or denies node-level network interaction parameters.
        """
        print("="*90)
        print("EXECUTING PEER CRYPTOGRAPHIC CHALLENGE-RESPONSE HANDSHAKE")
        print("="*90)
        
        target_node = challenge_meta["target_node"]
        claimed_epoch = challenge_meta["bound_epoch"]
        current_epoch = self.clock.get_current_epoch()

        print(f"[➔] Inbound Request Identity : {target_node}")
        print(f" ❖ Checking Epoch Windows   : Claimed={claimed_epoch} | Active={current_epoch}")

        # Security Guardrail 1: Enforce current synchronization epoch window alignment
        if claimed_epoch != current_epoch:
            print("   └── \033[38;5;196m[HANDSHAKE DENIED]\033[0m: Challenge epoch has expired or belongs to a future matrix.")
            print("="*90)
            return False

        # Compute what the valid signature should look like using our internal verification logic
        expected_signature = hmac.new(
            secure_key.encode('utf-8'),
            msg=challenge_meta["challenge_string"].encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        print(f"[➔] Expected Signature Hex   : {expected_signature[:32]}...")
        print(f"[➔] Provided Remote Signature : {provided_signature[:32]}...")

        # Security Guardrail 2: Perform constant-time string comparison to prevent side-channel timing vectors
        if hmac.compare_digest(expected_signature, provided_signature):
            print(f"\n\033[38;5;44m[✓] HANDSHAKE SUCCESSFUL: Identity for {target_node} verified cryptographically.\033[0m")
            print("    └── Ingestion airlocks un-locked for sync packets.")
            print("="*90)
            return True
        else:
            print(f"\n\033[38;5;196m[🚨 SECURITY ALERT] CRYPTOGRAPHIC VERIFICATION FAILED!\033[0m")
            print(f"    └── Threat Warning: Unauthorized node attempting fake handshake signature manipulation.")
            print("="*90)
            return False

if __name__ == "__main__":
    engine = CoreHandshakeEngine()
    
    # Define verification key parameters for testing
    VALID_PEER_KEY = "SECRET_TOKEN_ALPHA_VANCE_001"
    MALICIOUS_PEER_KEY = "COUNTERFEIT_MALICIOUS_TOKEN_999"

    # --- SIMULATION 1: TRUSTED HANDSHAKE VERIFICATION PASS ---
    # 1. Local appliance issues the challenge to NODE-ALPHA-001
    challenge_1 = engine.generate_handshake_challenge("NODE-ALPHA-001")
    
    # 2. Trusted node signs the challenge string properly
    valid_sig = engine.simulate_remote_peer_signature(challenge_1["challenge_string"], VALID_PEER_KEY)
    
    # 3. Local appliance runs authentication audit
    engine.verify_peer_handshake_response(challenge_1, valid_sig, VALID_PEER_KEY)

    print("\n")

    # --- SIMULATION 2: TAMPERED/MALICIOUS HANDSHAKE REJECTION ---
    # 1. Local appliance issues a challenge to an unverified connection profile
    challenge_2 = engine.generate_handshake_challenge("NODE-UNKNOWN-999")
    
    # 2. Rogue element attempts to spoof authentication with an invalid signature pattern
    invalid_sig = engine.simulate_remote_peer_signature(challenge_2["challenge_string"], MALICIOUS_PEER_KEY)
    
    # 3. Local appliance audits the threat vector and drops execution parameters instantly
    engine.verify_peer_handshake_response(challenge_2, invalid_sig, VALID_PEER_KEY)
