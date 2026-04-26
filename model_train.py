# =========================
# TRAIN & SAVE MODELS
# =========================

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("final_pairwise_dataset.csv")

# Encode
le_station = LabelEncoder()
df["station"] = le_station.fit_transform(df["station"])

le_decision = LabelEncoder()
df["decision"] = le_decision.fit_transform(df["decision"])

# Features
X = df[["train_1", "train_2", "station", "delay_after"]]

# Targets
y_decision = df["decision"]
y_delay = df["delay_after"]

# Models
model_decision = DecisionTreeClassifier()
model_delay = DecisionTreeRegressor()

model_decision.fit(X, y_decision)
model_delay.fit(X, y_delay)

# Save
joblib.dump(model_decision, "model_decision.pkl")
joblib.dump(model_delay, "model_delay.pkl")
joblib.dump(le_station, "le_station.pkl")
joblib.dump(le_decision, "le_decision.pkl")

print("✅ Models saved successfully")