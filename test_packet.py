import requests
import json

URL = "http://127.0.0.1:3000/v1/telemetry/ingest"
HEADERS = {"x-district-key": "VANCE_CORE_ALPHA_SECURE_KEY_2026"}
DATA = {
    "node_source": "CHILD_NODE_01",
    "action_type": "INTAKE_TRIGGER",
    "process_latency_seconds": 0.017,
    "raw_payload_string": "Lead intake event: User signed up for 30-day assessment."
}

def fire_test_packet():
    print("📡 Launching secure telemetry packet to Parent Node...")
    try:
        response = requests.post(URL, headers=HEADERS, json=DATA)
        print(f"🔒 Server Response Code: {response.status_code}")
        print("📦 Packet Ledger Commit Proof:")
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.ConnectionError:
        print("❌ Connection Refused. Is your FastAPI server running on Port 3000?")

if __name__ == "__main__":
    fire_test_packet()
