from datetime import datetime, timedelta, date
from decimal import Decimal, ROUND_HALF_UP
import json

# Konfiguration der Darlehensdaten
start_date = date(2025, 1, 15)
end_date = date(2030, 3, 15)
start_amount = Decimal('25995.73')
monthly_rate = Decimal('497.71')
annual_interest_rate = Decimal('0.0674')  # 6.74% p.a.

daily_interest_rate = annual_interest_rate / 365

def calculate_loan_balance(target_date):
    current_balance = start_amount
    current_date = start_date
    
    while current_date <= target_date:
        if current_date.day == 15 and current_date > start_date:
            # Monatliche Rate abziehen
            current_balance -= monthly_rate
        else:
            # Tägliche Zinsen berechnen
            current_balance += current_balance * daily_interest_rate
        
        current_date += timedelta(days=1)
    
    return max(current_balance, Decimal('0'))

# Berechne den aktuellen Stand
today = date.today()
current_value = calculate_loan_balance(today)

# Rundung auf ganze Euro
current_int = int(current_value.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
start_int = int(start_amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

# JSON-Datenstruktur
data = {
    "frames": [
        {
            "text": f"{current_int}€",
            "icon": "i616",
            "goalData": {
                "start": start_int,
                "current": current_int,
                "end": 0,
                "unit": "€"
            }
        }
    ]
}

# Datei schreiben
with open("darlehen.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
