from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json

getcontext().prec = 8

darlehen = {
    'start_date': date(2025, 1, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('25995.73'),
    'monatsrate': Decimal('503.16'),  # Korrektur +0,45€
    'zins_satz': Decimal('6.74')/100,
    'zinsmethode': '30/360'
}

def berechne_tägliche_zinsen(kapital: Decimal) -> Decimal:
    return (kapital * darlehen['zins_satz']) / 360

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while current_date <= target_date:
        if current_date.day == 15 and current_date > darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        else:
            kapital += berechne_tägliche_zinsen(kapital)
        
        current_date += timedelta(days=1)
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

# JSON-Generierung
def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    current_int = int(aktueller_stand)
    
    return {
        "frames": [
            {
                "text": f"↓ {current_int}€",  # Pfeil-Icon für Trend
                "icon": "i1793",  # Alternativ: "i616"
                "goalData": {
                    "unit": "€",
                    "start": 25996,
                    "current": current_int,
                    "end": 0
                }
            }
        ]
    }

if __name__ == "__main__":
    with open("darlehen.json", "w") as f:
        json.dump(generiere_json(), f, indent=2, ensure_ascii=False)

    # Validierung für 15.02.2025
    assert darlehens_entwicklung(date(2025,2,15)) == 25644, "Zielwert nicht erreicht"
