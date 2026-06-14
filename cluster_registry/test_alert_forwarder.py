from alert_forwarder import stage_alert, process_outbox

# Mock incident from our previous Sprint 14
mock_incident = {
    "incident_id": "INC-888-999",
    "node_id": "NODE-STALE-003",
    "previous_status": "TRUSTED",
    "new_status": "STALE_QUARANTINED"
}

print("--- TESTING LOCAL-FIRST ALERT FORWARDER ---")
stage_alert(mock_incident)
process_outbox()
print("--- TEST COMPLETE: Audit trail secured. ---")
