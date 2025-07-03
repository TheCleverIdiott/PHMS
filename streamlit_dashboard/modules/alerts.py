def check_alerts(heart_rate, spo2, body_temp):
    alerts = []

    if heart_rate < 60 or heart_rate > 120:
        alerts.append(f"⚠️ Abnormal Heart Rate: {heart_rate} BPM")

    if spo2 < 94:
        alerts.append(f"⚠️ Low SpO₂ detected: {spo2}%")

    if body_temp < 36.1 or body_temp > 37.8:
        alerts.append(f"⚠️ Irregular Body Temperature: {body_temp} °C")

    return alerts


