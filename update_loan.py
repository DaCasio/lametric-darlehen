from datetime import datetime, timedelta, date
import json
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

# Konfiguration der Darlehensdaten
start_date = date(2025, 1, 15)
end_date = date(2030, 3, 15)
start_amount = Decimal('25995.73')
monthly_rate = Decimal('497.71')
annual_interest_rate = Decimal('0.0674')  # 6.74% p.a.

daily_interest_rate = (Decimal('1') + annual_interest_rate) ** (Decimal('1') / Decimal('365')) - Decimal('1')

def calculate_loan_balance(target_date):
    current_balance = start_amount
    current_date = start_date
    days_since_last_payment = 0
    while current_date <= target_date:
        if current_date.day == 15:
            # Zinsen für den vergangenen Monat berechnen
            interest = current_balance * ((Decimal('1') + daily_interest_rate) ** Decimal(days_since_last_payment) - Decimal('1'))
            current_balance += interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            # Monatliche Rate abziehen
            current_balance -= monthly_rate
            days_since_last_payment = 0
        else:
            days_since_last_payment += 1
        current_date += timedelta(days=1)
    return max(current_balance, Decimal('0'))

# Berechne den aktuellen Stand basierend auf dem heutigen Datum
today = date.today()
current_value = calculate_loan_balance(today)

# Rundung auf ganze Zahlen (keine Nachkommastellen)
current_int = int(current_value.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
start_int = int(start_amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

# Erstelle den Datensatz im JSON-Format
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

# Speichere die JSON-Datei
with open("darlehen.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Aktueller Darlehensstand: {current_int}€")
