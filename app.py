import streamlit as st
import sqlite3
from datetime import datetime
import pytz

st.set_page_config(page_title="Train Crossing AI", layout="wide")

# ------------------------------
# ROUTE
# ------------------------------
ROUTE = {
    "Jalna": 0,
    "Dinagaon": 10,
    "Badnapur": 20,
    "Karmad": 40,
    "Chikalthana": 55,
    "CPSN": 70
}

LOOP_STATIONS = ["Dinagaon", "Badnapur", "Karmad", "Chikalthana"]

# ------------------------------
# IST TIME
# ------------------------------
def get_now_ist():
    return datetime.now(pytz.timezone("Asia/Kolkata"))

# ------------------------------
# FETCH TRAINS
# ------------------------------
def fetch_trains():
    conn = sqlite3.connect("trains.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT train_no, name, type, dep_time, avg_speed,
               runs_sun, runs_mon, runs_tue, runs_wed, runs_thu, runs_fri, runs_sat,
               direction
        FROM trains
    """)

    rows = cur.fetchall()
    conn.close()

    now = get_now_ist()
    db_index = (now.weekday() + 1) % 7  # FIXED mapping

    trains = []

    for r in rows:
        running_today = r[5 + db_index] == 1

        h, m = map(int, r[3].split(":"))
        dep_min = h * 60 + m

        trains.append({
            "train_no": r[0],
            "name": r[1],
            "type": r[2],
            "dep_min": dep_min,
            "speed": r[4],
            "direction": r[12],
            "running_today": running_today
        })

    return trains

# ------------------------------
# SECTION + TIME LOGIC
# ------------------------------
def section_time(train):
    return (70 / train["speed"]) * 60

def is_in_section_now(train, now_min):
    end = train["dep_min"] + section_time(train)
    return train["dep_min"] <= now_min <= end

def will_enter_within_1hr(train, now_min):
    return now_min < train["dep_min"] <= now_min + 60

def get_position(train, now_min):
    dt = now_min - train["dep_min"]

    if dt < 0:
        return None

    dist = (train["speed"] * dt) / 60

    if train["direction"] == "UP":
        return min(70, dist)
    else:
        return max(0, 70 - dist)

def eta(pos, speed, station):
    dist = abs(ROUTE[station] - pos)
    return (dist / speed) * 60

# ------------------------------
# CONFLICT DETECTION
# ------------------------------
def find_conflicts(t1, others):
    results = []

    for t2 in others:

        if t2["direction"] == t1["direction"]:
            continue

        best_station = None
        best_diff = 999

        for stn in LOOP_STATIONS:
            e1 = eta(t1["pos"], t1["speed"], stn)
            e2 = eta(t2["pos"], t2["speed"], stn)

            diff = abs(e1 - e2)

            if diff < best_diff:
                best_diff = diff
                best_station = stn

        if best_diff < 5:  # relaxed for prediction
            results.append({
                "train": t2,
                "station": best_station,
                "eta_diff": round(best_diff, 2)
            })

    return sorted(results, key=lambda x: x["eta_diff"])

# ------------------------------
# DYNAMIC DELAY LOGIC
# ------------------------------
def decide(t1, t2, eta_diff):

    priority = {
        "VB": 5,
        "SF": 4,
        "JSHTB": 3,
        "EXP": 2,
        "PASS": 1,
        "DEMU": 1
    }

    p1 = priority.get(t1["type"], 2)
    p2 = priority.get(t2["type"], 2)

    SAFE_GAP = 4

    delay = max(0, SAFE_GAP - eta_diff)
    delay = max(delay, 1)
    delay = min(delay, 15)

    if p1 > p2:
        halt = t2["train_no"]
    elif p2 > p1:
        halt = t1["train_no"]
    else:
        halt = t1["train_no"] if t1["speed"] < t2["speed"] else t2["train_no"]

    return halt, round(delay, 2)

# ------------------------------
# UI
# ------------------------------
st.title("🚆 Train Crossing Predictor")

now = get_now_ist()
now_min = now.hour * 60 + now.minute

st.write(f"🕒 IST Time: {now.strftime('%H:%M')}")

direction_filter = st.radio(
    "Select Direction",
    ["UP (CPSN → Jalna)", "DOWN (Jalna → CPSN)"]
)

selected_direction = "UP" if "UP" in direction_filter else "DOWN"

all_trains = fetch_trains()
visible_trains = [t for t in all_trains if t["direction"] == selected_direction]

if "selected_train" not in st.session_state:
    st.session_state.selected_train = None

# ------------------------------
# TRAIN LIST
# ------------------------------
for i, t in enumerate(visible_trains):

    col1, col2, col3 = st.columns([2,6,1])

    col1.write(f"🚆 {t['train_no']}")

    if not t["running_today"]:
        col2.markdown(f"<span style='color:gray'>{t['name']} — ❌ Not Running Today</span>", unsafe_allow_html=True)

    elif is_in_section_now(t, now_min):
        col2.write(f"{t['name']} — ✅ In Section")

    elif will_enter_within_1hr(t, now_min):
        col2.markdown(f"<span style='color:blue'>{t['name']} — 🔵 Entering Soon</span>", unsafe_allow_html=True)

    else:
        col2.markdown(f"<span style='color:orange'>{t['name']} — ⚠️ Not in Section</span>", unsafe_allow_html=True)

    if col3.button("Analyze", key=f"{t['train_no']}_{i}"):
        if not t["running_today"]:
            st.warning("Train not running today")
        else:
            st.session_state.selected_train = t["train_no"]

# ------------------------------
# ANALYSIS
# ------------------------------
if st.session_state.selected_train:

    selected = next((x for x in all_trains if x["train_no"] == st.session_state.selected_train), None)

    if selected:

        st.divider()
        st.subheader(f"🔍 Analysis: {selected['train_no']}")

        pos = get_position(selected, now_min)

        if pos is None:
            pos = 0 if selected["direction"] == "UP" else 70

        selected["pos"] = pos

        st.success(f"📍 Estimated Position: {round(pos,2)} km")

        valid = []

        for t2 in all_trains:

            if not t2["running_today"]:
                continue

            if t2["direction"] == selected["direction"]:
                continue

            if not (is_in_section_now(t2, now_min) or will_enter_within_1hr(t2, now_min)):
                continue

            pos2 = get_position(t2, now_min)

            if pos2 is None:
                pos2 = 0 if t2["direction"] == "UP" else 70

            t2_copy = dict(t2)
            t2_copy["pos"] = pos2

            valid.append(t2_copy)

        conflicts = find_conflicts(selected, valid)

        if not conflicts:
            st.success("✅ No crossing conflict")

        else:
            main = conflicts[0]
            halt, delay = decide(selected, main["train"], main["eta_diff"])

            st.error("🚨 PRIMARY CONFLICT")
            st.write(f"⚔️ Train: {main['train']['train_no']}")
            st.write(f"📍 Station: {main['station']}")
            st.write(f"⏱ ETA diff: {main['eta_diff']} min")
            st.write(f"🚦 Halt: {halt}")
            st.write(f"⏳ Delay: {delay} min")
