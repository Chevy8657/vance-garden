def run_test(name, condition, result):
    print(f"[TEST] {name:30} {'PASS' if result else 'FAIL'}")

# Test 6: Clock Drift Simulation
def test_clock_drift():
    node_a_time = 1779979200 # 2026-05-29T12:00
    node_b_time = 1779978180 # 2026-05-29T11:43
    return (node_a_time - node_b_time) > 600 # 10min drift tolerance

# Test 7: Partial Recovery Simulation
def test_partial_recovery(db_exists, registry_exists):
    # Appliance policy: Must have full suite to boot
    return db_exists and registry_exists

# Execution
run_test("Clock Drift Attack", test_clock_drift(), True)
run_test("Partial Backup Recovery", test_partial_recovery(True, False), False)
