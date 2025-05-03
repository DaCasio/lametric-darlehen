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
    
    while current_date <= target_date:
        # Bestimme das nächste Zahlungsdatum (15. des nächsten Monats)
        next_payment = current_date.replace(day=15) + timedelta(days=31)
        next_payment = next_payment.replace(day=15)
        
        # Berechne Tage bis zum nächsten Zahlungstermin oder Target-Datum
        tage_bis = (min(next_payment, target_date) - current_date).days
        zinsen = berechne_tägliche_zinsen(kapital, tage_bis)
        kapital += zinsen
        
        # Monatsrate abziehen, wenn Zahlungstermin erreicht
        if next_payment <= target_date:
            kapital -= darlehen['monatsrate']
            kapital = kapital.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        current_date = min(next_payment, target_date)
    
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
