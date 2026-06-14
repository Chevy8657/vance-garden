#!/usr/bin/env python3
import http.client
import json
import time
import os
import uuid
import sys
import hashlib

PARENT_HOST = "127.0.0.1"
PARENT_PORT = 3000
TELEMETRY_INTERVAL = 5
NODE_ID = str(uuid.getnode())
SPOOL_FILE = "telemetry_spool.json"
SHARED_SECRET = "farm_bureau_national_compliance_secret_key"

def get_node_telemetry():
    return {
        "node_id": NODE_ID,
        "timestamp": int(time.time()),
        "status": "ACTIVE",
        "metrics": {
            "load_avg": os.getloadavg() if hasattr(os, "getloadavg") else [0, 0, 0],
            "uptime": int(time.monotonic())
        }
    }

def generate_crypto_token(node_id, timestamp):
    hasher = hashlib.sha256()
    hasher.update(f"{SHARED_SECRET}{node_id}{timestamp}".encode('utf-8'))
    return hasher.hexdigest()

def spool_locally(data):
    spooled_records = []
    if os.path.exists(SPOOL_FILE):
        try:
            with open(SPOOL_FILE, "r") as f: spooled_records = json.load(f)
        except Exception: spooled_records = []
    spooled_records.append(data)
    with open(SPOOL_FILE, "w") as f: json.dump(spooled_records, f, indent=4)
    print(f"[{time.strftime('%H:%M:%S')}] 💾 Buffered data point locally.")

def process_spool():
    if not os.path.exists(SPOOL_FILE): return
    try:
        with open(SPOOL_FILE, "r") as f: spooled_records = json.load(f)
    except Exception: return
    if not spooled_records: return
    
    still_unsent = []
    for record in spooled_records:
        try:
            token = generate_crypto_token(record["node_id"], record["timestamp"])
            conn = http.client.HTTPConnection(PARENT_HOST, PARENT_PORT, timeout=3)
            headers = {
                "Content-Type": "application/json",
                "X-District-Token": token
            }
            conn.request("POST", "/api/telemetry", body=json.dumps(record), headers=headers)
            response = conn.getresponse()
            response.read()
            if response.status == 200: continue
            else: still_unsent.append(record)
        except Exception: still_unsent.append(record)

    if still_unsent:
        with open(SPOOL_FILE, "w") as f: json.dump(still_unsent, f, indent=4)
    else:
        if os.path.exists(SPOOL_FILE): os.remove(SPOOL_FILE)
        print(f"[{time.strftime('%H:%M:%S')}] ✨ Local buffer completely synced with parent.")

def transmit_loop():
    print(f"📡 Hardened Agent Node initialized. Shipping cryptographically signed streams...")
    while True:
        current_telemetry = get_node_telemetry()
        ts = current_telemetry["timestamp"]
        secure_token = generate_crypto_token(NODE_ID, ts)
        
        try:
            conn = http.client.HTTPConnection(PARENT_HOST, PARENT_PORT, timeout=3)
            headers = {
                "Content-Type": "application/json",
                "X-District-Token": secure_token
            }
            conn.request("POST", "/api/telemetry", body=json.dumps(current_telemetry), headers=headers)
            response = conn.getresponse()
            res_data = response.read().decode()
            conn.close()
            
            if response.status == 200:
                print(f"[{time.strftime('%H:%M:%S')}] 🟩 Signed packet accepted: {res_data}")
                process_spool()
            else:
                spool_locally(current_telemetry)
        except Exception:
            spool_locally(current_telemetry)
        time.sleep(TELEMETRY_INTERVAL)

if __name__ == "__main__":
    try: transmit_loop()
    except KeyboardInterrupt: sys.exit(0)
