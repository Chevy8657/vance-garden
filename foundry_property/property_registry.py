import json
import uuid
import hashlib
from datetime import datetime
import os

class PropertyRegistry:
    def __init__(self, db_path='properties.json', event_log='property_events.json'):
        self.db_path = db_path
        self.event_log = event_log
        # Initialize files if they don't exist
        for path in [self.db_path, self.event_log]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f)

    def _generate_hash(self, property_data):
        """Creates a unique hash for the initial state of the property."""
        content = f"{property_data['property_id']}{property_data['street_address']}{property_data['created_at']}"
        return hashlib.sha256(content.encode()).hexdigest()

    def register_property(self, details):
        """Creates a new property record and triggers the registration event."""
        property_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        # Assemble property record according to schema v1
        new_property = {
            "property_id": property_id,
            "property_name": details.get("property_name"),
            "street_address": details.get("street_address"),
            "city": details.get("city"),
            "state": details.get("state"),
            "zip_code": details.get("zip_code"),
            "jurisdiction_code": details.get("jurisdiction_code"),
            "manager_id": details.get("manager_id"),
            "registrar_id": details.get("registrar_id"),
            "created_at": created_at,
            "property_status": "ACTIVE",
            "registration_hash": ""
        }
        
        # Calculate integrity hash
        new_property["registration_hash"] = self._generate_hash(new_property)
        
        # Write to Property Registry
        properties = self._load_data(self.db_path)
        properties.append(new_property)
        self._save_data(self.db_path, properties)
        
        # Record the immutable event
        self._record_event("PROPERTY_REGISTERED", {"property_id": property_id})
        
        return new_property

    def _record_event(self, event_type, data):
        events = self._load_data(self.event_log)
        event_entry = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        events.append(event_entry)
        self._save_data(self.event_log, events)

    def _load_data(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def _save_data(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
