# Define permitted command scopes for cluster roles
ROLE_PERMISSIONS = {
    "SYNC_OPERATOR": ["READ_TELEMETRY", "PROPOSE_CONSENSUS", "REQUEST_STATE_SYNC"],
    "SECURITY_AUDITOR": ["READ_AUDIT_LOG", "VERIFY_INTEGRITY_HASH"],
    "ROOT_ADMIN": ["ALL_COMMANDS"]
}

def can_execute_command(node_manifest, command):
    """
    Core Rule: Validate role vs. command scope.
    """
    if node_manifest.get("trust_status") != "TRUSTED":
        return False
        
    role = node_manifest.get("node_role")
    allowed_scope = ROLE_PERMISSIONS.get(role, [])
    
    return command in allowed_scope or "ALL_COMMANDS" in allowed_scope

if __name__ == "__main__":
    print(f"[i] Security check: SYNC_OPERATOR executing READ_TELEMETRY: {can_execute_command({'node_role': 'SYNC_OPERATOR', 'trust_status': 'TRUSTED'}, 'READ_TELEMETRY')}")
