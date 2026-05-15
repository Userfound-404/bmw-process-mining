# models/train_predictive.py

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import LabelEncoder


# =========================================================
# Load Data
# =========================================================

df = pd.read_csv("data/event_log.csv")


# =========================================================
# Build order-level dataset (NO leakage features)
orders = df.groupby("case_id").agg(
    n_reworks=("activity", lambda x: (x == "Rework").sum()),
    n_steps=("activity", "count"),
    model_type=("model_type", "first"),
    supplier_id=("supplier_id", "first"),
    shift=("shift", "first"),
).reset_index()

# True duration (used ONLY for labeling)
duration = df.groupby("case_id")["duration_h"].sum()
orders["total_duration"] = duration.values

# Label
orders["is_late"] = (orders["total_duration"] > 120).astype(int)

# Encode categorical
for col in ["model_type", "supplier_id", "shift"]:
    orders[col] = LabelEncoder().fit_transform(orders[col])

# Features (NO leakage!)
features = ["n_reworks", "n_steps", "model_type", "supplier_id", "shift"]

X = orders[features]
y = orders["is_late"]

# =========================================================
# Train/Test Split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =========================================================
# Model
# =========================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# =========================================================
# Evaluation
# =========================================================

probs = model.predict_proba(X_test)[:, 1]
preds = model.predict(X_test)

print("\n=== MODEL PERFORMANCE ===")
print(f"ROC-AUC : {roc_auc_score(y_test, probs):.3f}")
print(f"Accuracy: {accuracy_score(y_test, preds):.3f}")


# =========================================================
# Risk Scoring
# =========================================================

orders["delay_risk"] = model.predict_proba(X)[:, 1]

high_risk = orders[orders["delay_risk"] > 0.7] \
    .sort_values("delay_risk", ascending=False)

high_risk.to_csv("data/high_risk_orders.csv", index=False)

print(f"\nSaved {len(high_risk)} high-risk orders → data/high_risk_orders.csv")