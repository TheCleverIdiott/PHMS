import streamlit as st
import os
import time
from streamlit_extras.switch_page_button import switch_page  # Make sure this is installed and imported

st.set_page_config(page_title="Smart Health Dashboard", page_icon="🩺", layout="wide")

# ---------- Auto Login Redirect ----------
if "user" not in st.session_state or st.session_state["user"] is None:
    login_script = os.path.join(os.path.dirname(__file__), "login", "0_Login.py")
    with open(login_script, "r", encoding="utf-8") as f:
        exec(f.read())
    st.stop()

# ---------- Logout Button Top-Right ----------
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

# ---------- Main Content ----------
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>Smart Health Monitoring Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align: center; font-size:18px;'>
        This dashboard is designed to monitor patient health vitals in real-time.<br>
        It integrates IoT sensor data, Firebase logging, and analytics tools to ensure efficient healthcare monitoring.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.markdown(
    """
    <div style='font-size:16px;'>
        👉 Use the sidebar to navigate between:
        <ul>
            <li><b>Vitals</b>: Input, simulate, and visualize patient vitals with alert detection and Firebase logging.</li>
            <li><b>Live Firebase Feed</b>: View the real-time trends of vitals data streamed from Firebase.</li>
            <li><b>History Log</b>: Browse and export previously logged vitals in CSV format.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- Footer ----------
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI</p>",
    unsafe_allow_html=True
)