# daily_report.py
import pandas as pd
from modules.notifier import send_email_alert
from datetime import datetime

df = pd.read_csv("realtime_vitals_data.csv")
today = datetime.now().strftime("%Y-%m-%d")

latest_10 = df.tail(10)
html_table = latest_10.to_html(index=False)

subject = f"📝 Daily Vitals Report – {today}"
body = f"""
<h2>🩺 Patient Vitals Report – {today}</h2>
<p>Below are the last 10 vitals logged:</p>
{html_table}
"""

send_email_alert(subject, body)
