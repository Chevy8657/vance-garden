def _num(value, default=0):
    try:
        if isinstance(value, str):
            value = value.replace("$", "").replace(",", "").replace("+", "").replace("%", "")
        return float(value)
    except Exception:
        return default


def analyze_client_record(client):
    volume = _num(client.get("transaction_volume", 0))
    gci = _num(client.get("gci", 0))
    agents = _num(client.get("agent_count", 0))
    readiness = 62

    avg_gci_per_advisor = gci / max(agents, 1)
    volume_per_advisor = volume / max(agents, 1)

    ipe_scores = {
        "Revenue Operations": round(min(99, 50 + (gci / 10000000 * 18) + (readiness / 100 * 10)), 1),
        "Recruiting Infrastructure": round(min(99, 40 + (agents / 50 * 18) + (readiness / 100 * 10)), 1),
        "Advisor Productivity": round(min(99, 42 + (avg_gci_per_advisor / 200000 * 22) + (volume_per_advisor / 7000000 * 10)), 1),
        "Process Automation": round(min(99, 42 + (agents / 50 * 10) + (readiness / 100 * 8)), 1),
        "Data Integrity": round(min(99, 48 + (readiness / 100 * 12)), 1),
        "Security": round(min(99, 45 + (readiness / 100 * 10)), 1),
        "Compliance Assurance": round(min(99, 50 + (readiness / 100 * 12)), 1),
        "Capital Readiness": round(min(99, 50 + (volume / 500000000 * 18) + (readiness / 100 * 8)), 1),
        "Executive Visibility": round(min(99, 46 + (gci / 10000000 * 8) + (agents / 50 * 6)), 1),
    }

    overall_ipe = round(sum(ipe_scores.values()) / len(ipe_scores), 1)
    weakest_pillar = min(ipe_scores, key=ipe_scores.get)
    weakest_score = ipe_scores[weakest_pillar]
    target_ipe = min(99, round(overall_ipe + 18, 1))
    ipe_gap = round(target_ipe - overall_ipe, 1)

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

    recommendations = {
        "Security": "Harden Security Controls Across Brokerage Operations",
        "Compliance Assurance": "Increase Compliance Assurance and Audit Readiness",
        "Process Automation": "Automate Operational Runway and Back-Office Scaling",
        "Data Integrity": "Strengthen Data Integrity Across Brokerage Operations",
        "Capital Readiness": "Improve Capital Readiness for Higher-Value Transactions",
        "Executive Visibility": "Increase Executive Visibility Across Brokerage Performance",
        "Recruiting Infrastructure": "Build a Repeatable Recruiting Infrastructure",
        "Advisor Productivity": "Increase Advisor Productivity Through Operating Discipline",
        "Revenue Operations": "Stabilize Revenue Operations Around High-Value Production",
    }

    capabilities = {
        "Security": [
            "Multi-Factor Authentication",
            "Single Sign-On",
            "Role-Based Access Control",
            "Centralized Audit Logging",
            "Security Monitoring"
        ],
        "Compliance Assurance": [
            "Compliance Workflow Engine",
            "Audit Evidence Repository",
            "Policy Management",
            "Exception Tracking",
            "Compliance Reporting"
        ],
        "Process Automation": [
            "Workflow Automation",
            "Task Routing",
            "Automated Notifications",
            "Process Monitoring",
            "Operational Dashboards"
        ],
        "Data Integrity": [
            "Data Validation Rules",
            "Duplicate Detection",
            "Data Governance Controls",
            "Master Record Management",
            "Data Quality Monitoring"
        ],
        "Capital Readiness": [
            "Capital Pipeline Tracking",
            "Deal Packaging Standards",
            "Investor Reporting",
            "Capital Relationship Management",
            "Funding Readiness Reviews"
        ],
        "Executive Visibility": [
            "Executive Dashboards",
            "KPI Monitoring",
            "Forecast Reporting",
            "Decision Support Analytics",
            "Leadership Review Workflows"
        ],
        "Recruiting Infrastructure": [
            "Candidate Pipeline Management",
            "Advisor Scorecards",
            "Recruiting Workflow Automation",
            "Talent Tracking",
            "Performance Benchmarking"
        ],
        "Advisor Productivity": [
            "Advisor Activity Tracking",
            "Performance Dashboards",
            "Productivity Benchmarking",
            "Coaching Workflows",
            "Production Analytics"
        ],
        "Revenue Operations": [
            "Revenue Scorecards",
            "Production Tracking",
            "Revenue Forecasting",
            "Pipeline Monitoring",
            "Operating Cadence Management"
        ],
    }

    action_plans = {
        "Security": {
            "days_0_30": ["Inventory user accounts and privileged access", "Review authentication and password policies", "Identify critical security exposure points"],
            "days_31_60": ["Deploy MFA and access-control standards", "Implement centralized audit logging", "Establish incident response procedures"],
            "days_61_90": ["Conduct security validation review", "Measure risk reduction against baseline", "Prepare executive security readiness report"],
        },
        "Compliance Assurance": {
            "days_0_30": ["Document compliance obligations", "Review record retention requirements", "Identify audit readiness gaps"],
            "days_31_60": ["Implement compliance workflows", "Create audit evidence repository", "Establish compliance review cadence"],
            "days_61_90": ["Run internal compliance assessment", "Validate controls and procedures", "Prepare external audit readiness package"],
        },
        "Process Automation": {
            "days_0_30": ["Map manual workflows", "Identify operational bottlenecks", "Prioritize automation candidates"],
            "days_31_60": ["Deploy workflow automation pilots", "Reduce manual reconciliation tasks", "Measure time savings"],
            "days_61_90": ["Scale automation platform-wide", "Monitor operational throughput", "Review productivity gains"],
        },
        "Data Integrity": {
            "days_0_30": ["Audit data quality issues", "Identify duplicate records", "Document data ownership"],
            "days_31_60": ["Implement validation controls", "Deploy data cleanup process", "Monitor integrity metrics"],
            "days_61_90": ["Establish governance standards", "Measure quality improvements", "Review data reliability score"],
        },
        "Capital Readiness": {
            "days_0_30": ["Map capital partner relationships", "Audit deal packaging quality", "Identify financing readiness gaps"],
            "days_31_60": ["Standardize capital package templates", "Create capital partner tracking", "Deploy deal-readiness review process"],
            "days_61_90": ["Review capital conversion outcomes", "Prioritize high-value capital relationships", "Prepare capital readiness score update"],
        },
        "Executive Visibility": {
            "days_0_30": ["Define executive operating metrics", "Map leadership reporting gaps", "Identify missing visibility signals"],
            "days_31_60": ["Deploy executive KPI dashboard", "Create weekly decision review cadence", "Standardize risk and opportunity reporting"],
            "days_61_90": ["Automate executive reporting workflow", "Review leadership visibility improvements", "Prepare management system review"],
        },
        "Recruiting Infrastructure": {
            "days_0_30": ["Map advisor gaps by specialty", "Define ideal advisor candidate profiles", "Create recruiting pipeline stages"],
            "days_31_60": ["Launch candidate scoring workflow", "Track outreach and follow-up activity", "Assign recruiting ownership by market segment"],
            "days_61_90": ["Review recruiting conversion rates", "Prioritize top advisor targets", "Build repeatable recruiting cadence"],
        },
        "Advisor Productivity": {
            "days_0_30": ["Baseline production by advisor", "Identify underutilized advisor capacity", "Define productivity benchmarks"],
            "days_31_60": ["Launch advisor performance dashboard", "Implement activity tracking cadence", "Coach advisors below benchmark"],
            "days_61_90": ["Review productivity lift", "Standardize winning advisor behaviors", "Scale advisor performance protocols"],
        },
        "Revenue Operations": {
            "days_0_30": ["Map production workflows by advisor and division", "Identify revenue leakage points", "Standardize weekly operating review cadence"],
            "days_31_60": ["Deploy revenue operations scorecards", "Implement advisor contribution tracking", "Align operating cadence to production goals"],
            "days_61_90": ["Lock recurring revenue review protocols", "Benchmark producer contribution by segment", "Prepare revenue operations maturity review"],
        },
    }

    plan = action_plans.get(weakest_pillar, {
        "days_0_30": ["Assess operating constraints"],
        "days_31_60": ["Deploy improvement initiative"],
        "days_61_90": ["Measure results and optimize"],
    })

    node_required_scores = [
        ipe_scores["Security"],
        ipe_scores["Compliance Assurance"],
        ipe_scores["Data Integrity"],
        ipe_scores["Executive Visibility"],
    ]

    node_readiness = round(
        sum(min(score, 90) for score in node_required_scores)
        / (90 * len(node_required_scores))
        * 100,
        1
    )

    compliance_node = {
        "status": (
            "Node Ready" if overall_ipe >= 90 and ipe_scores["Security"] >= 90 and ipe_scores["Compliance Assurance"] >= 90
            else "Node Preparation Required"
        ),
        "node_readiness": node_readiness,
        "security_score": ipe_scores["Security"],
        "compliance_score": ipe_scores["Compliance Assurance"],
        "data_integrity_score": ipe_scores["Data Integrity"],
        "executive_visibility_score": ipe_scores["Executive Visibility"],
        "requirements": [
            "Security score must reach 90+",
            "Compliance Assurance score must reach 90+",
            "Data Integrity controls must be verified",
            "Executive Visibility must support audit-ready reporting",
            "Operational workflows must be documented and repeatable"
        ],
        "next_node_action": (
            "Proceed to Compliant Node Owner validation"
            if overall_ipe >= 90 and ipe_scores["Security"] >= 90 and ipe_scores["Compliance Assurance"] >= 90
            else "Prioritize Security, Compliance Assurance, Data Integrity, and Executive Visibility controls"
        )
    }

    return {
        "ipe_scores": ipe_scores,
        "overall_ipe": overall_ipe,
        "target_ipe": target_ipe,
        "ipe_gap": ipe_gap,
        "maturity_level": maturity_level,
        "weakest_pillar": weakest_pillar,
        "weakest_score": weakest_score,
        "recommendation": recommendations.get(weakest_pillar, "Improve Operating Discipline"),
        "action_plan": plan,
        "recommended_capabilities": capabilities.get(weakest_pillar, []),
        "compliance_node": compliance_node,
    }
