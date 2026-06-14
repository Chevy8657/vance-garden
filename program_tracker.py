def generate_program_tracker(analysis, proposal):
    program = proposal.get("program", "Business Optimization Program")

    milestones = [
        {"name": "Assessment Complete", "complete": True},
        {"name": "Roadmap Generated", "complete": True},
        {"name": "Proposal Prepared", "complete": True},
        {"name": "Implementation Started", "complete": False},
        {"name": "Controls Deployed", "complete": False},
        {"name": "Verification Review", "complete": False},
    ]

    completed = sum(1 for m in milestones if m["complete"])
    completion = round((completed / len(milestones)) * 100, 1)

    return {
        "program": program,
        "status": "Proposal Ready",
        "completion": completion,
        "milestones": milestones,
        "expected_ipe_lift": proposal.get("projected_ipe_lift", 0),
        "target_ipe": proposal.get("target_ipe", analysis.get("target_ipe", 0)),
    }
