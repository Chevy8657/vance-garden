import os
import sqlite3

def render_gated_scroll_interface(broker_name, contact):
    # Digital Gothic Design System - Color Palette
    OBSIDIAN_BG = "\033[48;5;232m"
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    parent_id = f"NODE-{broker_name.replace(' ', '-').upper()}"
    
    # Establish connection to telemetry database to verify real-time status
    conn = sqlite3.connect("/home/rick/pet_alpha/telemetry.db")
    cursor = conn.cursor()
    
    # Fetch current state of the brokerage parent node
    cursor.execute("SELECT status FROM node_registry WHERE node_id = ?", (parent_id,))
    row = cursor.fetchone()
    node_status = row[0] if row else "UNKNOWN"
    
    # Count successfully anchored child nodes
    cursor.execute("SELECT COUNT(*) FROM node_registry WHERE node_type = 'Child' AND parent_node_id = ?", (parent_id,))
    active_children = cursor.fetchone()[0]
    conn.close()
    
    # Target baseline setup for active agents
    target_agents = 150
    
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("=" * 80)
    print(f"{BOLD}THE GATED SCROLLS — SOVEREIGN INTERFACE GATEWAY{RESET}{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("=" * 80)
    print(f" MOTHERSHIP REGISTRY : {parent_id}")
    print(f" GATEWAY CHANNEL    : DIRECT DISPATCH TO {contact.upper()}")
    
    if node_status == "PAUSED_FOR_MESH_INFILTRATION":
        print(f" OPERATIONAL PHASE  : {BOLD}MOTHERSHIP STABILIZED // STRUCTURAL PAUSE ENGAGED{RESET}{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
        print("-" * 80)
        print(f"{RESET}{OBSIDIAN_BG}")
        
        print(f"  {BOLD}MOTHERSHIP STATUS: LOCKED & SECURE{RESET}{OBSIDIAN_BG}\n")
        print(f"  The primary brokerage server core is online. To ensure accurate logging")
        print(f"  of the environment metrics, Vance has initiated an operational freeze.\n")
        print(f"  {GOLD_LEAF_AMBER}THE 2-DAY MESH INTEGRATION BLITZ IS ACTIVE:{RESET}{OBSIDIAN_BG}")
        print(f"  We are systematically registering all participating office devices and agent")
        print(f"  endpoints into the parent-child local matrix over this 48-hour stretch.\n")
        print(f"  • Integrated Child Nodes : {active_children} / {target_agents} Devices Synced")
        
        # Sync Status Bar
        sync_pct = int((active_children / target_agents) * 100) if active_children > 0 else 0
        bar = "█" * (sync_pct // 4) + "░" * (25 - (sync_pct // 4))
        print(f"  • Fleet Synchronization  : |{GOLD_LEAF_AMBER}{bar}{RESET}{OBSIDIAN_BG}| [ {sync_pct}% ]\n")
        
        print(f"  {BOLD}EXCLUSION & SCALABILITY METRICS:{RESET}{OBSIDIAN_BG}")
        print(f"  Devices not anchored within the 48-hour window will be blacklisted from the")
        print(f"  initial baseline data flight and routed to subsequent scheduled MAKEUP DATES")
        print(f"  or processed as persistent system add-ons at a later checkpoint.")
        
    else:
        print(f" OPERATIONAL PHASE  : ACTIVE TELEMETRY FLIGHT")
        print("-" * 80)
        print(f"{RESET}{OBSIDIAN_BG}")
        print("\n  [+] Mesh deployment verified. Baseline telemetry logging active.\n")
        
    print("\n" + "-" * 80)
    print(f"  {GOLD_LEAF_AMBER}VANCE GATEWAY: Operating detached under the hood [0% CPU overhead]{RESET}{OBSIDIAN_BG}")
    print("=" * 80)
    print(RESET)

if __name__ == "__main__":
    render_gated_scroll_interface("Urban Nest Realty", "Rick's Nevada Pipeline Team")
