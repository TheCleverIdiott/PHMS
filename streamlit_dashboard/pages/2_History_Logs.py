import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import os
import time


# ---------- Auth Check ----------
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("🔐 Please login first.")
    st.stop()


# ---------- Page Setup ----------
st.set_page_config(page_title="Vitals Log History", layout="wide", page_icon="📜")
st.title("📜 Logged Vitals History (Firebase)")

# ---------- Firebase Admin Setup ----------
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

# ---------- Fetch Data from Firebase ----------
st.info("⏳ Fetching data from Firebase...")
ref = db.reference("sensor_data")
raw_data = ref.get()

records = []
if raw_data:
    for date, entries in raw_data.items():
        for timestamp, values in entries.items():
            record = {
                "Date": date,
                "Time": values.get("Time", ""),
                "HeartRate": values.get("HeartRate"),
                "SpO2": values.get("SpO2") or values.get("Sp02"),
                "BodyTemp": values.get("BodyTemp"),
                "RoomTemp": values.get("RoomTemp"),
                "Humidity": values.get("Humidity")
            }
            records.append(record)

if records:
    df = pd.DataFrame(records)
    df = df.sort_values(by=["Date", "Time"])

    st.success(f"✅ Loaded {len(df)} vitals entries from Firebase.")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="📥 Download Firebase Data as CSV",
        data=df.to_csv(index=False),
        file_name="firebase_vitals_log.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ No vitals data found in Firebase.")

# ---------- Logout Top-Right ----------
colA, colB = st.columns([8, 2])
with colB:
    if st.button("🚪 Logout"):
        st.session_state["user"] = None
        st.success("✅ You have been logged out.")
        st.markdown("<meta http-equiv='refresh' content='2'>", unsafe_allow_html=True)
        time.sleep(2)
        st.stop()

# ---------- Footer ----------
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI</p>",
    unsafe_allow_html=True
)
