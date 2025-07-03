import pyrebase
import streamlit as st

firebase_config = {
    "apiKey": st.secrets["FIREBASE_API_KEY"],
    "authDomain": st.secrets["FIREBASE_AUTH_DOMAIN"],
    "databaseURL": st.secrets["FIREBASE_DB_URL"],
    "projectId": st.secrets["FIREBASE_PROJECT_ID"],
    "storageBucket": st.secrets["FIREBASE_STORAGE_BUCKET"],
    "messagingSenderId": "509332662334",  # optionally move this too
    "appId": st.secrets["FIREBASE_APP_ID"]
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "login_success" not in st.session_state:
        st.session_state.login_success = False

    # If login already successful, show and return
    if st.session_state.login_success and st.session_state.user:
        st.success(f"✅ Logged in as {st.session_state.user['email']}")
        return

    # Show login form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("🔓 Login")

        if submit:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.session_state.login_success = True  # ✅ trigger success
            except:
                st.session_state.login_success = False
                st.error("❌ Invalid credentials. Try again.")

def logout():
    st.session_state.user = None
    st.session_state.login_success = False
