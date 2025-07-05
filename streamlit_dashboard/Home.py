import streamlit as st
import os
import time
from streamlit_extras.switch_page_button import switch_page

# ---------- Page Setup ----------
st.set_page_config(page_title="Smart Health Dashboard", page_icon="🩺", layout="wide")

# ---------- Auto Login Redirect ----------
if "user" not in st.session_state or st.session_state["user"] is None:
    login_script = os.path.join(os.path.dirname(__file__), "login", "0_Login.py")
    with open(login_script, "r", encoding="utf-8") as f:
        exec(f.read())
    st.stop()

# ---------- Logout Button (Top-Right Corner) ----------
colA, colB = st.columns([8, 2])
with colB:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["user"] = None
        st.success("✅ Thank you for visiting. Logging out...")
        st.markdown("<meta http-equiv='refresh' content='2'>", unsafe_allow_html=True)
        time.sleep(2)
        login_script = os.path.join(os.path.dirname(__file__), "login", "0_Login.py")
        with open(login_script, "r", encoding="utf-8") as f:
            exec(f.read())
        st.stop()

# ---------- Header with Logo ----------
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/128/7310/7310705.png" width="120" />
        <h1 style="color: #2E86C1; margin-bottom: 5px;">🩺 Smart Health Monitoring Dashboard</h1>
        <p style='font-size:17px;'>Real-time vitals tracking platform for patient health management.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- Sidebar Navigation Guide ----------
st.markdown(
    """
    <div style='font-size:16px;'>
        📋 <b>Sidebar Navigation:</b>
        <ul>
            <li>🏠 <b>Home</b>: Overview of the Smart Health System</li>
            <li>📊 <b>Vitals</b>: Live monitoring, alerting, and Firebase streaming</li>
            <li>🗂️ <b>History Log</b>: View past data and export CSV logs</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Optional Features Highlight ----------
st.markdown("### 💡 Features at a Glance")
st.markdown(
    """
    - 🔔 Configurable Alert Thresholds  
    - 📨 SMS & Email Notifications  
    - 📈 Dynamic Charts with Plotly  
    - 📥 CSV Export Support  
    - 🎧 Audio + Popup Alert System  
    """
)

# ---------- Footer ----------
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; font-size: 14px; color: gray;'>
        🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI
    </div>
    """,
    unsafe_allow_html=True
)
