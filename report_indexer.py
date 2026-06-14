import os
import json

EXPORTS_DIR = '/home/rick/pet_alpha/exports/'

def build_search_index():
    """
    Scans the exports directory, parsing static JSON artifacts into an 
    optimized, read-only operational dictionary structure.
    """
    index = {}
    
    if not os.path.exists(EXPORTS_DIR):
        return index
        
    for filename in os.listdir(EXPORTS_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(EXPORTS_DIR, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    report_id = data.get('report_id')
                    if report_id:
                        index[report_id] = data
            except (json.JSONDecodeError, IOError) as e:
                # Silently catch/log malformed artifacts without stopping execution
                continue
                
    return index

if __name__ == "__main__":
    idx = build_search_index()
    print(f"[✓] Indexer executed. Indexed {len(idx)} independent data artifacts.")
