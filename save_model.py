# =========================
# SAVE TRAINED MODEL
# =========================

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("final_pairwise_dataset.csv")

# Encode station
le_station = LabelEncoder()
df["station"] = le_station.fit_transform(df["station"])

# Encode decision
le_decision = LabelEncoder()
df["decision"] = le_decision.fit_transform(df["decision"])

# Features & target
X = df[["train_1", "train_2", "station", "delay_after"]]
y = df["decision"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")