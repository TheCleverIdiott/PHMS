import streamlit as st
from modules.auth import login, logout

st.set_page_config(page_title="Login", layout="centered", page_icon="🔐")

# ---------- Centered Image Banner ----------
st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://cdn-icons-png.flaticon.com/128/2382/2382461.png" width="100"/>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- Title & Caption ----------
st.markdown("<h2 align='center'>🔐 Smart Health Login</h2>", unsafe_allow_html=True)
st.markdown("<p align='center'>Secure access to your health monitoring dashboard</p>", unsafe_allow_html=True)

# ---------- Centered Login ----------
if "user" not in st.session_state or st.session_state["user"] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login()  # Call your login logic

        if st.session_state.get("user"):
            st.success("✅ Login successful! Redirecting...")
            st.session_state.login_success = True
            st.rerun()
    st.stop()

# ---------- Already Logged In View ----------
st.markdown(f"<p align='center'>✅ Logged in as: {st.session_state['user']['email']}</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    if st.button("🚪 Logout"):
        logout()
        st.rerun()

st.markdown("<p align='center'>➡️ Use the sidebar to access the dashboard pages.</p>", unsafe_allow_html=True)
