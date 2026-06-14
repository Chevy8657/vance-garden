import json, os
class InsuranceDossierGenerator:
    def __init__(self, output_dir="foundry_insurance/insurance_dossiers"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    def generate(self, carrier_id, property_id):
        dossier = {"dossier_type": "INSURANCE_RISK_DOSSIER", "status": "AUTHORIZED"}
        with open(os.path.join(self.output_dir, f"dossier_{property_id}.json"), "w") as f:
            json.dump(dossier, f, indent=4)
        return dossier
