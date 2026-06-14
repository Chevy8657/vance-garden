import sqlite3
import json
import os

def export_latest_assessment_artifacts():
    """
    Reads the latest entry from assessment_reports and exports twin artifacts:
    1. A raw JSON payload data file.
    2. A clean, fixed-width ASCII plain text manifest (.txt).
    """
    reports_dir = '/home/rick/pet_alpha/reports/'
    
    conn = sqlite3.connect('/home/rick/pet_alpha/telemetry.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
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
    conn.close()
    
    if not report:
        print("\n\033[31m[!] EXPORT FAULT: No local assessment records found to save.\033[0m\n")
        return

    report_dict = dict(report)
    base_filename = os.path.join(reports_dir, f"{report['report_id']}")
    
    # ---- ARTIFACT 1: Programmatic Structured JSON ----
    json_path = f"{base_filename}.json"
    with open(json_path, 'w') as f:
        json.dump(report_dict, f, indent=4)
        
    # ---- ARTIFACT 2: Fixed-Width ASCII Manifest ----
    txt_path = f"{base_filename}.txt"
    
    # Progress bar text construction
    bar_length = 20
    yield_val = report['efficiency_yield']
    filled_length = int(round(bar_length * yield_val / 100)) if yield_val > 0 else 0
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("X" + "═" * 88 + "X\n")
        f.write(f"║ PET ALPHA APPLIANCE // THE GATED SCROLLS RECONCILIATION MANIFEST       ║\n")
        f.write("X" + "═" * 88 + "X\n\n")
        
        f.write("  CORE INFRASTRUCTURE METADATA\n")
        f.write(f"  ├── ARTIFACT SIGNATURE : {report['report_id']}\n")
        f.write(f"  ├── PARENT AUTHORITY   : {report['node_id']}\n")
        f.write(f"  └── CHRONOLOGY STAMP   : {report['generated_at']}\n")
        f.write("  " + "─" * 86 + "\n\n")
        
        f.write("  LOCAL FLEET DEPLOYMENT METRICS\n")
        f.write(f"  ├── Total Connected Handsets  : {report['total_nodes_evaluated']}\n")
        f.write(f"  ├── Primary Cohort (Baseline) : {report['primary_baseline_count']}\n")
        f.write(f"  ├── Isolated Makeup Buffer     : {report['makeup_pool_count']}\n")
        f.write(f"  └── Terminated Excursions      : {report['rejected_count']}\n")
        f.write("  " + "─" * 86 + "\n\n")
        
        f.write("  EVIDENCE-FIRST YIELD ANALYSIS\n")
        f.write(f"  ├── CPI Friction Score         : {report['cpi_score']}\n")
        f.write(f"  └── Network Efficiency Yield   : [{bar}] {yield_val}%\n")
        f.write("  " + "─" * 86 + "\n\n")
        
        f.write("  SYSTEM ARCHITECTURE DETERMINATION\n")
        f.write(f"  ├── OBSERVATION  : {report['observations']}\n")
        f.write(f"  └── ENFORCEMENT  : {report['recommendation']}\n\n")
        
        f.write("X" + "═" * 88 + "X\n")

    print(f"\n\033[32m[✓] SPRINT 2 COMPLETE: Twin artifacts compiled successfully.\033[0m")
    print(f"    ➔ Data Payload  : {json_path}")
    print(f"    ➔ Visual Scroll : {txt_path}\n")

if __name__ == "__main__":
    export_latest_assessment_artifacts()
