from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN, getcontext
import json

getcontext().prec = 8

darlehen = {
    'start_date': date(2023, 8, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('32000.00'),
    'monatsrate': Decimal('497.71'),  # Fixe Monatsrate (Zins + Tilgung)
    'zins_satz': Decimal('6.742') / 100,
    'zinsmethode': '30/360'
}

def berechne_monatszinsen(kapital: Decimal) -> Decimal:
    return (kapital * darlehen['zins_satz']) / 12

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = darlehen['start_date']
    kapital = darlehen['start_kapital']
    
    while current_date <= target_date:
        # Zinsen für den Monat berechnen (30/360-Methode)
        zinsen = berechne_monatszinsen(kapital)
        kapital += zinsen
        
        # Monatsrate am 15. jedes Monats abziehen
        if current_date.day == 15 and current_date >= darlehen['start_date']:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        # Nächsten Monat berechnen (30-Tage-Annäherung)
        current_date += timedelta(days=30)
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{int(aktueller_stand)}€",
                "icon": "616",  # Korrektes Icon-Format ohne "i"
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
    
    # Validierung für den 15.05.2025 (±2€ Toleranz)
    if date.today() == date(2025, 5, 15):
        aktueller_wert = darlehens_entwicklung(date.today())
        assert 24575 <= aktueller_wert <= 24579, f"Abweichung: {aktueller_wert}€ statt 24577,20€"
