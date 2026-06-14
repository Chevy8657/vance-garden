def generate_certification(analysis, verification):

    overall_ipe = analysis.get("overall_ipe", 0)
    maturity_level = analysis.get("maturity_level", "Unknown")
    compliance_node = analysis.get("compliance_node", {})
    node_readiness = compliance_node.get("node_readiness", 0)
    verification_score = verification.get("verification_score", 0)

    certified = (
        overall_ipe >= 90
        and node_readiness >= 90
        and verification_score >= 90
    )

    if certified:
        status = "Compliant Node Owner"
    elif verification_score >= 80 and node_readiness >= 75:
        status = "Node Certification Candidate"
    elif node_readiness >= 60:
        status = "Node Preparation In Progress"
    else:
        status = "Node Preparation Required"

    return {
        "status": status,
        "certified": certified,
        "current_maturity": maturity_level,
        "overall_ipe": overall_ipe,
        "node_readiness": node_readiness,
        "verification_score": verification_score,
        "requirements": [
            "Overall IPE must reach 90+",
            "Node Readiness must reach 90+",
            "Verification Score must reach 90+",
            "Security and Compliance controls must be validated",
            "Operational workflows must be documented and repeatable"
        ]
    }
