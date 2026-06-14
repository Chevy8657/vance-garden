import json
from datetime import datetime

LEDGER_FILE = "/home/rick/pet_alpha/ledger.json"

class GovernanceScoreEngine:
    def calculate(self, integrity_score: float, checkpoints_passed: int, acknowledgment_complete: bool, audit_failures: int):
        score = 0

        score += integrity_score * 0.50
        score += checkpoints_passed * 10
        score += 20 if acknowledgment_complete else 0
        score -= audit_failures * 15

        final_score = max(0, min(100, round(score, 2)))
        
        # Tier classification
        if final_score >= 90:
            tier = "SOVEREIGN"
        elif final_score >= 70:
            tier = "COLLABORATIVE"
        else:
            tier = "RESTRICTED"
            
        return {
            "score": final_score,
            "tier": tier
        }

def log_event(event_type, payload):
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **payload
    }
    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"[+] Persistence Verified: {event_type} | Score: {payload['score']} | Tier: {payload['tier']}")
    return event

if __name__ == "__main__":
    engine = GovernanceScoreEngine()
    
    # Simulating DISTRICT_07 to hit exactly 84.5
    # (89 * 0.50) + (2 * 10) + 20 - (0 * 15) = 44.5 + 20 + 20 - 0 = 84.5
    result = engine.calculate(
        integrity_score=89.0,
        checkpoints_passed=2,
        acknowledgment_complete=True,
        audit_failures=0
    )

    log_event("GOVERNANCE_SCORE_CALCULATED", {
        "node_id": "DISTRICT_07",
        "score": result["score"],
        "tier": result["tier"]
    })
