import sqlite3
from datetime import datetime

def check_node_anniversaries():
    # Connect to your sovereign node database
    conn = sqlite3.connect("telemetry.db")
    cursor = conn.cursor()
    
    # Fetch active nodes, their original activation timestamps, and owner details
    # Assumes a structured node_registry table matching your node architecture
    try:
        cursor.execute("SELECT node_id, owner_name, tier, activation_date FROM node_registry WHERE status = 'active'")
        active_nodes = cursor.fetchall()
    except sqlite3.OperationalError:
        print("[-] node_registry table not initialized yet. Skipping check.")
        conn.close()
        return

    today = datetime.now()
    current_md = today.strftime("%m-%d")
    current_year = today.year

    print(f"[*] Scanning network registry for milestones: {today.strftime('%Y-%m-%d')}")
    
    for node_id, owner, tier, activation_date_str in active_nodes:
        # Expected format: 'YYYY-MM-DD'
        act_date = datetime.strptime(activation_date_str, "%Y-%m-%d")
        act_md = act_date.strftime("%m-%d")
        
        if current_md == act_md and current_year > act_date.year:
            years_active = current_year - act_date.year
            print(f"\n[★] MILESTONE DETECTED: Node {node_id} ({tier}) owned by {owner} has hit Year {years_active}!")
            print(f"[-] Dispatching automated appreciation workflow request for {owner}...")
            # Here, the engine can fire a webhook to print a custom thank you card or queue a high-end corporate gift shipment
            
    conn.close()

if __name__ == "__main__":
    check_node_anniversaries()
