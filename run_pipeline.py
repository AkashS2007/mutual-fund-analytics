"""
Master execution script for Bluestock Mutual Fund Analytics Pipeline.
Runs all ETL steps in sequence.
"""
import subprocess
import sys

def run(script):
    print(f"\n{'='*50}")
    print(f"▶ Running {script}...")
    print('='*50)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"❌ {script} failed!")
        sys.exit(1)
    print(f"✅ {script} complete")

if __name__ == "__main__":
    print("🚀 Bluestock MF Analytics Pipeline Starting...")
    run("data_ingestion.py")
    run("live_nav_fetch.py")
    run("data_cleaning.py")
    run("load_to_db.py")
    run("validate_amfi_codes.py")
    print("\n🎉 Pipeline complete! Database ready at bluestock_mf.db")