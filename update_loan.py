from datetime import datetime, timedelta
import json

# Konfiguration der Darlehensdaten
start_date = datetime(2025, 1, 15)
end_date = datetime(2030, 3, 15)
start_amount = 25995.73
monthly_rate = 497.71
annual_interest_rate = 0.0674  # 6.74% p.a.

daily_interest_rate = annual_interest_rate / 365

def calculate_loan_balance(target_date):
    current_balance = start_amount
    current_date = start_date
    while current_date <= target_date:
        if current_date.day == 15:
            # Monatliche Rate abziehen
            current_balance -= monthly_rate
        else:
            # Tägliche Zinsen hinzufügen
            current_balance += current_balance * daily_interest_rate
        current_date += timedelta(days=1)
    return max(current_balance, 0)

# Berechne den aktuellen Stand basierend auf dem heutigen Datum
today = datetime.now().date()
current_value = calculate_loan_balance(today)

# Rundung auf ganze Zahlen (keine Nachkommastellen)
current_int = int(round(current_value))
start_int = int(round(start_amount))

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

# Speichere die JSON-Datei
with open("darlehen.json", "w") as f:
    json.dump(data, f, indent=2)
