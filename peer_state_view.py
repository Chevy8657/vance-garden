import sqlite3
from offline_gap_detector import calculate_peer_drift

DB_PATH = '/home/rick/pet_alpha/telemetry.db'

def render_immune_system_report():
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    VITRUVEO_TEAL   = "\033[38;5;44m"
    CRITICAL_RED    = "\033[38;5;196m"
    RESET           = "\033[0m"
    BOLD            = "\033[1m"
    
    print("\n" + GOLD_LEAF_AMBER + "═" * 90)
    print(f" {BOLD}PET SYSTEM APPLIANCE // SPRINT 6: PEER BEHAVIOR REPUTATION ANALYSIS LOG{RESET}{GOLD_LEAF_AMBER}")
    print("═" * 90 + RESET)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM peer_registry;")
    peers = cursor.fetchall()
    
    if not peers:
        print("  [-] No registered node identities present in peer network ledger matrix.")
        conn.close()
        return

    for p in peers:
        node = p['node_id']
        status = p['trust_status']
        status_color = CRITICAL_RED if status == 'SUSPENDED' else GOLD_LEAF_AMBER if status == 'QUARANTINED' else VITRUVEO_TEAL
        
        condition, hours = calculate_peer_drift(node)
        
        print(f"\n  • {BOLD}NODE IDENTITY:{RESET} {node:<16} | {BOLD}STATUS:{RESET} {status_color}{status:<12}{RESET}")
        print(f"    ├── Last Seen : {p['last_seen'][:19].replace('T', ' ')} UTC (Gap: {hours:.2f} hrs -> {condition})")
        print(f"    └── Safe Trace: Last Pkt ID: {p['last_packet_id'] or 'NONE':<10} | Last Match Hash: {p['last_accepted_hash'] or 'NONE'}")
        
        # Pull transactional pattern breakdown for this specific peer
        cursor.execute("""
            SELECT outcome_category, COUNT(*) as cnt 
            FROM peer_sync_ledger 
            WHERE node_id = ? 
            GROUP BY outcome_category;
        """, (node,))
        
        tallies = {row['outcome_category']: row['cnt'] for row in cursor.fetchall()}
        
        print(f"    └── Transactional Metric Counters:")
        print(f"        [✓] ACCEPTED: {tallies.get('ACCEPTED', 0):<4} [⚠️] QUARANTINED: {tallies.get('QUARANTINED', 0):<4}")
        print(f"        [🛑] REPLAY_BLOCKED: {tallies.get('REPLAY_BLOCKED', 0):<4} [🧬] HASH_MUTATIONS_CAUGHT: {tallies.get('HASH_MUTATION_BLOCKED', 0)}")
    
    conn.close()
    print("\n" + GOLD_LEAF_AMBER + "═" * 90 + RESET + "\n")

if __name__ == "__main__":
    render_immune_system_report()
