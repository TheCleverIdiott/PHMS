# 🩺 Real-Time Smart Health Monitoring Dashboard using ESP32, Firebase & Streamlit

![GitHub stars](https://img.shields.io/github/stars/dhananjaykr9/Patient-Health-Monitoring-System?style=social)
![GitHub forks](https://img.shields.io/github/forks/dhananjaykr9/Patient-Health-Monitoring-System?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/dhananjaykr9/Patient-Health-Monitoring-System?style=social)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/platform-ESP32--Firebase--Streamlit-green)

![GitHub last commit](https://img.shields.io/github/last-commit/dhananjaykr9/Patient-Health-Monitoring-System)
![GitHub repo size](https://img.shields.io/github/repo-size/dhananjaykr9/Patient-Health-Monitoring-System)
![License](https://img.shields.io/github/license/dhananjaykr9/Patient-Health-Monitoring-System)

---

## 📌 Project Overview

This project implements a **real-time Smart Health Monitoring System** using an **ESP32 microcontroller** (with simulated sensor data), **Firebase Realtime Database**, and an interactive **Streamlit Dashboard** to visualize patient vitals like Heart Rate, SpO₂, Body Temperature, Room Temperature, and Humidity.

> 📍 The system also includes alert triggering, SMS/email notifications, historical log tracking, and secure login using Firebase Auth.

---

## 💡 Tech Stack

* **ESP32** – Simulates patient sensor data
* **Firebase Realtime Database** – Cloud backend for storing vitals
* **Firebase Authentication** – Secured access for dashboard users
* **Streamlit** – Frontend dashboard for real-time monitoring
* **Twilio API** – Sends SMS alerts
* **Gmail SMTP** – Sends email alerts
* **Plotly** – Generates dynamic vitals charts

---

## 🧭 System Architecture

```
ESP32 → Firebase Realtime DB → Streamlit Dashboard
                                  ↓
          Login Auth, Alerts, Charts, SMS/Email Notifications
```

---

## ✅ Key Features

* Real-time monitoring of patient vitals from cloud database
* Interactive, auto-refreshing dashboard (every 10s)
* Configurable alert thresholds (via sidebar)
* Alarm popup + siren playback
* SMS & Email alerts using Twilio + Gmail SMTP
* Historical vitals table with CSV export option
* Modular and clean code structure
* Horizontal time filter slider for viewing past N hours

---

## 🔐 Firebase Authentication

Dashboard access is protected by Firebase Email/Password login. Each authenticated user has access to secured vitals only.

---

## 📊 Dashboard Modules

| Page            | Description                                   |
| --------------- | --------------------------------------------- |
| **Home**        | Overview, instructions, logout                |
| **Vitals**      | Real-time vitals chart, alert popup, notifier |
| **History Log** | View and export CSV of past vitals            |

---

## 📁 Project Structure

```
streamlit_dashboard/
│
├── assets/                        → Logo & alarm sound
│   ├── alarm-siren.mp3
│   └── logo.png
│
├── login/
│   └── 0_Login.py                 → Firebase login UI
│
├── modules/                      → Modular Python files
│   ├── alerts.py                 → Threshold checking
│   ├── auth.py                   → Auth logic
│   ├── notifier.py               → Twilio/SMTP functions
│   ├── firebase_export.py        → Export functions
│   └── daily_report.py           → Scheduled reporting (Not Integrated Now)
│
├── pages/
│   ├── 1_Vitals.py               → Real-time dashboard
│   └── 2_History_Logs.py         → Data logs page
│
├── Home.py                       → Main landing page
└── requirements.txt              → Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Firebase Setup

* Create a Firebase project
* Enable Realtime Database
* Enable Email/Password Authentication
* Generate Admin SDK and add to Streamlit Secrets

### 2. ESP32 Simulation

Use simulated random values:

```cpp
int HeartRate = random(60, 120);
int Sp02 = random(90,100);
float BodyTemp = random(360, 390) / 10;
float RoomTemp = random(250, 320) / 10.0;
int Humidity = random(30,70);
```

Firebase path:

```
/sensor_data/YYYY-MM-DD/<timestamp>/
    HeartRate: 102
    SpO2: 96
    BodyTemp: 37.2
    RoomTemp: 30.5
    Humidity: 48
```

### 3. Streamlit Installation

```bash
pip install streamlit firebase-admin plotly streamlit-autorefresh twilio
streamlit run streamlit_dashboard/Home.py
```

 Add your Firebase credentials in `.streamlit/secrets.toml` 
---

## 📤 Alerts & Notifications

| Type  | Tech Used   | Behavior                                 |
| ----- | ----------- | ---------------------------------------- |
| Alert | Plotly + JS | Popup and siren when vitals cross limits |
| SMS   | Twilio API  | Sends text alerts                        |
| Email | Gmail SMTP  | Sends alert email                        |

---

## 🕒 Filter by Time

Use the sidebar slider to view data for the last **N hours** dynamically. Data updates in real-time via auto-refresh.

---

## 🔒 Security

* Firebase authentication for login
* Firebase rules restrict access per user
* Secrets are securely stored in `.streamlit/secrets.toml`

---

## 🧩 Visuals

<h3>📈 Real-Time Vitals Trend Charts</h3>
<img src="streamlit_dashboard\images\body_temp_over_time.png" width="600"/>
<img src="streamlit_dashboard\images\heart_rate_over_time.png" width="600"/>
<img src="streamlit_dashboard\images\room_temp_humidity_trends.png" width="600"/>
<img src="streamlit_dashboard\images\SpO2_over_time.png" width="600"/>

<h3>🏠 Home Dashboard</h3>
<img src="streamlit_dashboard\images\dashboard_home.png" width="600"/>

<h3>🫀 Vitals Dashboard</h3>
<img src="streamlit_dashboard\images\vitals_dashboard.png" width="600"/>

<h3>🔐 Login Page</h3>
<img src="screenshots/gauge_display.png" width="600"/>

<h3>🗂️ Vitals Data Logs</h3>
<img src="streamlit_dashboard\images\login_page.png" width="600"/>

---

## 🚀 Future Improvements

* Replace simulation with actual MAX30102 or DS18B20 sensors
* Scheduled email reports (daily/weekly PDF/CSV)
* Statistical anomaly detection (Z-score, IQR)
* AI/ML model for predictive diagnostics
* Multi-role login (Admin, Doctor, Patient)
* User dashboard for each patient
* Mobile-optimized interface or PWA

---

## 🔭 Future Scope

This project can be expanded into a full-fledged IoT HealthTech solution:

* **Medical-grade sensor integration** (clinically accurate data)
* **Cloud deployment for hospitals** (AWS/GCP scalable systems)
* **EHR integration** with hospital databases
* **AI-powered patient risk scoring and forecasting**
* **Geolocation-based alerts and patient tracking**
* **Multi-channel notifications** (Email, SMS, WhatsApp, Telegram)
* **Mobile companion app** for both patients and doctors
* **Dashboard analytics with historical trends and insights**

---
---

## 🤝 Contact & Contribution

Feel free to fork the repo, raise issues, or contribute. For discussions, reach me via [LinkedIn](https://www.linkedin.com/in/dhananjaykharkar/)

---

⭐ **If you like this project, please give it a star!**
📄 Licensed under the [MIT License](LICENSE)

---
