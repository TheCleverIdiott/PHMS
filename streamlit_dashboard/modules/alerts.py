def check_alerts(heart_rate, spo2, body_temp, thresholds=None):
    if thresholds is None:
        thresholds = {
            "hr_min": 60,
            "hr_max": 120,
            "spo2_min": 95,
            "body_temp_max": 37.5
        }
    alerts = []

    # Use user-defined thresholds if provided
    if thresholds:
        if heart_rate < thresholds["hr_min"]:
            alerts.append(f"Low Heart Rate: {heart_rate} BPM")
        if heart_rate > thresholds["hr_max"]:
            alerts.append(f"High Heart Rate: {heart_rate} BPM")
        if spo2 < thresholds["spo2_min"]:
            alerts.append(f"Low SpO₂: {spo2}%")
        if body_temp > thresholds["body_temp_max"]:
            alerts.append(f"High Body Temp: {body_temp}°C")
    else:
        # Default static thresholds
        if heart_rate < 60 or heart_rate > 120:
            alerts.append(f"Abnormal Heart Rate: {heart_rate} BPM")
        if spo2 < 95:
            alerts.append(f"Low SpO₂: {spo2}%")
        if body_temp > 37.5:
            alerts.append(f"High Body Temp: {body_temp}°C")

    return alerts

