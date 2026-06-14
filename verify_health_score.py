import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from unified_dossier import UnifiedDossier

aggregator = UnifiedDossier()
dossier = aggregator.generate("PROP-001")

# Debugging the business logic outcome
print("--- DOSSIER DEBUG PAYLOAD ---")
print(json.dumps(dossier, indent=4))
print("-----------------------------")

print(f"Property Health Score: {dossier['health_score']} / 100")
print(f"Risk Classification: {dossier['risk_classification']}")

assert dossier["health_score"] == 100
print("[★] HEALTH SCORE VERIFY: SUCCESS")
