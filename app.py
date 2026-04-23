# ==========================
# TRAIN CROSSING PREDICTOR UI
# ==========================

import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv("final_pairwise_dataset.csv")

# Encode
le_station = LabelEncoder()
df["station"] = le_station.fit_transform(df["station"])

le_decision = LabelEncoder()
df["decision"] = le_decision.fit_transform(df["decision"])

X = df[["train_1", "train_2", "station", "delay_after"]]
y = df["decision"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# --------------------------
# UI
# --------------------------
st.title("🚆 Train Crossing Predictor")

train1 = st.number_input("Enter Train 1 Number")
train2 = st.number_input("Enter Train 2 Number")

station = st.selectbox("Select Station", 
                       le_station.inverse_transform(df["station"].unique()))

delay = st.slider("Delay (minutes)", 0, 60)

# --------------------------
# PREDICT
# --------------------------
if st.button("Predict"):
    station_encoded = le_station.transform([station])[0]
    
    sample = [[train1, train2, station_encoded, delay]]
    
    pred = model.predict(sample)
    result = le_decision.inverse_transform(pred)
    
    st.success(f"Prediction: {result[0]}")