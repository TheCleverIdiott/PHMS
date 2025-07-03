import streamlit as st
import pandas as pd
import plotly.express as px
from modules.firebase_export import fetch_latest_entries
from streamlit_autorefresh import st_autorefresh
from modules.auth import login, logout
import os

# ---------- Auto Login Redirect ----------
from streamlit_extras.switch_page_button import switch_page

# ---------- Auth Check ----------
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("🔐 Please login first.")
    st.stop()

# ---------- Logout Button Top-Right ----------
import time

colA, colB = st.columns([8, 2])
with colB:
    if st.button("🚪 Logout"):
        st.session_state["user"] = None
        st.success("✅ Thank You for Visiting Us. You have been logged out successfully.")
        st.markdown("<meta http-equiv='refresh' content='2'>", unsafe_allow_html=True)
        time.sleep(2)
        login_script = os.path.join(os.path.dirname(__file__), "login", "0_Login.py")
        with open(login_script, "r", encoding="utf-8") as f:
            exec(f.read())
        st.stop()

    
# ---------- Page Setup ----------
st.set_page_config(page_title="Live Firebase Feed", layout="wide", page_icon="📡")
st.title("📡 Live Vitals Feed from Firebase")

# ---------- Auto Refresh Every 10 sec ----------
st_autorefresh(interval=10000, key="firebase_auto_refresh")

# ---------- Data Fetch ----------
st.info("Auto-refreshing every 10 seconds. You can also click below to fetch now.")
if st.button("🔄 Manual Refresh"):
    st.rerun()

df = fetch_latest_entries(limit=15)

if df.empty:
    st.warning("⚠️ No recent data found in Firebase. Log some data from the Vitals page.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.success(f"✅ Showing latest {len(df)} entries from Firebase.")

    # ---------- Charts ----------
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(df, x="timestamp", y=["heart_rate", "spo2"], title="Heart Rate & SpO₂ (Live)", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(df, x="timestamp", y=["body_temp", "room_temp", "humidity"], title="Temperature & Humidity (Live)", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ---------- Raw Table ----------
    st.subheader("📋 Raw Data Table")
    st.dataframe(df)

# ---------- Footer ----------
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI</p>",
    unsafe_allow_html=True
)