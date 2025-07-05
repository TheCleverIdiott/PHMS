import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from firebase_admin import credentials, db, initialize_app
import firebase_admin
from modules.alerts import check_alerts
from modules.notifier import send_sms_alert, send_email_alert
import base64

# ----------- Auth Check -----------
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("🔒 Please login to access the dashboard.")
    st.stop()


# ----------- Page Setup -----------
st.set_page_config(page_title="Vitals Monitoring", layout="wide", page_icon="📊")
st_autorefresh(interval=10000, key="auto_refresh")

st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #2E86C1;'>📊 Real-Time Vitals Dashboard</h1>
        <p style='font-size: 16px;'>Live monitoring of patient vitals with alerts and Firebase integration.</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)

# ----------- Firebase Setup -----------
if not firebase_admin._apps:
    cred = credentials.Certificate({
    "type": st.secrets["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_CLIENT_ID"],
    "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
    "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_X509_CERT_URL"]
}) # Ensure this file is present
    firebase_admin.initialize_app(cred, {
        'databaseURL': st.secrets["FIREBASE_DB_URL"]
    })



# ----------- Fetch Firebase Data -----------
ref = db.reference("sensor_data")
raw_data = ref.get()

records = []
if raw_data:
    for day in raw_data.values():
        if isinstance(day, dict):
            for item in day.values():
                records.append(item)

if records:
    df = pd.DataFrame(records)
    df = df.sort_values(by="Time")
    # Convert to datetime
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    st.markdown("### ⏱️ View Time Range")
    hours = st.slider("Show data for past N hours", min_value=0, max_value=24, value=1, step=1)

    st.markdown("### 🔔 Alert Settings")
    toggle = st.toggle("Enable SMS/Email Alerts", value=st.session_state.get("enable_alerts", True))
    st.session_state.enable_alerts = toggle

    st.markdown("---")
    st.markdown("### 📊 Alert Thresholds")
    thresholds = {
        "hr_min": st.number_input("Min Heart Rate (BPM)", min_value=30, max_value=100, value=60, key="hr_min"),
        "hr_max": st.number_input("Max Heart Rate (BPM)", min_value=100, max_value=200, value=120, key="hr_max"),
        "spo2_min": st.number_input("Min SpO₂ (%)", min_value=80, max_value=100, value=95, key="spo2_min"),
        "body_temp_max": st.number_input("Max Body Temp (°C)", min_value=35.0, max_value=42.0, value=37.5, key="body_temp_max")
    }

# ------------------- DATA FILTERING -------------------
df = pd.DataFrame(records).sort_values(by="Time") if records else pd.DataFrame(columns=["Time", "HeartRate", "Sp02", "BodyTemp", "RoomTemp", "Humidity"])

if not df.empty:
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    now = pd.Timestamp.now()
    df = df[df['Time'] >= (now - pd.Timedelta(hours=hours))]


# ----------- Display Current Vitals -----------
st.markdown("### 🧾 Current Vitals Summary")
if not df.empty:
    latest = df.iloc[-1]
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("❤️ Heart Rate", f"{latest['HeartRate']} BPM")
    col2.metric("🩸 SpO₂", f"{latest['Sp02']} %")
    col3.metric("🌡️ Body Temp", f"{latest['BodyTemp']} °C")
    col4.metric("🏠 Room Temp", f"{latest['RoomTemp']} °C")
    col5.metric("💧 Humidity", f"{latest['Humidity']} %")

    # ----------- Alert System -----------
    alerts = check_alerts(
        int(latest["HeartRate"]),
        int(latest["Sp02"]),
        float(latest["BodyTemp"]),
        thresholds=thresholds
    )

    if alerts:
        st.error("🚨 Alerts Triggered")
        for alert in alerts:
            st.warning(alert)

        # -------- Online Alarm Sound --------
        alarm_url = "https://raw.githubusercontent.com/dhananjaykr9/Smart-Health-Streamlit-Dashboard/main/streamlit_dashboard/assets/alarm-siren.mp3"

        st.markdown(f"""
            <audio autoplay>
                <source src="{alarm_url}" type="audio/mp3">
            </audio>
            <script>
                window.onload = function() {{
                    alert("🚨 ALERT: Abnormal vitals detected! Please check immediately.");
                }}
            </script>
        """, unsafe_allow_html=True)

        if st.session_state.enable_alerts:
            alert_message = "\n".join(alerts)
            send_sms_alert(f"🚨 Patient Alert:\n{alert_message}")
            send_email_alert("🚨 Patient Vitals Alert", alert_message)
            st.info("📨 Notifications sent via SMS & Email.")
        else:
            st.info("⚠️ Alerts detected but notifications are disabled.")
    else:
        st.success("✅ All vitals are in healthy range.")

else:
    st.warning("⚠️ No data from Firebase yet. Check if ESP32 is pushing data.")

# ----------- Trend Charts -----------
if not df.empty:
    st.markdown("### 📈 Real-Time Vitals Trend Charts")

    fig1 = px.line(df, x="Time", y="HeartRate", title="❤️ Heart Rate Over Time",
                   markers=True, template="plotly_dark", line_shape="spline")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(df, x="Time", y="Sp02", title="🩸 SpO₂ Over Time",
                   markers=True, template="plotly_dark", line_shape="spline")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.line(df, x="Time", y="BodyTemp", title="🌡️ Body Temp Over Time",
                   markers=True, template="plotly_dark", line_shape="spline")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.line(df, x="Time", y=["RoomTemp", "Humidity"],
                   title="🏠 Room Temp & 💧 Humidity Trends",
                   markers=True, template="plotly_dark", line_shape="spline")
    st.plotly_chart(fig4, use_container_width=True)

# ------------------ Data Table ------------------
#st.markdown("### 📋 Latest Data Table")
#st.dataframe(df.tail(50), use_container_width=True)

# ------------------ CSV Export ------------------
#st.download_button(
#    label="📥 Download Full Vitals CSV",
#    data=df.to_csv(index=False),
#    file_name="realtime_vitals_data.csv",
#    mime="text/csv"
#)

# ----------- Footer -----------
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px;'>🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI</p>", unsafe_allow_html=True)
