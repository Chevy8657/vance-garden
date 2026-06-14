def generate_verification(program):

    milestones = program.get("milestones", [])

    completed = sum(
        1 for m in milestones
        if m.get("complete")
    )

    total = max(len(milestones), 1)

    verification_score = round(
        (completed / total) * 100,
        1
    )

    verified = verification_score >= 80

    return {
        "verification_score": verification_score,
        "verified": verified,
        "verified_items": completed,
        "total_items": total,
        "status": (
            "Verified"
            if verified
            else "Pending Verification"
        )
    }
