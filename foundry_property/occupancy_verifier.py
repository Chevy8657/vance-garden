import json
import os
from datetime import datetime, timezone
import uuid

class OccupancyVerifier:
    def __init__(self, occupancy_file="foundry_property/occupancy_records.json"):
        self.occupancy_file = occupancy_file
        if not os.path.exists(self.occupancy_file):
            with open(self.occupancy_file, "w") as f:
                json.dump([], f)

    def verify(self, property_id, status, verified_by):
        record = {
            "verification_id": f"OCC-{uuid.uuid4().hex[:8].upper()}",
            "property_id": property_id,
            "occupancy_status": status,
            "verified_by": verified_by,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "verification_hash": uuid.uuid4().hex
        }
        
        with open(self.occupancy_file, "r+") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=4)
            
        return record
