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
    'zinsmethode': 'act/360'  # Tägliche Zinsen (Actual/360)
}

def berechne_tägliche_zinsen(kapital: Decimal, tage: int) -> Decimal:
    return (kapital * darlehen['zins_satz'] / 360 * tage).quantize(Decimal('0.00000000'))

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while current_date < target_date:
        # Bestimme das nächste relevante Datum (nächster 15. oder Target-Datum)
        next_date = current_date + timedelta(days=1)
        
        # Zinsen für 1 Tag berechnen
        kapital += berechne_tägliche_zinsen(kapital, 1)
        
        # Monatsrate am 15. abziehen (nicht vor Startdatum)
        if next_date.day == 15 and next_date > darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        current_date = next_date
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{aktueller_stand:.0f}€",
                "icon": "3309",  # Korrekt ohne "i"
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
    
    # Debug-Output für spezifische Daten
    debug_dates = {
        date(2025, 4, 15): Decimal('24934.82'),
        date(2025, 5, 15): Decimal('24577.20'),
        date(2025, 6, 15): Decimal('24217.57')
    }
    for d, expected in debug_dates.items():
        calculated = darlehens_entwicklung(d)
        assert calculated == expected, f"Fehler am {d}: {calculated} ≠ {expected}"
