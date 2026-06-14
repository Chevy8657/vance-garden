import json
from datetime import datetime

LEDGER_FILE = "/home/rick/pet_alpha/ledger.json"
DISCOUNT_PER_RECRUIT = 10  # 10%

class ReferralEngine:
    def calculate_discount(self, agent_id: str, base_fee: float, recruits_count: int):
        # Calculate discount capped at 100%
        discount_percent = min(recruits_count * DISCOUNT_PER_RECRUIT, 100)
        
        # Apply discount to base fee
        discount_multiplier = 1 - (discount_percent / 100.0)
        adjusted_fee = round(base_fee * discount_multiplier, 2)
        
        # Evaluate loop status
        free_at_10 = recruits_count >= 10

        return {
            "agent_id": agent_id,
            "recruits_count": recruits_count,
            "discount_percent": discount_percent,
            "adjusted_fee": adjusted_fee,
            "free_at_10": free_at_10
        }

def log_event(event_type, payload):
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **payload
    }
    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"[+] Revenue Signal Verified: {event_type} | Agent: {payload['agent_id']} | Adjusted Fee: ${payload['adjusted_fee']}")
    return event

if __name__ == "__main__":
    engine = ReferralEngine()
    
    # Simulating AGENT_001 with 4 recruits on a $300 base fee
    # Expected adjusted fee: $180
    result = engine.calculate_discount(
        agent_id="AGENT_001",
        base_fee=300.0,
        recruits_count=4
    )

    log_event("REFERRAL_DISCOUNT_CALCULATED", result)
