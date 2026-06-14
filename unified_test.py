import json
import os
import sys

# Ensure the subfolder is in the path
sys.path.append(os.path.join(os.getcwd(), 'foundry_property'))

# Ensure files exist
os.makedirs('foundry_property', exist_ok=True)
registry_file = 'foundry_property/properties.json'
event_file = 'foundry_property/property_events.json'

if not os.path.exists(registry_file):
    with open(registry_file, 'w') as f:
        json.dump([{"property_id": "TEST-123", "street_address": "Test St"}], f)

# Attempt import
try:
    from inspection_logger import InspectionLogger
    logger = InspectionLogger(registry_file, event_file)
    logger.log_inspection("TEST-123", "SYSTEM", "PASS", "Automated validation")
    print("SUCCESS: Integrity verified.")
except ImportError:
    print("Error: inspection_logger.py not found in foundry_property/")
except Exception as e:
    print(f"Execution Error: {e}")
