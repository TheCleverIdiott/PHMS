import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os
import pandas as pd

# ---------- Firebase Initialization ----------
firebase_key_path = "streamlit_dashboard/firebase_key.json"

if os.path.exists(firebase_key_path) and not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://patient-health-1cdb3-default-rtdb.firebaseio.com/'
    })

# ---------- Push Data to Firebase ----------
def push_to_firebase(heart_rate, spo2, body_temp, room_temp, humidity):
    try:
        ref = db.reference("patient_vitals")
        ref.push({
            "timestamp": datetime.now().isoformat(),
            "heart_rate": heart_rate,
            "spo2": spo2,
            "body_temp": body_temp,
            "room_temp": room_temp,
            "humidity": humidity
        })
        print("✅ Data successfully pushed to Firebase.")
    except Exception as e:
        print(f"❌ Firebase push failed: {e}")

# ---------- Fetch Latest Entries ----------
def fetch_latest_entries(limit=10):
    try:
        ref = db.reference("patient_vitals")
        data = ref.order_by_key().limit_to_last(limit).get()
        if data:
            df = pd.DataFrame(list(data.values()))
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df.sort_values("timestamp")
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Firebase fetch failed: {e}")
        return pd.DataFrame()
