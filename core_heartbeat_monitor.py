import sqlite3
import datetime
import os

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

class CoreHeartbeatMonitor:
    def __init__(self):
        pass

    def enforce_temporal_decay(self):
        """
        Calculates the exact time delta since each peer's last verification 
        and systematically applies dynamic trust degradation rules.
        """
        print("="*90)
        print("EXECUTING PEER IDENTITY TEMPORAL DECAY SWEEP")
        print("="*90)

        if not os.path.exists(DB_PATH):
            print("[✕] Monitor Error: Target database registry missing.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fetch current system timestamp in UTC
        now = datetime.datetime.now(datetime.timezone.utc)

        try:
            cursor.execute("SELECT node_id, trust_status, last_seen FROM peer_registry;")
            peers = cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"[✕] Database read error: {e}")
            conn.close()
            return

        demotions = 0

        for node_id, status, last_seen_str in peers:
            # Skip nodes that are explicitly suspended via administrative intervention
            if status == "SUSPENDED":
                continue

            try:
                # Standardizing various SQLite text formats into an aware datetime
                if "Z" in last_seen_str:
                    last_seen_str = last_seen_str.replace("Z", "+00:00")
                if "+" not in last_seen_str:
                    # Treat raw system strings as UTC
                    last_seen_str += "+00:00"
                
                # Truncate fractional seconds if present from sqlite expressions
                if "." in last_seen_str:
                    base, offset = last_seen_str.split("+")
                    base = base.split(".")[0]
                    last_seen_str = f"{base}+{offset}"

                last_seen = datetime.datetime.fromisoformat(last_seen_str)
            except ValueError:
                print(f" [!] Warning: Skipping parsing for node {node_id} due to invalid format: {last_seen_str}")
                continue

            # Calculate precise time variance in hours
            delta = now - last_seen
            delta_hours = delta.total_seconds() / 3600.0

            print(f" ❖ Eval: {node_id:<15} | Current Status: {status:<14} | Offline Gap: {delta_hours:.2f} hrs")

            # Condition A: Demote stale elevated endpoints
            if delta_hours > 1.0 and delta_hours <= 24.0 and status == "ELEVATED_TRUST":
                print(f"   └── \033[38;5;214m[⚠️ DEMOTION]\033[0m Target exceeded active horizon. Shifting to standard TRUSTED.")
                cursor.execute("UPDATE peer_registry SET trust_status = 'TRUSTED' WHERE node_id = ?;", (node_id,))
                demotions += 1

            # Condition B: Quarantine fully non-responsive instances
            elif delta_hours > 24.0 and status != "STALE_SUSPENDED":
                print(f"   └── \033[38;5;196m[🚨 QUARANTINE]\033[0m Target crossed max stale window. Shifting to STALE_SUSPENDED.")
                cursor.execute("UPDATE peer_registry SET trust_status = 'STALE_SUSPENDED' WHERE node_id = ?;", (node_id,))
                demotions += 1

        if demotions > 0:
            conn.commit()
            print(f"\n\033[38;5;44m[✓] Decay sweep complete. Mutated {demotions} identity states.\033[0m")
        else:
            print(f"\n[i] All identity statuses within acceptable nominal windows. Zero mutations applied.")

        conn.close()
        print("="*90)

if __name__ == "__main__":
    monitor = CoreHeartbeatMonitor()
    monitor.enforce_temporal_decay()
