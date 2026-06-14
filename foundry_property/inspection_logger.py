import json
import uuid
from datetime import datetime
from property_registry import PropertyRegistry

class InspectionLogger:
    def __init__(self, property_db='properties.json', event_log='property_events.json'):
        self.registry = PropertyRegistry(property_db, event_log)
        self.event_log = event_log

    def log_inspection(self, property_id, inspector_id, status, report):
        properties = self.registry._load_data(self.registry.db_path)
        if not any(p['property_id'] == property_id for p in properties):
            raise ValueError(f"Property {property_id} not found.")

        inspection_event = {
            "event_id": str(uuid.uuid4()),
            "property_id": property_id,
            "event_type": "PROPERTY_INSPECTION",
            "inspector_id": inspector_id,
            "status": status,
            "report": report,
            "timestamp": datetime.utcnow().isoformat()
        }
        events = self.registry._load_data(self.event_log)
        events.append(inspection_event)
        self.registry._save_data(self.event_log, events)
        return inspection_event
