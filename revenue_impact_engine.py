def calculate_revenue_impact(client, analysis, opportunity):
    gci = float(client.get("gci", 0) or 0)
    investment = float(opportunity.get("opportunity_value", 0) or 0)
    ipe_gap = float(analysis.get("ipe_gap", 0) or 0)

    # Recovery model:
    # base operational recovery + gap-adjusted upside
    recovery_rate = 0.015 + (ipe_gap / 100 * 0.035)

    projected_revenue_lift = round(gci * recovery_rate, 0)

    payback_months = round((investment / max(projected_revenue_lift, 1)) * 12, 1)

    roi_percent = round(
        (projected_revenue_lift / max(investment, 1)) * 100,
        1
    )

    return {
        "projected_revenue_lift": projected_revenue_lift,
        "investment": investment,
        "payback_months": payback_months,
        "roi_percent": roi_percent,
        "current_ipe": analysis.get("overall_ipe", 0),
        "projected_ipe": analysis.get("target_ipe", 0),
        "projected_ipe_lift": ipe_gap,
        "recovery_rate": round(recovery_rate * 100, 2),
    }
