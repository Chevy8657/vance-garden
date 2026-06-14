import sqlite3
import os
import sys

def run_preflight_checks():
    """
    Executes a clinical, zero-compromise audit of the local appliance environment.
    If core primitives are missing or altered, the node fails closed immediately.
    """
    DB_PATH = '/home/rick/pet_alpha/telemetry.db'
    
    # Digital Gothic Branded Output Token
    OBSIDIAN_BG     = "\033[48;5;232m"
    FOUNDRY_TEXT    = "\033[38;5;250m"
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    CRITICAL_RED    = "\033[38;5;196m"
    RESET           = "\033[0m"
    BOLD            = "\033[1m"
    
    print(f"{OBSIDIAN_BG}{GOLD_LEAF_AMBER}")
    print("X" + "═" * 88 + "X")
    print(f"║ {BOLD}NODE-ALPHA-001 // SYSTEM PRE-FLIGHT INITIALIZATION DETECTOR{RESET}{OBSIDIAN_BG}{GOLD_LEAF_AMBER}           ║")
    print("X" + "═" * 88 + "X" + FOUNDRY_TEXT)
    
    print("  [➔] Stage 1: File System Verification...")
    if not os.path.exists(DB_PATH):
        print(f"  └── {CRITICAL_RED}[CRITICAL FAULT] Local storage foundation not found at {DB_PATH}{FOUNDRY_TEXT}")
        print(f"  └── {CRITICAL_RED}STATUS: HALTING BOOT SEQUENCE TO PREVENT CONTAMINATION.{RESET}")
        sys.exit(1)
    print(f"  └── [✓] Found persistent database layer at: {DB_PATH}")
    
    print("  [➔] Stage 2: Schema Primitive Validation...")
    required_tables = {
        'agent_mesh_ledger': ['brokerage_id', 'cohort_type', 'sync_status'],
        'node_registry': ['node_id', 'node_type', 'status', 'parent_node_id'],
        'assessment_reports': ['report_id', 'generated_at', 'cpi_score', 'efficiency_yield']
    }
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        for table, expected_columns in required_tables.items():
            # Query table layout info from SQLite master internals
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [row[1] for row in cursor.fetchall()]
            
            if not columns:
                print(f"  └── {CRITICAL_RED}[CRITICAL FAULT] Table '{table}' missing entirely.{FOUNDRY_TEXT}")
                print(f"  └── {CRITICAL_RED}STATUS: STRUCTURAL INTEGRITY COMPROMISED. HALTING BOOT.{RESET}")
                conn.close()
                sys.exit(1)
                
            # Verify every critical infrastructure primitive column is present
            for col in expected_columns:
                if col not in columns:
                    print(f"  └── {CRITICAL_RED}[CRITICAL FAULT] Table '{table}' missing primitive column: '{col}'{FOUNDRY_TEXT}")
                    print(f"  └── {CRITICAL_RED}STATUS: SCHEMA MUTATION DETECTED. HALTING BOOT.{RESET}")
                    conn.close()
                    sys.exit(1)
            
            print(f"  └── [✓] Table '{table}' structure validated.")
            
    except sqlite3.Error as e:
        print(f"  └── {CRITICAL_RED}[DATABASE ERROR] {e}{RESET}")
        conn.close()
        sys.exit(1)
        
    conn.close()
    
    print("  " + "─" * 86)
    print(f"  {BOLD}SYSTEM HEALTH STATUS : OPERATIONAL{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
    print("  All local-first infrastructure barriers passed successfully.")
    print(GOLD_LEAF_AMBER + "X" + "═" * 88 + "X" + RESET)

if __name__ == "__main__":
    run_preflight_checks()
