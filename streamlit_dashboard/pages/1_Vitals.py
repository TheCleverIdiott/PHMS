import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from modules.alerts import check_alerts
from modules.logger import log_data
from modules.firebase_export import push_to_firebase
import os
import plotly.graph_objects as go


# ---------- Auth Check ----------
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("🔒 Please login to access the dashboard.")
    st.stop()

# ---------- Page Config ----------
st.set_page_config(page_title="Vitals Monitoring", layout="wide", page_icon="📊")
st_autorefresh(interval=10000, key="auto_refresh")

# ---------- Stylish Header ----------
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #2E86C1;'>📊 Vitals Monitoring Dashboard</h1>
        <p style='font-size: 17px;'>Real-time monitoring of vital signs with alert detection and secure data logging.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

# ---------- Sidebar Controls ----------
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")
    with st.expander("🛠️ Simulate Vitals", expanded=True):
        heart_rate = st.slider("Heart Rate (BPM)", 50, 150, 75)
        spo2 = st.slider("SpO2 (%)", 85, 100, 98)
        body_temp = st.slider("Body Temp (°C)", 35.0, 40.0, 36.8, step=0.1)
        room_temp = st.slider("Room Temp (°C)", 20.0, 40.0, 28.5, step=0.1)
        humidity = st.slider("Humidity (%)", 20, 100, 55)
    st.markdown("---")
    firebase_enabled = st.checkbox("📤 Export to Firebase", value=False)

# ---------- Display Vitals ----------
st.markdown("### 🧾 Current Vitals Summary")
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("❤️ Heart Rate", f"{heart_rate} BPM")
    col2.metric("🩸 SpO₂", f"{spo2} %")
    col3.metric("🌡️ Body Temp", f"{body_temp} °C")
    col4.metric("🏠 Room Temp", f"{room_temp} °C")
    col5.metric("💧 Humidity", f"{humidity} %")

# ---------- Alert Check ----------
alerts = check_alerts(heart_rate, spo2, body_temp)
if alerts:
    st.error("⚠️ Alerts Triggered")
    for alert in alerts:
        st.warning(alert)
else:
    st.success("✅ All vitals are within the healthy range.")

# ---------- Log Data ----------
st.markdown("### 📥 Log & Export Vitals")
if st.button("Log Vitals Now"):
    log_data(heart_rate, spo2, body_temp, room_temp, humidity)
    if firebase_enabled:
        push_to_firebase(heart_rate, spo2, body_temp, room_temp, humidity)
    st.toast("✅ Vitals logged successfully!")

# ---------- Load & Display Data ----------
log_file = "vitals_log.csv"
if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
    df = pd.DataFrame(columns=["Time", "HeartRate", "SpO2", "BodyTemp", "RoomTemp", "Humidity"])
    df.to_csv(log_file, index=False)
else:
    df = pd.read_csv(log_file)

# ---------- Charts ----------
st.markdown("### 📈 Vitals Trend Overview")

# Summary Stats
latest_row = df.tail(1)
if not latest_row.empty:
    st.markdown("#### 🔎 Recent Snapshot")
    colT1, colT2, colT3 = st.columns(3)
    colT1.info(f"**Avg Heart Rate:** {int(df['HeartRate'].mean())} BPM")
    colT2.info(f"**Avg SpO₂:** {round(df['SpO2'].mean(), 1)} %")
    colT3.info(f"**Avg Body Temp:** {round(df['BodyTemp'].mean(), 1)} °C")

st.markdown("---")

# Chart 1: Heart Rate Trend
fig_hr = px.line(df, x="Time", y="HeartRate", title="❤️ Heart Rate Over Time",
                 markers=True, template="plotly_dark", line_shape="spline")
fig_hr.update_traces(line=dict(color="red", width=3))
fig_hr.update_layout(height=400, hovermode="x unified")
st.plotly_chart(fig_hr, use_container_width=True)

# Chart 2: SpO₂ Trend
fig_spo2 = px.line(df, x="Time", y="SpO2", title="🩸 SpO₂ (%) Over Time",
                   markers=True, template="plotly_dark", line_shape="spline")
fig_spo2.update_traces(line=dict(color="blue", width=3))
fig_spo2.update_layout(height=400, hovermode="x unified")
st.plotly_chart(fig_spo2, use_container_width=True)

# Chart 3: Temperature & Humidity Trend
fig_temp_hum = px.line(df, x="Time", y=["BodyTemp", "RoomTemp", "Humidity"],
                       title="🌡️ Temp & 💧 Humidity Trends",
                       markers=True, template="plotly_dark", line_shape="spline")
fig_temp_hum.update_layout(height=450, hovermode="x unified")
st.plotly_chart(fig_temp_hum, use_container_width=True)


from firebase_admin import credentials, db, initialize_app
import firebase_admin

# ---------- Firebase Admin Setup ----------
if not firebase_admin._apps:
    cred = credentials.Certificate("service_account.json")  # Ensure this file exists in your project
    initialize_app(cred, {
        'databaseURL': st.secrets["FIREBASE_DB_URL"]
    })

# ---------- Fetch Data from Firebase ----------
firebase_path = "vitals"  # Adjust if your path is different
ref = db.reference(firebase_path)
data = ref.get()

# Convert nested dict to DataFrame
if data:
    records = list(data.values())
    df_firebase = pd.DataFrame(records)
    df_firebase = df_firebase.sort_values(by="Time")  # Ensure chronological order
else:
    df_firebase = pd.DataFrame(columns=["Time", "HeartRate", "SpO2", "BodyTemp", "RoomTemp", "Humidity"])

# ---------- Animated Chart from Firebase ----------
st.subheader("📡 Real-Time Animated Trends (from Firebase)")

animated_fig = px.line(
    df_firebase,
    x="Time",
    y=["HeartRate", "SpO2", "BodyTemp", "RoomTemp", "Humidity"],
    labels={"value": "Reading", "variable": "Vital Sign"},
    title="📉 Animated Real-Time Vitals",
)

animated_fig.update_layout(
    xaxis_title="Timestamp",
    yaxis_title="Reading",
    hovermode="x unified",
    template="plotly_white",
    legend_title="Vitals",
    updatemenus=[{
        "type": "buttons",
        "buttons": [{
            "label": "Play",
            "method": "animate",
            "args": [None, {"frame": {"duration": 1000, "redraw": True}, "fromcurrent": True}]
        }]
    }]
)

# Add frames manually for animation
animated_fig.frames = [
    go.Frame(
        data=[
            go.Scatter(
                x=df_firebase["Time"][:k + 1],
                y=df_firebase[vital][:k + 1],
                mode="lines+markers",
                name=vital
            )
            for vital in ["HeartRate", "SpO2", "BodyTemp", "RoomTemp", "Humidity"]
        ]
    )
    for k in range(1, len(df_firebase))
]

st.plotly_chart(animated_fig, use_container_width=True)


# ---------- Footer ----------
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI</p>",
    unsafe_allow_html=True
)
