from datetime import datetime, timedelta, date
import json
from decimal import Decimal, ROUND_HALF_UP

# Konfiguration der Darlehensdaten
start_date = date(2025, 1, 15)
end_date = date(2030, 3, 15)
start_amount = Decimal('25996.00')  # Gerundeter Startwert
target_amount_15_02_2025 = Decimal('25644.00')
monthly_rate = Decimal('497.71')
annual_interest_rate = Decimal('0.0674')  # 6.74% p.a.

# Berechnung des täglichen Zinssatzes basierend auf dem Zielwert am 15.02.2025
days_between = (date(2025, 2, 15) - start_date).days
daily_interest_rate = ((target_amount_15_02_2025 + monthly_rate - start_amount) / start_amount / days_between).quantize(Decimal('0.00000001'))

def calculate_loan_balance(target_date):
    current_balance = start_amount
    current_date = start_date
    
    while current_date <= target_date:
        if current_date.day == 15 and current_date > start_date:
            # Monatliche Rate abziehen
            current_balance -= monthly_rate
        
        # Tägliche Zinsberechnung
        interest = current_balance * daily_interest_rate
        current_balance += interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        current_date += timedelta(days=1)
    
    return max(current_balance, Decimal('0'))

# Berechne den aktuellen Stand basierend auf dem heutigen Datum
today = date.today()
current_value = calculate_loan_balance(today)

# Rundung auf ganze Zahlen (keine Nachkommastellen)
current_int = int(current_value.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
start_int = int(start_amount)

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

# Zusätzliche Ausgabe für den 15.2.2025
balance_15_02_2025 = calculate_loan_balance(date(2025, 2, 15))
print(f"Darlehensstand am 15.2.2025: {int(balance_15_02_2025)}€")
