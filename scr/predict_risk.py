import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_FILE = BASE_DIR / "reports" / "model.joblib"

model = joblib.load(MODEL_FILE)

sample_event = pd.DataFrame([{
    "event_type": "privilege_escalation",
    "src_zone": "corp",
    "dst_zone": "prod",
    "event_count_10m": 15,
    "unique_src_10m": 3,
    "asset_criticality": 5,
    "prior_incident_impact": 2,
    "is_privileged_account": 1,
    "geo_risk": 4
}])

prediction = model.predict(sample_event)[0]
print(f"Predicted Risk Level: {prediction}")
