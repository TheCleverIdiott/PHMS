import pandas as pd
from datetime import datetime
import os

def log_data(heart_rate, spo2, body_temp, room_temp, humidity):
    log_file = "vitals_log.csv"
    
    # Prepare entry
    new_entry = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "HeartRate": heart_rate,
        "SpO2": spo2,
        "BodyTemp": body_temp,
        "RoomTemp": room_temp,
        "Humidity": humidity
    }

    # Append to existing or create new CSV
    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])

    df.to_csv(log_file, index=False)
