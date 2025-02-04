from datetime import datetime, timedelta
import json

start_date = datetime(2025, 1, 15)
end_date = datetime(2030, 3, 15)
total_days = (end_date - start_date).days  # Korrekt: 1885 Tage
daily_reduction = 25995.73 / total_days    # 13.80€/Tag

# Heutiges Datum dynamisch
today = datetime.now().date()
days_passed = (today - start_date.date()).days
current_value = 25995.73 - (daily_reduction * days_passed)

with open("darlehen.json", "w") as f:
    json.dump({
        "frames": [{
            "text": f"{max(current_value, 0):.2f}€",
            "icon": "i3219",
            "goalData": {
                "start": 25995.73,
                "current": max(current_value, 0),
                "end": 0,
                "unit": "€"
            }
        }]
    }, f)
