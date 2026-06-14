def calculate_opportunity(analysis):

    gap = analysis.get("ipe_gap", 0)
    weakest = analysis.get("weakest_pillar", "General Improvement")

    program_map = {
        "Security": "Security Modernization Program",
        "Compliance Assurance": "Compliance Readiness Program",
        "Process Automation": "Operational Automation Program",
        "Data Integrity": "Data Governance Program",
        "Capital Readiness": "Capital Readiness Program",
        "Executive Visibility": "Executive Visibility Program",
        "Recruiting Infrastructure": "Recruiting Acceleration Program",
        "Advisor Productivity": "Advisor Productivity Program",
        "Revenue Operations": "Revenue Operations Program",
    }

    opportunity_value = round(gap * 1250, 0)

    return {
        "opportunity_value": opportunity_value,
        "projected_ipe_lift": gap,
        "recommended_program": program_map.get(
            weakest,
            "Business Optimization Program"
        )
    }
