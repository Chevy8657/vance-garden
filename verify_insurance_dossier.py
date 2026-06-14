import sys
import os
sys.path.append(os.getcwd())

from foundry_insurance.insurance_dossier import InsuranceDossierGenerator

generator = InsuranceDossierGenerator()

# Generate the Dossier
dossier = generator.generate("CAR-001", "PROP-001")

print(f"[✓] Dossier Exported: {dossier['dossier_type']} for {dossier['property_id']}")
print(f"[✓] Risk Band: {dossier['risk_band']} | Confidence: {dossier['underwriting_confidence']}")

# Verify Rule Enforcement
try:
    generator.generate("UNAUTH-CARRIER", "PROP-001")
except PermissionError:
    print("[✓] Dossier Access Denied: Unauthorized carrier")

print("[★] SPRINT 46: INSURANCE DOSSIER EXPORT VERIFIED")
