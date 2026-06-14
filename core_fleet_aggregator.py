import sqlite3
import os

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class CoreFleetAggregator:
    def __init__(self):
        pass

    def generate_fleet_intelligence_report(self):
        print("="*90)
        print("COMPILING CROSS-EPOCH DECENTRALIZED FLEET TELEMETRY REPORT")
        print("="*90)

        if not os.path.exists(DB_PATH):
            print("[✕] Operational Error: Local telemetry storage file unreadable.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            # 1. Fetch current temporal sequence metadata
            cursor.execute("SELECT config_value FROM active_system_config WHERE config_key = 'CURRENT_EPOCH_SEQUENCE';")
            epoch = cursor.fetchone()
            current_epoch = epoch[0] if epoch else "0"

            # 2. Extract operational peer matrices
            cursor.execute("SELECT node_id, trust_status FROM peer_registry;")
            peers = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[✕] Aggregation Aborted: Failed to parse persistence structures: {e}")
            conn.close()
            return
        finally:
            conn.close()

        total_nodes = len(peers)
        active_voters = [n for n in peers if n[1] in ('TRUSTED', 'ELEVATED_TRUST')]
        disabled_nodes = [n for n in peers if n[1] not in ('TRUSTED', 'ELEVATED_TRUST')]

        # Calculate consensus readiness velocity
        readiness_percentage = (len(active_voters) / total_nodes * 100) if total_nodes > 0 else 0.0

        print(f"📡 Current Network Synchronization Epoch : Block Sequence #{current_epoch}")
        print(f"📊 Global Consensus Topology Footprint     : {total_nodes} Node Instances Tracked")
        print(f"    ├── Active Consensus Clearance Quorum : {len(active_voters)} Instances Online")
        print(f"    └── Isolated Out-of-Band Nodes       : {len(disabled_nodes)} Instances Dormant")
        print(f"📈 Estimated Cluster Consensus Readiness  : \033[38;5;44m{readiness_percentage:.1f}%\033[0m")
        print("-"*90)
        
        print("🌐 LIVE TOPOLOGY DISTRIBUTION MONITOR")
        for node_id, status in peers:
            display_status = f"\033[38;5;44m{status:<16}\033[0m" if status in ('TRUSTED', 'ELEVATED_TRUST') else f"\033[38;5;196m{status:<16}\033[0m"
            print(f"    ├── {node_id:<16} ➔ Security Status: {display_status}")
        print("="*90)

if __name__ == "__main__":
    aggregator = CoreFleetAggregator()
    aggregator.generate_fleet_intelligence_report()
