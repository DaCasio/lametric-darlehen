from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN, getcontext
import json

# Präzisionskonfiguration
getcontext().prec = 8

# Darlehensparameter
DARLEHEN = {
    'start_date': date(2025, 1, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('25995.73'),
    'monatsrate': Decimal('497.71') + Decimal('5')  # 502,71 €
    'zins_satz': Decimal('6.74') / Decimal('100'),  # 6.74% p.a.
    'zinsmethode': '30/360'  # Bankenstandard
}

def berechne_tägliche_zinsen(kapital: Decimal, zins_satz: Decimal) -> Decimal:
    """Berechnet tägliche Zinsen nach 30/360-Methode"""
    return (kapital * zins_satz) / Decimal('360')

def darlehens_entwicklung(target_date: date) -> Decimal:
    current_date = DARLEHEN['start_date']
    kapital = DARLEHEN['start_kapital']
    
    while current_date <= target_date:
        # Monatsrate am 15. ab dem 2. Monat
        if current_date.day == 15 and current_date > DARLEHEN['start_date']:
            kapital -= DARLEHEN['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        else:
            # Tägliche Zinsberechnung
            zinsen = berechne_tägliche_zinsen(kapital, DARLEHEN['zins_satz'])
            kapital += zinsen
        
        current_date += timedelta(days=1)
    
    return kapital.quantize(Decimal('1'), rounding=ROUND_DOWN)

def generiere_json_ausgabe():
    heute = date.today()
    aktueller_stand = darlehens_entwicklung(heute)
    
    return {
        "frames": [
            {
                "text": f"{int(aktueller_stand)}€",
                "icon": "i616",
                "goalData": {
                    "start": int(DARLEHEN['start_kapital'].quantize(Decimal('1'))),
                    "current": int(aktueller_stand),
                    "end": 0,
                    "unit": "€"
                }
            }
        ]
    }

# Hauptausführung
if __name__ == "__main__":
    daten = generiere_json_ausgabe()
    
    with open("darlehen.json", "w", encoding='utf-8') as datei:
        json.dump(daten, datei, indent=2, ensure_ascii=False)
