import random
import pandas as pd
from pathlib import Path

# Ensure data directory exists
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "siem_events.csv"

EVENT_TYPES = {
    "failed_login": 10,
    "port_scan": 25,
    "suspicious_dns": 30,
    "malware_alert": 45,
    "privilege_escalation": 70,
    "data_exfiltration": 85
}

ZONES = ["internet", "corp", "dmz", "vendor", "prod", "dev"]

def calculate_risk(row):
    score = EVENT_TYPES[row["event_type"]]
    score += row["event_count_10m"] * 2
    score += row["asset_criticality"] * 8
    score += row["prior_incident_impact"] * 10
    score += row["is_privileged_account"] * 15
    score += row["geo_risk"] * 3

    if score < 70:
        return "Low"
    elif score < 140:
        return "Medium"
    else:
        return "High"

def generate_data(rows=5000):
    data = []

    for _ in range(rows):
        record = {
            "event_type": random.choices(
                list(EVENT_TYPES.keys()),
                weights=[40, 25, 15, 10, 5, 5]
            )[0],
            "src_zone": random.choice(["internet", "corp", "vendor"]),
            "dst_zone": random.choice(["corp", "dmz", "prod"]),
            "event_count_10m": random.randint(1, 40),
            "unique_src_10m": random.randint(1, 20),
            "asset_criticality": random.randint(1, 5),
            "prior_incident_impact": random.randint(0, 3),
            "is_privileged_account": random.choice([0, 1]),
            "geo_risk": random.randint(1, 5)
        }

        record["risk_label"] = calculate_risk(record)
        data.append(record)

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_data()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset generated: {OUTPUT_FILE}")
    print(df["risk_label"].value_counts())
