import requests
import random
import time

URL = "http://127.0.0.1:3000/v1/telemetry/ingest"
HEADERS = {"x-district-key": "VANCE_CORE_ALPHA_SECURE_KEY_2026"}

# 1. Map out the 8 Regional Office Branches
offices = [
    "OFFICE_01_SUMMERLIN", "OFFICE_02_HENDERSON", "OFFICE_03_RENO", 
    "OFFICE_04_AUSTIN", "OFFICE_05_DALLAS", "OFFICE_06_MIAMI", 
    "OFFICE_07_ORLANDO", "OFFICE_08_TAMPA"
]

actions = ["GOVERNED_DRAFTING", "COMPLIANCE_CHECK", "INTAKE_TRIGGER"]

def run_enterprise_simulation():
    print("🏛️  PET ENTERPRISE SIMULATOR: 8 OFFICES // 400 AGENTS")
    print("📡 Initializing heavy telemetry ingestion stream down to Mother Node...\n")
    
    # Simulate a massive, rapid batch of 60 operational hits across the branches
    for i in range(60):
        office = random.choice(offices)
        # Randomly assign to one of the 400 agent slots across the enterprise footprint
        agent_id = f"AGENT_{random.randint(1, 400):03d}"
        action = random.choice(actions)
        latency = round(random.uniform(0.008, 0.045), 4)
        
        # Structure the node source to capture both the regional office branch and the agent unit
        node_source_identity = f"{office}//{agent_id}"
        
        payload = {
            "node_source": node_source_identity,
            "action_type": action,
            "process_latency_seconds": latency,
            "raw_payload_string": f"Enterprise ledger tracking sequence line {i} for {node_source_identity}."
        }
        
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            print(f"📡 [INGEST] {office} -> {agent_id} -> {action} ({latency}s)")
        else:
            print(f"❌ Connection interrupted for {node_source_identity}")
            
        # Micro-pause to maintain high-velocity ingestion without crashing local terminal prints
        time.sleep(0.02)

    print("\n🏁 Heavy enterprise batch injection complete. Roster timeline synchronized.")

if __name__ == "__main__":
    run_enterprise_simulation()
