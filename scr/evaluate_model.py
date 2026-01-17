import pandas as pd
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "siem_events.csv"
MODEL_FILE = BASE_DIR / "reports" / "model.joblib"
REPORT_DIR = BASE_DIR / "reports"

df = pd.read_csv(DATA_FILE)

X = df.drop("risk_label", axis=1)
y = df["risk_label"]

_, X_test, _, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

model = joblib.load(MODEL_FILE)
y_pred = model.predict(X_test)

report = classification_report(y_test, y_pred)
with open(REPORT_DIR / "metrics.txt", "w") as f:
    f.write(report)

cm = confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"])
disp = ConfusionMatrixDisplay(cm, display_labels=["Low", "Medium", "High"])
disp.plot()
plt.savefig(REPORT_DIR / "confusion_matrix.png")

print("Evaluation completed. Metrics saved.")
