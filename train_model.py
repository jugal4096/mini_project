# ==============================
# TRAIN CROSSING PREDICTOR MODEL
# ==============================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# ------------------------------
# STEP 1: LOAD DATA
# ------------------------------
df = pd.read_csv("final_pairwise_dataset.csv")

print("Dataset Loaded Successfully")
print(df.head())

# ------------------------------
# STEP 2: PREPROCESSING
# ------------------------------

# Encode categorical column (station)
le_station = LabelEncoder()
df["station"] = le_station.fit_transform(df["station"])

# Encode target (decision)
le_decision = LabelEncoder()
df["decision"] = le_decision.fit_transform(df["decision"])

# ------------------------------
# STEP 3: FEATURES & TARGET
# ------------------------------
X = df[["train_1", "train_2", "station", "delay_after"]]
y = df["decision"]

# ------------------------------
# STEP 4: TRAIN TEST SPLIT
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------
# STEP 5: MODEL TRAINING
# ------------------------------
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# ------------------------------
# STEP 6: MODEL ACCURACY
# ------------------------------
accuracy = model.score(X_test, y_test)
print("\nModel Accuracy:", accuracy)

# ------------------------------
# STEP 7: SAMPLE PREDICTION
# ------------------------------
# Example input:
# train_1 = 17611
# train_2 = 11409
# station = "Karmad"
# delay = 15

station_input = "Karmad"
station_encoded = le_station.transform([station_input])[0]

sample = [[17611, 11409, station_encoded, 15]]

prediction = model.predict(sample)

result = le_decision.inverse_transform(prediction)

print("\nPrediction Result:")
print(f"Train 17611 vs 11409 at {station_input} → {result[0]}")