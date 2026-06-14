from inspection_logger import InspectionLogger
import json
import os

def run_test():
    # Ensure properties.json exists from previous steps
    if not os.path.exists('properties.json'):
        print("Error: properties.json not found. Run register_property first.")
        return
        
    logger = InspectionLogger()
    with open('properties.json', 'r') as f:
        props = json.load(f)
    
    if not props:
        print("Error: No properties registered. Register one first.")
        return
        
    target_id = props[0]['property_id']
    logger.log_inspection(target_id, "TEST-USER", "PASS", "Test inspection")
    print("SUCCESS")

if __name__ == "__main__":
    run_test()
