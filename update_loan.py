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
    'zinsmethode': '30/360'  # Zurück zu 30/360-Methode
}

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while current_date <= target_date:
        # Zinsen für 30 Tage berechnen
        if current_date.day == 15:
            zinsen = (kapital * darlehen['zins_satz'] / 12).quantize(Decimal('0.01'))
            kapital += zinsen
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        # Immer um 30 Tage springen
        current_date += timedelta(days=30)
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

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
    
    # Validierung mit Toleranz
    if date.today() == date(2025, 4, 15):
        wert = darlehens_entwicklung(date.today())
        assert 24930 <= abs(wert) <= 24940, f"Abweichung: {wert}"
