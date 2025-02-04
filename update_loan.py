from datetime import datetime, timedelta
import json

# Konfiguration der Darlehensdaten
start_date = datetime(2025, 1, 15)
end_date = datetime(2030, 3, 15)
start_amount = 25995.73

total_days = (end_date - start_date).days
daily_reduction = start_amount / total_days

# Berechne den aktuellen Stand basierend auf dem heutigen Datum
today = datetime.now().date()
days_passed = (today - start_date.date()).days
current_value = max(start_amount - daily_reduction * days_passed, 0)

# Rundung ohne Nachkommastellen: Umwandlung in Integer
current_int = int(round(current_value, 0))
start_int = int(round(start_amount, 0))

# Erstelle den Datensatz im JSON-Format
data = {
    "frames": [
        {
            "text": f"{current_int}€",
            "icon": "i3219",
            "goalData": {
                "start": start_int,
                "current": current_int,
                "end": 0,
                "unit": "€"
            }
        }
    ]
}

with open("darlehen.json", "w") as f:
    json.dump(data, f, indent=2)
