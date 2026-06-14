import json
import os
from datetime import datetime, timezone
import uuid

class MaintenanceLogger:
    def __init__(self, maintenance_file="foundry_property/maintenance_events.json"):
        self.maintenance_file = maintenance_file
        if not os.path.exists(self.maintenance_file):
            with open(self.maintenance_file, "w") as f:
                json.dump([], f)

    def log_maintenance(self, property_id, description, priority="NORMAL", created_by="SYSTEM"):
        event = {
            "maintenance_id": f"MAINT-{uuid.uuid4().hex[:8].upper()}",
            "property_id": property_id,
            "opened_at": datetime.now(timezone.utc).isoformat(),
            "description": description,
            "priority": priority,
            "status": "OPEN",
            "created_by": created_by
        }
        
        with open(self.maintenance_file, "r+") as f:
            data = json.load(f)
            data.append(event)
            f.seek(0)
            json.dump(data, f, indent=4)
            
        return event
