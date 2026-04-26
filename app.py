import streamlit as st
import joblib

st.set_page_config(page_title="Train Crossing AI", layout="centered")

st.title("🚆 Train Crossing Predictor")
st.caption("Train 1: Jalna → CPSN | Train 2: CPSN → Jalna")

# ------------------------------
# ROUTE (WITH DINAGAON)
# ------------------------------
ROUTE = {
    "Jalna": 0,
    "Dinagaon": 10,
    "Badnapur": 20,
    "Karmad": 40,
    "Chikalthana": 55,
    "Aurangabad": 70
}

STATIONS = list(ROUTE.keys())
LOOP_STATIONS = ["Badnapur", "Karmad", "Chikalthana"]

# ------------------------------
# LOAD MODEL
# ------------------------------
try:
    model_decision = joblib.load("model_decision.pkl")
    model_delay = joblib.load("model_delay.pkl")
    le_station = joblib.load("le_station.pkl")
    le_decision = joblib.load("le_decision.pkl")
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ------------------------------
# PRIORITY
# ------------------------------
def priority(t):
    return {"Passenger": 1, "Express": 2, "Superfast": 3}[t]

# ------------------------------
# POSITION
# ------------------------------
def pos_train1(station, dist):
    # Jalna → CPSN (forward)
    return ROUTE[station] - dist

def pos_train2(station, dist):
    # CPSN → Jalna (reverse)
    return ROUTE[station] + dist

# ------------------------------
# MEETING POINT
# ------------------------------
def meeting_point(p1, p2):
    meet = (p1 + p2) / 2
    station = min(LOOP_STATIONS, key=lambda s: abs(ROUTE[s] - meet))
    return station, meet

# ------------------------------
# NEAREST LOOP
# ------------------------------
def nearest_loop(pos):
    stn = min(LOOP_STATIONS, key=lambda s: abs(ROUTE[s] - pos))
    return stn, abs(pos - ROUTE[stn])

# ------------------------------
# RULE SCORE
# ------------------------------
def rule_score(d1, d2, delay1, delay2, p1, p2, prox1, prox2):
    s1 = s2 = 0

    if d1 < d2:
        s1 += 2
    elif d2 < d1:
        s2 += 2

    if prox1 < prox2:
        s1 += 1
    elif prox2 < prox1:
        s2 += 1

    if p1 > p2:
        s1 += 2
    elif p2 > p1:
        s2 += 2

    if delay1 < delay2:
        s1 += 1
    else:
        s2 += 1

    return s1, s2

# ------------------------------
# HYBRID DECISION
# ------------------------------
def hybrid_decision(ml, s1, s2):
    if ml == "HALT_TRAIN1":
        s2 += 2
    elif ml == "HALT_TRAIN2":
        s1 += 2

    return "Train 1 PASS, Train 2 HALT" if s1 > s2 else "Train 2 PASS, Train 1 HALT"

# ------------------------------
# PREDICT
# ------------------------------
def predict(t1, t2, s1, s2, d1, d2, delay1, delay2, type1, type2):

    p1 = pos_train1(s1, d1)
    p2 = pos_train2(s2, d2)

    # must be facing each other
    if p1 >= p2:
        return {"info": "No crossing (positions not opposing)"}

    station, meet = meeting_point(p1, p2)

    dist1 = abs(p1 - meet)
    dist2 = abs(p2 - meet)

    loop1, prox1 = nearest_loop(p1)
    loop2, prox2 = nearest_loop(p2)

    pr1 = priority(type1)
    pr2 = priority(type2)

    s1_score, s2_score = rule_score(dist1, dist2, delay1, delay2, pr1, pr2, prox1, prox2)

    if station not in le_station.classes_:
        return {"error": f"{station} not in model"}

    enc = le_station.transform([station])[0]

    sample = [[t1, t2, enc, delay1]]

    ml = model_decision.predict(sample)
    ml = le_decision.inverse_transform(ml)[0]

    delay_pred = model_delay.predict(sample)

    final = hybrid_decision(ml, s1_score, s2_score)

    return {
        "station": station,
        "meeting_km": round(meet, 2),
        "ml": ml,
        "scores": (s1_score, s2_score),
        "final": final,
        "delay": int(delay_pred[0])
    }

# ------------------------------
# UI
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚆 Train 1 (J → CPSN)")
    t1 = st.number_input("Train 1 No", key="t1")
    s1 = st.selectbox("Approaching Station", STATIONS, key="s1")
    d1 = st.slider("Distance (km)", 0, 20, key="d1")
    delay1 = st.slider("Delay", 0, 60, key="delay1")
    type1 = st.selectbox("Type", ["Passenger", "Express", "Superfast"], key="type1")

with col2:
    st.subheader("🚆 Train 2 (CPSN → J)")
    t2 = st.number_input("Train 2 No", key="t2")
    s2 = st.selectbox("Approaching Station", STATIONS, key="s2")
    d2 = st.slider("Distance (km)", 0, 20, key="d2")
    delay2 = st.slider("Delay", 0, 60, key="delay2")
    type2 = st.selectbox("Type", ["Passenger", "Express", "Superfast"], key="type2")

if st.button("⚡ Predict Crossing"):

    result = predict(t1, t2, s1, s2, d1, d2, delay1, delay2, type1, type2)

    if "info" in result:
        st.info(result["info"])
    elif "error" in result:
        st.error(result["error"])
    else:
        st.success("Prediction Complete")

        st.write(f"📍 Crossing Station: **{result['station']}**")
        st.write(f"📏 Meeting Point: **{result['meeting_km']} km**")
        st.write(f"🤖 ML Decision: {result['ml']}")
        st.write(f"⚖️ Scores: T1={result['scores'][0]}, T2={result['scores'][1]}")
        st.write(f"🚦 Final Decision: {result['final']}")
        st.write(f"⏱ Delay: {result['delay']} min")