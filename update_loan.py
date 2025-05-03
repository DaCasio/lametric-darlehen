from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json

getcontext().prec = 10

darlehen = {
    'start_date': date(2023, 8, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('32000.00'),
    'monatsrate': Decimal('497.71'),
    'zins_satz': Decimal('6.742') / 100,
    'zinsmethode': '30/360'
}

def days_360(start: date, end: date) -> int:
    """Berechnet Tage nach 30/360-Methode"""
    d1 = min(start.day, 30)
    d2 = end.day if (start.day < 30 or end.day < 30) else 30
    return 360*(end.year - start.year) + 30*(end.month - start.month) + (d2 - d1)

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    letzte_zahlung = current_date
    
    while current_date <= target_date:
        # Zinsen bis zum nächsten Zahlungstermin berechnen
        if current_date.day == 15 or current_date == darlehen['start_date']:
            next_payment = current_date + timedelta(days=30)
            next_payment = next_payment.replace(day=15)
            
            tage = days_360(current_date, min(next_payment, target_date))
            zinsen = kapital * darlehen['zins_satz'] / 360 * tage
            kapital += zinsen
            
            if next_payment <= target_date:
                kapital -= darlehen['monatsrate']
                kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
                letzte_zahlung = next_payment
            
            current_date = min(next_payment, target_date)
        else:
            current_date += timedelta(days=1)
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{aktueller_stand:.0f}€",
                "icon": "3309",
                "goalData": {
                    "start": 32000,
                    "current": int(aktueller_stand),
                    "end": 0,
                    "unit": "€"
                }
            }
        ]
    }

if __name__ == "__main__":
    with open("darlehen.json", "w") as f:
        json.dump(generiere_json(), f, indent=2, ensure_ascii=False)

    # Validierungen
    heute = date.today()
    if heute == date(2025, 5, 15):
        assert 24577 <= darlehens_entwicklung(heute) <= 24579
    elif heute == date(2025, 6, 15):
        assert 24217 <= darlehens_entwicklung(heute) <= 24219
        
