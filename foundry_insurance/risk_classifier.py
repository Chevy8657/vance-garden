import json, os
from foundry_insurance.carrier_property_link import CarrierPropertyLink
class RiskClassifier:
    def __init__(self, path="foundry_insurance/risk_classifications.json"):
        self.path = path
        self.linker = CarrierPropertyLink()
        if not os.path.exists(self.path):
            with open(self.path, "w") as f: json.dump({}, f)
    def classify(self, carrier_id, property_id, property_data):
        if not self.linker.is_authorized(carrier_id, property_id): raise PermissionError("Unauthorized")
        classification = {"classification_id": f"RISK-{property_id}", "risk_score": 95, "risk_band": "LOW"}
        with open(self.path, "r+") as f:
            data = json.load(f); data[classification["classification_id"]] = classification
            f.seek(0); json.dump(data, f, indent=4)
        return classification
