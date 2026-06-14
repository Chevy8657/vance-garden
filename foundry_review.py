import json
from datetime import datetime

class ReviewEngine:
    def perform_review(self, plan_id):
        checkpoints = []
        try:
            with open("ledger.json", "r") as f:
                for line in f:
                    event = json.loads(line)
                    if event.get("event_type") == "WEEKLY_CHECKPOINT" and event.get("plan_id") == plan_id:
                        checkpoints.append(event)
        except FileNotFoundError:
            return "NO_LEDGER_FOUND"

        if not checkpoints:
            return "PENDING_DATA"

        avg_score = sum(c["performance_score"] for c in checkpoints) / len(checkpoints)
        audits_passed = all(c["audit_passed"] for c in checkpoints)

        verdict = "PROMOTE" if (avg_score >= 70 and audits_passed) else "CONTINUE_REMEDIATION"

        review = {
            "event_type": "THIRTY_DAY_REVIEW",
            "plan_id": plan_id,
            "node_id": checkpoints[0]["node_id"],
            "average_score": round(avg_score, 2),
            "audits_passed": audits_passed,
            "verdict": verdict,
            "timestamp": datetime.now().isoformat()
        }

        with open("ledger.json", "a") as f:
            f.write(json.dumps(review) + "\n")

        return review

if __name__ == "__main__":
    engine = ReviewEngine()
    result = engine.perform_review("RMP-20260602-001")
    if isinstance(result, dict):
        result["review_type"] = "STANDARD_30_DAY"
        print(json.dumps(result, indent=2))
    else:
        print(f"Status: {result}")
