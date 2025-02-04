from datetime import datetime, timedelta
import json

# Start- und Enddaten
start_date = datetime(2025, 1, 15)
end_date = datetime(2030, 3, 15)
total_days = (end_date - start_date).days

# Berechnung der täglichen Reduktion
start_amount = 25995.73
daily_reduction = start_amount / total_days

# Aktuellen Stand berechnen
today = datetime.now().date()
days_passed = (today - start_date.date()).days
current_value = max(start_amount - (daily_reduction * days_passed), 0)

# JSON-Datei erstellen
json_data = {
    "frames": [
        {
            "text": f"{current_value:.2f}€",
            "icon": "i3219",
            "goalData": {
                "start": start_amount,
                "current": current_value,
                "end": 0,
                "unit": "€"
            }
        }
    ]
}

with open("darlehen.json", "w") as f:
    json.dump(json_data, f, indent=2)
