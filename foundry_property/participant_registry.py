import json
import os

class ParticipantRegistry:
    def __init__(self, registry_file="foundry_property/participants.json"):
        self.registry_file = registry_file
        if not os.path.exists(self.registry_file):
            with open(self.registry_file, "w") as f:
                json.dump({}, f)

    def register(self, participant_id, p_type, metadata):
        with open(self.registry_file, "r+") as f:
            data = json.load(f)
            data[participant_id] = {
                "type": p_type,
                "metadata": metadata,
                "trust_status": "VERIFIED"
            }
            f.seek(0)
            json.dump(data, f, indent=4)
        return data[participant_id]
