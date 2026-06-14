import sqlite3
import os
import sys
import time

def run_chaos_simulation():
    db_path = '/home/rick/pet_alpha/telemetry.db'
    print("=" * 90)
    print("Executing Node Survival Test: ACID Transaction Boundary Isolation")
    print("=" * 90)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current row count of reports for baseline check
    cursor.execute("SELECT COUNT(*) FROM assessment_reports;")
    initial_count = cursor.fetchone()[0]
    print(f"[➔] Initial pre-crash stable state count: {initial_count} records.")
    
    print("[➔] Opening dirty, non-committed database transaction...")
    try:
        # Intentionally open a transaction block without committing
        cursor.execute("""
            INSERT INTO assessment_reports 
            (report_id, generated_at, node_id, total_nodes_evaluated, primary_baseline_count, 
             makeup_pool_count, rejected_count, cpi_score, efficiency_yield, observations, recommendation)
            VALUES ('PET-RPT-CORRUPTED-CHAOS-NODE', 'INVALID_TIME', 'CRASH_TEST', 999, 0, 0, 0, 0.0, 0.0, 'DIRTY_DATA', 'SHOULD_NEVER_EXIST');
        """)
        
        # Simulate a hard, unannounced process termination right here before conn.commit() is ever reached
        print("\n[!!!] SIMULATING HARD SYSTEM CRASH / LOSS OF POWER / SERVICE TERMINATION")
        print("[!!!] Killing the active execution thread immediately without closing handles.\n")
        sys.stdout.flush()
        
        # Hard exit the process to mimic a severe power loss or OS kill signal
        os._exit(1)
        
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_chaos_simulation()
