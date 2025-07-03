import streamlit as st
import pandas as pd
import os
from modules.auth import login, logout

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
st.set_page_config(page_title="Vitals Log History", layout="wide", page_icon="📜")
st.title("📜 Logged Vitals History (CSV)")

# ---------- File Path ----------
log_file = "vitals_log.csv"

# ---------- Load Data ----------
if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
    df = pd.read_csv(log_file)

    st.success(f"✅ Showing {len(df)} logged entries.")
    st.dataframe(df)

    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name="vitals_log.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ No data available. Please log some vitals from the Vitals tab.")

# ---------- Footer ----------
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px; color: gray;'>🔒 Secured | Powered by ❤️ Streamlit & Firebase | Smart Health AI</p>",
    unsafe_allow_html=True
)