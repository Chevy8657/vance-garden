import sqlite3

def render_latest_gated_scroll_report():
    """
    Queries the local assessment_reports table and renders a high-fidelity,
    authoritative terminal view using the Digital Gothic aesthetic grammar.
    """
    conn = sqlite3.connect('/home/rick/pet_alpha/telemetry.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                report_id, generated_at, node_id, total_nodes_evaluated, 
                primary_baseline_count, makeup_pool_count, rejected_count, 
                cpi_score, efficiency_yield, observations, recommendation 
            FROM assessment_reports 
            ORDER BY generated_at DESC 
            LIMIT 1;
        """)
        report = cursor.fetchone()
    except sqlite3.OperationalError as e:
        print(f"\n\033[31m[!] DATABASE FAULT: {e}\033[0m\n")
        conn.close()
        return
        
    conn.close()
    
    if not report:
        print("\n\033[31m[!] CRITICAL FAULT: No local assessment records found to render.\033[0m\n")
        return

    # Digital Gothic Color Archetypes
    OBSIDIAN_BG     = "\033[48;5;232m"
    FOUNDRY_TEXT    = "\033[38;5;250m"
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    VITRUVEO_TEAL   = "\033[38;5;44m"
    RESET           = "\033[0m"
    BOLD            = "\033[1m"
    
    print(f"{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("X" + "═" * 88 + "X")
    print(f"║ {BOLD}PET ALPHA APPLIANCE // THE GATED SCROLLS RECONCILIATION MANIFEST{RESET}{OBSIDIAN_BG}{GOLD_LEAF_AMBER}       ║")
    print("X" + "═" * 88 + "X" + FOUNDRY_TEXT)
    
    # Section: Infrastructure Primitives
    print(f"  {BOLD}CORE INFRASTRUCTURE METADATA{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
    print(f"  ├── ARTIFACT SIGNATURE : {GOLD_LEAF_AMBER}{report['report_id']}{FOUNDRY_TEXT}")
    print(f"  ├── PARENT AUTHORITY   : {report['node_id']}")
    print(f"  └── CHRONOLOGY STAMP   : {report['generated_at']}")
    print("  " + "─" * 86)
    
    # Section: Cohort Telemetry Matrix
    print(f"  {BOLD}LOCAL FLEET DEPLOYMENT METRICS{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
    print(f"  ├── Total Connected Handsets  : {GOLD_LEAF_AMBER}{report['total_nodes_evaluated']}{FOUNDRY_TEXT}")
    print(f"  ├── Primary Cohort (Baseline) : {VITRUVEO_TEAL}{report['primary_baseline_count']}{FOUNDRY_TEXT}")
    print(f"  ├── Isolated Makeup Buffer     : {report['makeup_pool_count']}")
    print(f"  └── Terminated Excursions      : {report['rejected_count']}")
    print("  " + "─" * 86)
    
    # Section: Deterministic Calculations
    print(f"  {BOLD}EVIDENCE-FIRST YIELD ANALYSIS{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
    
    # Visual Progress Bar for Core Network Efficiency
    bar_length = 20
    yield_val = report['efficiency_yield']
    filled_length = int(round(bar_length * yield_val / 100)) if yield_val > 0 else 0
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    print(f"  ├── CPI Friction Score         : {GOLD_LEAF_AMBER}{report['cpi_score']}{FOUNDRY_TEXT}")
    print(f"  └── Network Efficiency Yield   : [{VITRUVEO_TEAL}{bar}{FOUNDRY_TEXT}] {GOLD_LEAF_AMBER}{yield_val}%{FOUNDRY_TEXT}")
    print("  " + "─" * 86)
    
    # Section: Governance & Recommendations
    print(f"  {BOLD}SYSTEM ARCHITECTURE DETERMINATION{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
    print(f"  ├── OBSERVATION  : {report['observations']}")
    print(f"  └── ENFORCEMENT  : {GOLD_LEAF_AMBER}{report['recommendation']}{FOUNDRY_TEXT}")
    
    print(GOLD_LEAF_AMBER + "X" + "═" * 88 + "X" + RESET)

if __name__ == "__main__":
    render_latest_gated_scroll_report()
