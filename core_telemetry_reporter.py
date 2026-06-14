import sqlite3
import json
import os

DB_PATH = '/home/rick/pet_alpha/telemetry.db'
TRANSMIT_LOG_PATH = '/home/rick/pet_alpha/broadcast_history.log'

def generate_telemetry_dashboard():
    """
    Queries local state variables and outputs a structured diagnostic dashboard
    aligned with the digital gothic UI system specification.
    """
    if not os.path.exists(DB_PATH):
        print(f"\033[38;5;196m[✕] Monitoring Error: Telemetry database missing at {DB_PATH}\033[0m")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Fetch Node Peer Trust Metrics
    try:
        cursor.execute("SELECT node_id, trust_status, last_seen FROM peer_registry;")
        peers = cursor.fetchall()
    except sqlite3.OperationalError:
        peers = []

    # 2. Fetch Core Transaction Ledger Analytics
    try:
        cursor.execute("SELECT COUNT(*), COUNT(DISTINCT origin_node) FROM transaction_ledger;")
        total_transactions, distinct_nodes = cursor.fetchone()
    except sqlite3.OperationalError:
        total_transactions, distinct_nodes = 0, 0

    # 3. Fetch Active Operational Policy Configurations
    try:
        cursor.execute("SELECT config_key, config_value FROM active_system_config;")
        configs = cursor.fetchall()
    except sqlite3.OperationalError:
        configs = []

    conn.close()

    # 4. Count Broadcast History Entries if available
    broadcast_count = 0
    if os.path.exists(TRANSMIT_LOG_PATH):
        with open(TRANSMIT_LOG_PATH, 'r') as f:
            broadcast_count = len(f.readlines())

    # Build the Diagnostic UI Panels
    print("\033[48;5;232m" + "="*90)
    print(" │ FOUNDRY APPLIANCE CORE TELEMETRY METRIC MONITOR")
    print("="*90)
    
    print(f" ❖ NETWORK INFRASTRUCTURE AGGREGATION")
    print(f"   ├── Total Committed Transactions : \033[1;38;5;44m{total_transactions}\033[0m records")
    print(f"   ├── Active Outbound Broadcasts   : \033[1;38;5;44m{broadcast_count}\033[0m dispatches")
    print(f"   └── Unique Ingress Data Sources  : {distinct_nodes} peers registered")
    print(" " + "-"*88)

    print(" ❖ ACTIVE OPERATIONAL CONFIGURATIONS")
    if configs:
        for key, val in configs:
            print(f"   └── \033[38;5;214m{key:<20}\033[0m ➔ \033[1m{val}\033[0m")
    else:
        print("   └── [!] Zero live business configurations committed.")
    print(" " + "-"*88)

    print(" ❖ PEER IDENTITY REGISTRY MATRIX")
    if peers:
        for node_id, status, last_seen in peers:
            status_color = "\033[38;5;44m" if "TRUST" in status or status == "TRUSTED" else "\033[38;5;196m"
            print(f"   ├── \033[1m{node_id:<15}\033[0m 🌟 Status: {status_color}{status:<15}\033[0m Last Active: {last_seen[:19]}")
    else:
        print("   └── Registry matrix is unseeded.")
        
    print("="*90 + "\033[0m")

if __name__ == "__main__":
    generate_telemetry_dashboard()
