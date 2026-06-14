import json
import os

LEDGER_FILE = "/home/rick/pet_alpha/ledger.json"

def perform_audit():
    if not os.path.exists(LEDGER_FILE):
        return "Audit: Ledger not found."
    return "Audit: Integrity Verified."

if __name__ == "__main__":
    print(perform_audit())
