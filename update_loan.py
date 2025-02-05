from datetime import datetime, timedelta, date
import json
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

# Konfiguration der Darlehensdaten
start_date = date(2025, 1, 15)
end_date = date(2030, 3, 15)
start_amount = Decimal('25995.73')
monthly_rate = Decimal('497.71')
annual_interest_rate = Decimal('0.0674')  # 6.74% p.a.

# Täglicher Zinssatz (360-Tage-Basis)
daily_interest_rate = annual_interest_rate / Decimal('360')

def calculate_loan_balance(target_date):
    current_balance = start_amount
    current_date = start_date
    days_in_year = 360
    
    while current_date <= target_date:
        if current_date.day == 15:
            # Monatliche Zinsberechnung
            days_since_last_payment = 30  # Annahme: immer 30 Tage zwischen Zahlungen
            interest = current_balance * (annual_interest_rate / 12)
            current_balance += interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Monatliche Rate abziehen
            current_balance -= monthly_rate
        
        current_date += timedelta(days=1)
    
    return max(current_balance, Decimal('0'))

# Berechne den aktuellen Stand basierend auf dem heutigen Datum
today = date.today()
current_value = calculate_loan_balance(today)

# Rundung auf ganze Zahlen (keine Nachkommastellen)
current_
