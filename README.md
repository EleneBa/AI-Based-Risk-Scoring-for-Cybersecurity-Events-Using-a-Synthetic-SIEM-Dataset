# AI Risk Scoring (Synthetic SIEM Event Dataset)

## Project Overview
This project generates a **synthetic SIEM event dataset** and trains a **machine learning classification model**
to assign a **risk label** to security events: **Low / Medium / High**.

The pipeline is fully reproducible:
1) Generate labeled SIEM-like events (`src/generate_dataset.py`)
2) Train a classifier (`src/train_model.py`)
3) Evaluate model performance (`src/evaluate_model.py`)
4) Predict risk for a sample event (`src/predict_risk.py`)

---

## Folder Structure

- `src/`
  - `generate_dataset.py` — creates the dataset and assigns `risk_label`
  - `train_model.py` — trains the model and saves it to `reports/model.joblib`
  - `evaluate_model.py` — produces evaluation outputs (`metrics.txt`, `confusion_matrix.png`)
  - `predict_risk.py` — loads the saved model and prints a sample risk prediction
- `data/`
  - `siem_events.csv` — generated dataset (created by `src/generate_dataset.py`)
- `reports/`
  - `model.joblib` — saved trained pipeline/model (created by `src/train_model.py`)
  - `metrics.txt` — classification report (created by `src/evaluate_model.py`)
  - `confusion_matrix.png` — confusion matrix image (created by `src/evaluate_model.py`)

---

## Dataset Description

### Features (X)
Synthetic SIEM event features used for training:
- `event_type` (categorical): SIEM alert category (e.g., failed_login, malware_alert, data_exfiltration)
- `src_zone` (categorical): source network zone (internet/corp/vendor)
- `dst_zone` (categorical): destination zone (corp/dmz/prod)
- `event_count_10m` (numeric): count of similar events in last 10 minutes
- `unique_src_10m` (numeric): number of unique sources in last 10 minutes
- `asset_criticality` (1–5): importance of target asset
- `prior_incident_impact` (0–3): historical incident impact score
- `is_privileged_account` (0/1): whether involved account is privileged
- `geo_risk` (1–5): geolocation-based risk bucket (synthetic)

### Target (y)
- `risk_label`: {Low, Medium, High}

### Risk Label Logic
A deterministic risk score is computed from event attributes and mapped to:
- **Low**: score < 70
- **Medium**: 70 ≤ score < 140
- **High**: score ≥ 140

This provides an explainable and cybersecurity-relevant target suitable for SOC triage.

---

### Install Dependencies
Run the following inside the project environment (PyCharm Terminal):
```bash
pip install pandas numpy scikit-learn matplotlib joblib
