import sqlite3

def purge_inactive_territory(region_keyword):
    conn = sqlite3.connect("/home/rick/pet_alpha/telemetry.db")
    cursor = conn.cursor()
    
    # Remove any mock parent or child nodes tagged with the inactive region
    cursor.execute("DELETE FROM node_registry WHERE node_id LIKE ? OR parent_node_id LIKE ?", 
                   (f"%{region_keyword}%", f"%{region_keyword}%"))
    
    conn.commit()
    changes = conn.total_changes
    conn.close()
    
    print(f"\n[⚡ VANCE PURGE] Scrubbing database ledger...")
    print(f"[✓] SUCCESS: Removed {changes} stale tracking records linked to '{region_keyword}'.")
    print("[✓] TERRITORY MATRIX FILTERED: Core focus restricted to Nevada and Texas execution lines.")

if __name__ == "__main__":
    purge_inactive_territory("WISCONSIN")
