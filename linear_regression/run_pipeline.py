import sys
import traceback
import subprocess

print("\n🚀 Starting FULL ML PIPELINE\n")

try:
    # -------------------------
    # 1. INIT DB TABLES
    # -------------------------
    print("Initializing DB tables...")
    from data.db.init_db import init_feature_tables
    init_feature_tables()
    print("DB tables ready------------>>\n")

    # -------------------------
    # 2. LOAD RAW DATA
    # -------------------------
    print("Loading raw data into DB...")
    from data.db.load_data_to_db import load_csv_to_db
    load_csv_to_db()
    print("Raw data loaded------------->\n")

    # -------------------------
    # 3. CREATE FEATURE VIEW
    # -------------------------
    print("Creating feature view...")
    from src.features.feature_view_housing_v1 import create_feature_view
    create_feature_view()
    print("Feature view created------------------>\n")

    # -------------------------
    # 4. TRAIN MODEL
    # -------------------------
    print("Training model...")
    from src.training.train import train
    train()
    print("Model trained & saved---------------->\n")

    # -------------------------
    # 5. TEST INFERENCE
    # -------------------------
    print("Running inference test...")

    subprocess.run(
        [sys.executable, "-m", "src.inference.test_housing_predict"],
        check=True
    )

    print("\PIPELINE COMPLETED SUCCESSFULLY\n")

except Exception as e:
    print("\n❌ PIPELINE FAILED\n")
    traceback.print_exc()
    sys.exit(1)
