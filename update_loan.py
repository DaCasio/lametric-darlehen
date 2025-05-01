from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json

getcontext().prec = 8

darlehen = {
    'start_date': date(2023, 8, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('32000.00'),
    'monatsrate': Decimal('497.71'),
    'zins_satz': Decimal('6.742') / 100,
    'zinsmethode': '30/360'
}

def berechne_monatszinsen(kapital: Decimal) -> Decimal:
    return (kapital * darlehen['zins_satz'] / 12).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while current_date <= target_date:
        # Zinsen für den aktuellen Monat berechnen
        zinsen = berechne_monatszinsen(kapital)
        kapital += zinsen
        
        # Monatsrate am 15. abziehen (nicht vor dem Startdatum)
        if current_date.day == 15 and current_date >= darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        # Zum 15. des nächsten Monats springen (30/360-Methode)
        if current_date.month == 12:
            new_year = current_date.year + 1
            new_month = 1
        else:
            new_year = current_date.year
            new_month = current_date.month + 1
        
        current_date = date(new_year, new_month, 15)
    
    return kapital * Decimal('-1')  # Negativen Darlehensstand korrigieren

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{abs(aktueller_stand):.0f}€",
                "icon": "3309",
                "goalData": {
                    "start": 32000,
                    "current": int(abs(aktueller_stand)),
                    "end": 0,
                    "unit": "€"
                }
            }
        ]
    }

if __name__ == "__main__":
    with open("darlehen.json", "w") as f:
        json.dump(generiere_json(), f, indent=2, ensure_ascii=False)
    
    # Validierung für Mai 2025
    if date.today() == date(2025, 5, 15):
        aktueller_wert = darlehens_entwicklung(date.today())
        assert 24577 <= abs(aktueller_wert) <= 24579, f"Abweichung: {abs(aktueller_wert)}€ statt 24.577,20€"
