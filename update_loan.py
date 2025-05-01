from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json

getcontext().prec = 8

darlehen = {
    'start_date': date(2023, 8, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('32000.00'),
    'monatsrate': Decimal('497.71'),  # Fixe Rate (Zins + Tilgung)
    'zins_satz': Decimal('6.742') / 100,
    'zinsmethode': '30/360'
}

def berechne_monatszinsen(kapital: Decimal) -> Decimal:
    return (kapital * darlehen['zins_satz'] / 12).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

def darlehens_entwicklung(target_date: date) -> Decimal:
    aktuelles_datum = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while aktuelles_datum <= target_date:
        # Zinsen berechnen und abziehen
        zinsen = berechne_monatszinsen(kapital)
        kapital += zinsen  # Zinsen addieren
        
        # Rate am 15. des Monats abziehen
        if aktuelles_datum.day == 15 and aktuelles_datum >= darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        # Nächsten Monat (30-Tage-Schritt für 30/360)
        aktuelles_datum += timedelta(days=30)
    
    return kapital * Decimal('-1')  # Korrektur: Negativen Wert anzeigen

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{abs(aktueller_stand):.0f}€",  # Absoluter Wert ohne Vorzeichen
                "icon": "3309",  # Korrektes Icon
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
