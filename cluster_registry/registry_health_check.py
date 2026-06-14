import datetime

def mark_stale_nodes(registry_data, timeout_seconds=300):
    """Flags nodes as STALE if their 'last_seen' is beyond the timeout."""
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for node in registry_data:
        last_seen = datetime.datetime.fromisoformat(node['last_seen'])
        if (now - last_seen).total_seconds() > timeout_seconds:
            node['trust_status'] = "STALE"
            
    return registry_data
