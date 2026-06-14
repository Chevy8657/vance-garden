import json, os, hashlib
from datetime import datetime, timezone
class CarrierRegistry:
    def __init__(self, path="foundry_insurance/carriers.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f: json.dump({}, f)
    def register(self, carrier_id, carrier_name, carrier_type, jurisdiction):
        carrier = {"carrier_id": carrier_id, "carrier_name": carrier_name, "status": "ACTIVE"}
        with open(self.path, "r+") as f:
            data = json.load(f); data[carrier_id] = carrier
            f.seek(0); json.dump(data, f, indent=4)
        return carrier
