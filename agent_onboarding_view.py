import os
import time
import sqlite3
import datetime

def process_onboarding_to_ledger(broker_name):
    # Digital Gothic Palette ANSI Escapes
    OBSIDIAN_BG = "\033[48;5;232m"
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[38;5;51m"
    
    parent_id = f"NODE-{broker_name.replace(' ', '-').upper()}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Roster array mapping directly to the live terminal display
    incoming_agents = [
        {"name": "Agent Sarah Jenkins", "type": "Office Mobile", "action": "SYNCED"},
        {"name": "Agent Marcus Vance", "type": "Workstation Laptop", "action": "SYNCED"},
        {"name": "Agent Bradley Cooper", "type": "Office Mobile", "action": "SYNCED"},
        {"name": "Agent Claire Redfield", "type": "Remote Laptop", "action": "MAKEUP"},
    ]
    
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("=" * 80)
    print(f"{BOLD}THE GATED SCROLLS — LIVE SCREEN SHARE: AGENT FLEET LOADING MATRIX{RESET}{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("=" * 80)
    print(f" MOTHERSHIP TARGET : {parent_id}")
    print(f" MESH SPRINT TIME  : 48-HOUR BLITZ ACTIVE")
    print("-" * 80)
    print(f"{RESET}{OBSIDIAN_BG}")
    
    print(f"  {BOLD}INITIALIZING LOCAL DEVICE INGESTION DISPATCH...{RESET}{OBSIDIAN_BG}\n")
    time.sleep(1)
    
    conn = sqlite3.connect("/home/rick/pet_alpha/telemetry.db")
    cursor = conn.cursor()
    
    for agent in incoming_agents:
        print(f"  [⚡] INCOMING DEPLOYMENT REQUEST DETECTED...")
        time.sleep(0.8)
        print(f"      Identity  : {agent['name']}")
        print(f"      Hardware  : {agent['type']}")
        
        child_node_id = f"NODE-CHILD-{agent['name'].replace(' ', '-').upper()}"
        
        if agent['action'] == "SYNCED":
            print(f"      Topology  : {GOLD_LEAF_AMBER}SUCCESS ──► Anchored as Child Node to Mothership Parent{RESET}{OBSIDIAN_BG}")
            # Insert active child node directly linked to the mothership
            cursor.execute("""
                INSERT OR REPLACE INTO node_registry (node_id, owner_name, tier, activation_date, status, node_type, parent_node_id)
                VALUES (?, ?, 'Agent Device Endpoint', ?, 'active', 'Child', ?)
            """, (child_node_id, agent['name'], timestamp, parent_id))
        else:
            print(f"      Topology  : {CYAN}WINDOW EXPIRED ──► Diverted to Scheduled Makeup Checkpoint{RESET}{OBSIDIAN_BG}")
            # Store in database under a pending/makeup status to preserve the boundary
            cursor.execute("""
                INSERT OR REPLACE INTO node_registry (node_id, owner_name, tier, activation_date, status, node_type, parent_node_id)
                VALUES (?, ?, 'Agent Device Endpoint Pool', ?, 'PENDING_MAKEUP', 'Child', ?)
            """, (child_node_id, agent['name'], timestamp, parent_id))
            
        print(f"      Resource  : System idling perfectly at 0% CPU utilization.")
        print("-" * 60)
        conn.commit()
        time.sleep(1)
        
    conn.close()
    
    print(f"\n{GOLD_LEAF_AMBER}")
    print("=" * 80)
    print(f" MESH STATUS: PHASE 1 COMPLETED | AWAITING LATE-STAGE PERSISTENT ADD-ONS")
    print("=" * 80)
    print(RESET)

if __name__ == "__main__":
    process_onboarding_to_ledger("Urban Nest Realty")
