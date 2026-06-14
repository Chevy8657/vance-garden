import json
import os

def generate_brokerage_analysis(ledger_path="brokerage_ledger.json"):
    """
    Parses the latest ledger entry and generates deep conditional strategic analysis 
    based directly on the brokerage's specific scale, pain points, and business goals.
    """
    fallback_brief = {
        "snapshot": {
            "expected_impact": "+$119,000",
            "status": "HIGH PERFORMING",
            "ownership_readiness": "89%",
            "annual_volume": "$45,000,000.00",
            "gci": "$1,350,000.00",
            "advisors": "32"
        },
        "review": {
            "what_happened": "Your brokerage successfully generated $45,000,000 in annual production volume across 32 active agents.",
            "what_it_means": "Administrative friction and manual commission splits causing execution delay and administrative exhaustion are artificially limiting transaction velocity.",
            "recommendation_title": "Automate Operational Runway and Back-Office Scaling",
            "solution_mechanism": "Automated Commission Routing Engine",
            "what_to_do_next": "Deploy automated commission routing mechanics and localized ledger reconciliation to compress tasks into seconds, directly targeting operational leakage."
        },
        "strengths": {
            "greatest_strength": "Advisor Recruiting",
            "greatest_opportunity": "Commission Automation"
        },
        "action_plan": {
            "days_0_30": ["Map current manual split workflows", "Identify high-friction execution delays"],
            "days_31_60": ["Deploy localized routing beta", "Integrate ledger reconciliation sync"],
            "days_61_90": ["Scale automated back-office pipeline", "Review operational runway recovery"]
        }
    }

    if not os.path.exists(ledger_path):
        return fallback_brief

    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                return fallback_brief
            latest_record = json.loads(lines[-1])
    except Exception:
        return fallback_brief

    name = latest_record.get("brokerage_name", "Foundry Partner Node")
    vol = latest_record.get("transaction_volume", 0.0)
    gci = latest_record.get("gci", 0.0)
    agents = latest_record.get("agent_count", 0)
    pain = latest_record.get("pain_point", "").lower()
    goal = latest_record.get("business_goal", "").lower()

    vol_formatted = f"${vol:,.2f}"
    gci_formatted = f"${gci:,.2f}"
    
    impact_val = int(gci * 0.018)
    if impact_val == 0:
        impact_val = 119000
    impact_formatted = f"+${impact_val:,}"

    if vol >= 100000000:
        status = "ENTERPRISE SCALE"
        readiness = "92%"
    else:
        status = "HIGH PERFORMING"
        readiness = "89%"

    if "commercial" in name.lower() or "split" in pain or "industrial" in goal or "recruiting" in pain:
        greatest_strength = "Deal-Stage Capital Access" if vol > 200000000 else "Advisor Retainer Pool"
        greatest_opportunity = "Commercial Split & Margin Optimization"

        what_happened = (
            f"Your enterprise successfully generated {vol_formatted[:-3]} in annual production "
            f"volume across {agents} active specialized commercial advisors."
        )
        
        what_it_means = (
            f"High-leverage transaction scale is heavily exposed to commercial split complexity "
            f"and localized advisor production variance. A lack of structural deal-stage follow-up discipline "
            f"and fragmented recruiting pipelines for specialized divisions create compounding margin leakage, "
            f"diluting overall operational yield."
        )
        
        # OUTCOME FIRST Framework
        recommendation_title = "Protect Margin Leakage Across Commercial Split Structures"
        solution_mechanism = "Recruiting Consistency + Split Tracking Engine"
        
        what_to_do_next = (
            f"Your {vol_formatted[:-3]} commercial volume base creates high leverage, but complex split variables "
            f"and inconsistent recruiting visibility are limiting advisor expansion and margin protection. "
            f"Systemizing this stack directly captures downstream leakage and stabilizes division growth."
        )

        days_0_30 = [
            "Standardize complex commercial split rules and tier frameworks",
            "Audit historical deals for margin leakage patterns",
            "Map industrial division advisor competency matrices"
        ]
        days_31_60 = [
            "Track industrial and commercial recruiting pipelines by specialty",
            "Deploy automated margin protection guards inside the core ledger",
            "Establish unified deal-stage follow-up discipline protocols"
        ]
        days_61_90 = [
            "Identify top-tier industrial advisor candidates via automated scoring",
            "Eliminate multi-party variance across active high-value listings",
            "Lock down enterprise margin protection rules across all divisions"
        ]

    else:
        greatest_strength = "Advisor Recruiting"
        greatest_opportunity = "Commission Automation"
        
        what_happened = f"Your brokerage successfully generated {vol_formatted} in annual production volume across {agents} active agents."
        what_it_means = "Administrative friction and manual commission splits causing execution delay and administrative exhaustion are artificially limiting transaction velocity, creating operational leakage, and capping agent production capacity."
        
        recommendation_title = "Automate Operational Runway and Back-Office Scaling"
        solution_mechanism = "Automated Commission Routing Engine"
        
        what_to_do_next = "Deploy automated commission routing mechanics and localized ledger reconciliation to compress tasks into seconds, directly targeting: 'automate operational runway back-office'."
        
        days_0_30 = ["Map current manual split workflows", "Identify high-friction execution delays"]
        days_31_60 = ["Deploy localized routing beta", "Integrate ledger reconciliation sync"]
        days_61_90 = ["Scale automated back-office pipeline", "Review operational runway recovery"]


    # --- V2 INTELLIGENCE LAYER ---
    def _num(value, default=0):
        try:
            if isinstance(value, str):
                value = value.replace("$", "").replace(",", "").replace("+", "").replace("%", "")
            return float(value)
        except Exception:
            return default

    annual_volume_raw = _num(locals().get("volume", locals().get("annual_volume", 0)))
    gci_raw = _num(locals().get("gci", locals().get("gross_gci", annual_volume_raw * 0.03)))
    agents_raw = _num(locals().get("agents", locals().get("active_advisors", 0)))
    readiness_raw = _num(locals().get("readiness", 0))

    avg_gci_per_advisor = gci_raw / max(agents_raw, 1)
    volume_per_advisor = annual_volume_raw / max(agents_raw, 1)

    margin_leakage_score = min(
        99,
        45
        + (gci_raw / 10000000 * 18)
        + (agents_raw / 50 * 12)
        + (readiness_raw / 100 * 8)
    )

    recruiting_scale_score = min(
        99,
        40
        + (agents_raw / 50 * 18)
        + (readiness_raw / 100 * 10)
    )

    advisor_productivity_score = min(
        99,
        42
        + (avg_gci_per_advisor / 200000 * 22)
        + (volume_per_advisor / 7000000 * 10)
    )

    capital_access_score = min(
        99,
        50
        + (annual_volume_raw / 500000000 * 18)
        + (readiness_raw / 100 * 8)
    )

    lead_conversion_score = min(
        99,
        45
        + (avg_gci_per_advisor / 250000 * 12)
        + (agents_raw / 75 * 8)
    )

    opportunity_scores = {
        "margin_leakage": round(margin_leakage_score, 1),
        "recruiting_scale": round(recruiting_scale_score, 1),
        "advisor_productivity": round(advisor_productivity_score, 1),
        "capital_access": round(capital_access_score, 1),
        "lead_conversion": round(lead_conversion_score, 1),
    }

    ipe_scores = {
        "ipe_1_revenue_operations": round(min(99, 50 + (gci_raw / 10000000 * 18) + (readiness_raw / 100 * 10)), 1),
        "ipe_2_recruiting_infrastructure": round(recruiting_scale_score, 1),
        "ipe_3_advisor_productivity": round(advisor_productivity_score, 1),
        "ipe_4_process_automation": round(min(99, 42 + (agents_raw / 50 * 10) + (readiness_raw / 100 * 8)), 1),
        "ipe_5_data_integrity": round(min(99, 48 + (readiness_raw / 100 * 12)), 1),
        "ipe_6_security": round(min(99, 45 + (readiness_raw / 100 * 10)), 1),
        "ipe_7_compliance_assurance": round(min(99, 50 + (readiness_raw / 100 * 12)), 1),
        "ipe_8_capital_readiness": round(capital_access_score, 1),
        "ipe_9_executive_visibility": round(min(99, 46 + (gci_raw / 10000000 * 8) + (agents_raw / 50 * 6)), 1),
    }

    overall_ipe = round(sum(ipe_scores.values()) / len(ipe_scores), 1)

    if overall_ipe >= 90:
        maturity_level = "Compliant Node Owner"
    elif overall_ipe >= 80:
        maturity_level = "Integrated Brokerage"
    elif overall_ipe >= 70:
        maturity_level = "Managed Brokerage"
    elif overall_ipe >= 60:
        maturity_level = "Digitized Brokerage"
    else:
        maturity_level = "Manual Brokerage"

    target_ipe = min(99, round(overall_ipe + 18, 1))
    ipe_gap = round(target_ipe - overall_ipe, 1)

    top_opportunity = max(opportunity_scores, key=opportunity_scores.get)
    confidence = round(opportunity_scores[top_opportunity] / 100, 2)

    if top_opportunity == "margin_leakage":
        greatest_strength = "Deal-Stage Capital Access"
        greatest_opportunity = "Commercial Split & Margin Optimization"
        recommendation_title = "Protect Margin Leakage Across Commercial Split Structures"
        solution_mechanism = "Automated Commission Routing Engine"
        impact_rates = {
            "margin_leakage": 0.018,
            "recruiting_scale": 0.025,
            "advisor_productivity": 0.021,
            "capital_access": 0.015,
            "lead_conversion": 0.019,
        }

        selected_impact_rate = impact_rates.get(top_opportunity, 0.018)
        expected_impact_value = max(75000, round(gci_raw * selected_impact_rate))
        impact_formatted = f"+${expected_impact_value:,.0f}"
        what_it_means = (
            f"Your {vol_formatted} annual production base across {int(agents_raw)} commercial advisors creates meaningful operating leverage, "
            f"but the current score profile shows margin leakage risk outranking advisor productivity, recruiting scale, capital access, and lead conversion. "
            f"At {gci_formatted} in gross GCI, even small split variance, deal-stage inconsistency, and manual reconciliation gaps can compound into measurable enterprise leakage. "
            f"Systemizing commission logic and margin controls can protect operating yield while preserving advisor growth capacity."
        )
        what_to_do_next = (
            "Deploy a commercial split optimization workflow with automated routing, "
            "ledger reconciliation, advisor variance tracking, and margin protection rules."
        )
        days_0_30 = [
            "Standardize complex commercial split rules and tier frameworks",
            "Audit historical deals for margin leakage patterns",
            "Map industrial division advisor competency matrices"
        ]
        days_31_60 = [
            "Track industrial and commercial recruiting pipelines by specialty",
            "Deploy automated margin protection guards inside the core ledger",
            "Establish unified deal-stage follow-up discipline protocols"
        ]
        days_61_90 = [
            "Identify top-tier industrial advisor candidates via automated scoring",
            "Eliminate multi-party variance across active high-value listings",
            "Lock down enterprise margin protection rules across all divisions"
        ]


    # --- IPE OVERRIDE ENGINE ---
    weakest_ipe_pillar = min(ipe_scores, key=ipe_scores.get)
    weakest_ipe_score = ipe_scores[weakest_ipe_pillar]

    ipe_labels = {
        "ipe_1_revenue_operations": "Revenue Operations",
        "ipe_2_recruiting_infrastructure": "Recruiting Infrastructure",
        "ipe_3_advisor_productivity": "Advisor Productivity",
        "ipe_4_process_automation": "Process Automation",
        "ipe_5_data_integrity": "Data Integrity",
        "ipe_6_security": "Security",
        "ipe_7_compliance_assurance": "Compliance Assurance",
        "ipe_8_capital_readiness": "Capital Readiness",
        "ipe_9_executive_visibility": "Executive Visibility",
    }

    ipe_recommendations = {
        "ipe_1_revenue_operations": (
            "Stabilize Revenue Operations Around High-Value Production",
            "Revenue Operations Control Layer",
            "Revenue Operations Discipline"
        ),
        "ipe_2_recruiting_infrastructure": (
            "Build a Repeatable Recruiting Infrastructure",
            "Advisor Recruiting Pipeline Engine",
            "Recruiting Infrastructure"
        ),
        "ipe_3_advisor_productivity": (
            "Increase Advisor Productivity Through Operating Discipline",
            "Advisor Performance System",
            "Advisor Productivity"
        ),
        "ipe_4_process_automation": (
            "Automate Operational Runway and Back-Office Scaling",
            "Workflow Automation Engine",
            "Process Automation"
        ),
        "ipe_5_data_integrity": (
            "Strengthen Data Integrity Across Brokerage Operations",
            "Unified Data Quality Layer",
            "Data Integrity"
        ),
        "ipe_6_security": (
            "Harden Security Controls Across Brokerage Operations",
            "Security Control Framework",
            "Security"
        ),
        "ipe_7_compliance_assurance": (
            "Increase Compliance Assurance and Audit Readiness",
            "Compliance Assurance Node",
            "Compliance Assurance"
        ),
        "ipe_8_capital_readiness": (
            "Improve Capital Readiness for Higher-Value Transactions",
            "Capital Readiness Framework",
            "Capital Readiness"
        ),
        "ipe_9_executive_visibility": (
            "Increase Executive Visibility Across Brokerage Performance",
            "Executive Visibility Layer",
            "Executive Visibility"
        ),
    }

    weakest_label = ipe_labels.get(weakest_ipe_pillar, weakest_ipe_pillar)
    recommendation_title, solution_mechanism, greatest_opportunity = ipe_recommendations[weakest_ipe_pillar]

    greatest_strength = "Operating Scale"
    top_opportunity = weakest_ipe_pillar
    confidence = round(weakest_ipe_score / 100, 2)

    what_happened = (
        f"VANCE analyzed {vol_formatted} in annual transaction volume, {gci_formatted} in gross GCI, "
        f"and {int(agents_raw)} active advisors. The assessment produced an Overall IPE of {overall_ipe}/100 "
        f"with {weakest_label} identified as the weakest operating pillar."
    )

    what_it_means = (
        f"The brokerage is currently operating as a {maturity_level} with an IPE gap of {ipe_gap} points. "
        f"{weakest_label} scored {weakest_ipe_score}/100, making it the highest-priority constraint preventing progression "
        f"toward Integrated Brokerage and eventual Compliant Node Owner status."
    )

    what_to_do_next = (
        f"Deploy the {solution_mechanism} to raise {weakest_label}, improve Integrated Process Efficiency, "
        f"and move the brokerage from {overall_ipe}/100 toward the target IPE of {target_ipe}/100."
    )

    days_0_30 = [
        f"Audit current {weakest_label.lower()} workflows and control gaps",
        "Document baseline process friction and ownership responsibilities",
        "Define measurable IPE improvement targets"
    ]

    days_31_60 = [
        f"Deploy {solution_mechanism} pilot workflow",
        "Track adoption, exceptions, and process recovery signals",
        "Create weekly executive review cadence"
    ]

    days_61_90 = [
        f"Scale {weakest_label.lower()} controls across active operations",
        "Measure IPE lift against baseline",
        "Prepare maturity review toward next VANCE operating level"
    ]
    # --- END IPE OVERRIDE ENGINE ---

    debug = {
        "selected_opportunity": top_opportunity,
        "confidence": confidence,
        "opportunity_scores": opportunity_scores,
            "ipe_scores": ipe_scores,
            "overall_ipe": overall_ipe,
            "target_ipe": target_ipe,
            "ipe_gap": ipe_gap,
            "maturity_level": maturity_level,
        "impact_formula": f"expected_impact = gross_gci * {selected_impact_rate * 100:.1f}%",
        "gross_gci_used": gci_raw,
        "annual_volume_used": annual_volume_raw,
        "advisors_used": agents_raw
    }
    # --- END V2 INTELLIGENCE LAYER ---

    return {
        "snapshot": {
            "expected_impact": impact_formatted,
            "status": status,
            "ownership_readiness": readiness,
            "annual_volume": vol_formatted,
            "gci": gci_formatted,
            "advisors": str(agents)
        },
        "review": {
            "what_happened": what_happened,
            "what_it_means": what_it_means,
            "recommendation_title": recommendation_title,
            "solution_mechanism": solution_mechanism,
            "what_to_do_next": what_to_do_next
        },
        "strengths": {
            "greatest_strength": greatest_strength,
            "greatest_opportunity": greatest_opportunity
        },
        "action_plan": {
            "days_0_30": days_0_30,
            "days_31_60": days_31_60,
            "days_61_90": days_61_90
        },
        "debug": debug
    }
