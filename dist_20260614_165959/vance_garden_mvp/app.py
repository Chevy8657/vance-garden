from flask import Flask, render_template, redirect, url_for, request
from vance_engine import VanceRecommendationEngine

app = Flask(__name__)
engine = VanceRecommendationEngine()



@app.route("/garden")
def garden():
    return render_template("landing.html")


@app.route("/request-access", methods=["POST"])
def request_access():
    import json
    from datetime import datetime

    lead_data = {
        "name": request.form.get("name"),
        "company": request.form.get("company"),
        "role": request.form.get("role"),
        "email": request.form.get("email"),
        "timestamp": datetime.now().isoformat()
    }

    with open("garden_leads.jsonl", "a") as f:
        f.write(json.dumps(lead_data) + "\n")

    return render_template("thank_you.html", lead=lead_data)


@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        summary=engine.get_dashboard_summary(),
        morning=engine.get_morning_brief(),
        reality_cards=engine.get_reality_cards(),
        action_packs=engine.get_action_packs(),
        ledger=engine.get_capacity_ledger(),
        change_manager=engine.get_change_manager(),
        work=engine.get_work_classification(),
        away=engine.get_while_away(),
    )


@app.route("/attention")
@app.route("/items")
@app.route("/reality")
def items_needing_attention():
    return render_template(
        "items_needing_attention.html",
        reality_cards=engine.get_reality_cards()
    )


@app.route("/plans")
@app.route("/actions")
def prebuilt_action_plans():
    return render_template(
        "prebuilt_action_plans.html",
        action_packs=engine.get_action_packs()
    )


@app.route("/plans/<action_pack_id>")
@app.route("/actions/<action_pack_id>")
def action_detail(action_pack_id):
    action_bundle = engine.get_action_with_reality(action_pack_id)
    if not action_bundle:
        return redirect(url_for("prebuilt_action_plans"))
    return render_template("action_detail.html", action_bundle=action_bundle)


@app.route("/approve/<action_pack_id>")
def approve_action(action_pack_id):
    decision = engine.record_decision(
        action_pack_id=action_pack_id,
        decision="implemented",
        approved_by="Broker Owner",
        notes="Reviewed, approved, and moved to Change Manager for implementation tracking.",
    )
    action_bundle = engine.get_action_with_reality(action_pack_id)
    return redirect(url_for("change_manager"))


@app.route("/change")
@app.route("/capacity")
def change_manager():
    return render_template(
        "change_manager.html",
        change_manager=engine.get_change_manager(),
        ledger=engine.get_capacity_ledger(),
        summary=engine.get_dashboard_summary(),
    )


@app.route("/away")
@app.route("/brief")
def while_you_were_away():
    return render_template(
        "while_you_were_away.html",
        away=engine.get_while_away()
    )


@app.route("/where-your-money-goes")
@app.route("/work")
def where_your_money_goes():
    change_manager = engine.get_change_manager()
    admin_drag_in_change_manager = any(
        change["title"] == "Administrative Drag Reduction Pack"
        for change in change_manager["changes"]
    )

    return render_template(
        "where_your_money_goes.html",
        work=engine.get_work_classification(),
        admin_drag_in_change_manager=admin_drag_in_change_manager
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
