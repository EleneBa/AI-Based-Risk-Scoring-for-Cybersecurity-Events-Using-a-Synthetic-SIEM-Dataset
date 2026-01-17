import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "siem_events.csv"
MODEL_FILE = BASE_DIR / "reports" / "model.joblib"
MODEL_FILE.parent.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

X = df.drop("risk_label", axis=1)
y = df["risk_label"]

categorical_features = ["event_type", "src_zone", "dst_zone"]
numeric_features = [col for col in X.columns if col not in categorical_features]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced"
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", model)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

pipeline.fit(X_train, y_train)
joblib.dump(pipeline, MODEL_FILE)

print("Model trained and saved to reports/model.joblib")
