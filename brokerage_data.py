import json
from pathlib import Path

BROKERAGE_LEDGER = Path("/home/rick/pet_alpha/brokerage_ledger.json")

def load_brokerage_records(path=BROKERAGE_LEDGER):
    records = []
    if not Path(path).exists():
        return records

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                continue

    return records

def get_latest_brokerage(path=BROKERAGE_LEDGER):
    records = load_brokerage_records(path)
    return records[-1] if records else {}
