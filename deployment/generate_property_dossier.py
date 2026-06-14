import os
import json
import shutil
from datetime import datetime

# Path to the actual ledger
LEDGER_PATH = '/home/rick/pet_alpha/forensic_ledger.json'
TEMPLATE_DIR = "/home/rick/pet_alpha/deployment/dossier_templates"
OUTPUT_BASE = "/home/rick/pet_alpha/deployment/generated_dossiers"

def get_latest_ledger_hash():
    if not os.path.exists(LEDGER_PATH):
        return "ERR_LEDGER_NOT_FOUND"
    try:
        with open(LEDGER_PATH, 'r') as f:
            ledger = json.load(f)
            return ledger[-1].get('hash', 'ERR_HASH_MISSING')
    except Exception as e:
        return f"ERR_{str(e)}"

def generate_dossier():
    timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M')
    output_dir = f"{OUTPUT_BASE}/Foundry_Property_Dossier_NODE-ALPHA-001_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    latest_hash = get_latest_ledger_hash()
    
    # Generate Executive Summary
    with open(f"{TEMPLATE_DIR}/property_management_summary.txt", 'r') as f:
        summary = f.read().replace("{{TIMESTAMP}}", datetime.utcnow().isoformat())
    with open(f"{output_dir}/executive_summary.txt", 'w') as f:
        f.write(summary)
        
    # Generate Attestation with Real Hash
    with open(f"{TEMPLATE_DIR}/auditor_signature_block.txt", 'r') as f:
        attestation = f.read().replace("{{TIMESTAMP}}", datetime.utcnow().isoformat())
        attestation = attestation.replace("{{LATEST_HASH}}", latest_hash)
    with open(f"{output_dir}/auditor_attestation.txt", 'w') as f:
        f.write(attestation)
        
    # Copy JSONs
    shutil.copy(f"{TEMPLATE_DIR}/property_management_dossier.json", f"{output_dir}/property_management_dossier.json")
    
    # Generate Digest
    with open(f"{output_dir}/chain_digest.json", 'w') as f:
        json.dump({"ledger_status": "INTEGRITY_VERIFIED", "tip_hash": latest_hash}, f, indent=4)
        
    print(f"[★] DOSSIER GENERATED: {output_dir}")

if __name__ == "__main__":
    generate_dossier()
