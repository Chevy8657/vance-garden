def generate_proposal(client, analysis, opportunity):

    return {
        "client_name": client.get("brokerage_name", "Client"),

        "current_ipe": analysis.get("overall_ipe", 0),
        "target_ipe": analysis.get("target_ipe", 0),

        "program": opportunity.get(
            "recommended_program",
            "Business Optimization Program"
        ),

        "investment": opportunity.get(
            "opportunity_value",
            0
        ),

        "projected_ipe_lift": opportunity.get(
            "projected_ipe_lift",
            0
        ),

        "timeline": "90 Days",

        "scope": analysis.get(
            "recommended_capabilities",
            []
        )
    }
