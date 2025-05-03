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

def monatliche_zinsberechnung(kapital: Decimal) -> Decimal:
    return (kapital * darlehen['zins_satz'] / 12).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    # Berechne alle Zahlungstermine bis zum Target-Datum
    while current_date <= target_date:
        # Zinsen für den aktuellen Monat berechnen
        zinsen = monatliche_zinsberechnung(kapital)
        kapital += zinsen
        
        # Rate am 15. abziehen (außer beim Startdatum selbst)
        if current_date != darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        # Springe zum nächsten 15. des Monats
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 15)
        else:
            current_date = date(current_date.year, current_date.month + 1, 15)
    
    # Tägliche Zinsen für die Resttage nach dem letzten Zahlungstermin
    if current_date > target_date:
        tage_seit_letzter_zahlung = (target_date - current_date.replace(day=15)).days
        tage = max(0, tage_seit_letzter_zahlung)
        kapital += monatliche_zinsberechnung(kapital) / 30 * tage
    
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
    
    # Testdaten validieren
    testdaten = {
        date(2025, 4, 15): Decimal('24934.82'),
        date(2025, 5, 15): Decimal('24577.20'),
        date(2025, 6, 15): Decimal('24217.57')
    }
    
    for datum, sollwert in testdaten.items():
        istwert = darlehens_entwicklung(datum)
        assert istwert == sollwert, f"Fehler am {datum}: {istwert} ≠ {sollwert}"
