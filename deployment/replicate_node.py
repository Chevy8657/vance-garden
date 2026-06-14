import shutil
# Seed new node from Baseline-A snapshot
SOURCE = "/home/rick/pet_alpha/builds/BASELINE-A"
TARGET = "/home/rick/pet_alpha/builds/NODE-BETA-001"

if not os.path.exists(SOURCE):
    print(f"[✕] ERROR: Baseline-A snapshot not found at {SOURCE}")
else:
    shutil.copytree(SOURCE, TARGET)
    print(f"[✓] REPLICATION COMPLETE: Node Beta initialized from Baseline-A.")
