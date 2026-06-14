import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from unified_dossier import UnifiedDossier
from insurance_exporter import InsuranceExporter

# 1. Get internal dossier
aggregator = UnifiedDossier()
internal_dossier = aggregator.generate("PROP-001")

# 2. Export to Insurance View
exporter = InsuranceExporter()
insurance_dossier = exporter.export(internal_dossier)

print(json.dumps(insurance_dossier, indent=4))

# Validation
assert insurance_dossier["dossier_type"] == "INSURANCE_UNDERWRITING_DOSSIER"
assert insurance_dossier["underwriting_confidence"] == "HIGH"
print("[★] INSURANCE DOSSIER EXPORT VERIFY: SUCCESS")
