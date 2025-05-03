from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN
import json

# Kompletter Tilgungsplan (15. jedes Monats bis 03/2030)
TILGUNGSPLAN = {
    date(2025, 4, 15): Decimal('24934.82'),
    date(2025, 5, 15): Decimal('24577.20'),
    date(2025, 6, 15): Decimal('24217.57'),
    date(2025, 7, 15): Decimal('23855.92'),
    date(2025, 8, 15): Decimal('23492.24'),
    date(2025, 9, 15): Decimal('23126.52'),
    date(2025, 10, 15): Decimal('22758.74'),
    date(2025, 11, 15): Decimal('22388.90'),
    date(2025, 12, 15): Decimal('22016.98'),
    date(2026, 1, 15): Decimal('21642.97'),
    date(2026, 2, 15): Decimal('21266.86'),
    date(2026, 3, 15): Decimal('20888.63'),
    date(2026, 4, 15): Decimal('20508.28'),
    date(2026, 5, 15): Decimal('20125.79'),
    date(2026, 6, 15): Decimal('19741.15'),
    date(2026, 7, 15): Decimal('19354.35'),
    date(2026, 8, 15): Decimal('18965.38'),
    date(2026, 9, 15): Decimal('18574.22'),
    date(2026, 10, 15): Decimal('18180.87'),
    date(2026, 11, 15): Decimal('17785.31'),
    date(2026, 12, 15): Decimal('17387.52'),
    date(2027, 1, 15): Decimal('16987.50'),
    date(2027, 2, 15): Decimal('16585.23'),
    date(2027, 3, 15): Decimal('16180.70'),
    date(2027, 4, 15): Decimal('15773.90'),
    date(2027, 5, 15): Decimal('15364.81'),
    date(2027, 6, 15): Decimal('14953.42'),
    date(2027, 7, 15): Decimal('14539.72'),
    date(2027, 8, 15): Decimal('14123.70'),
    date(2027, 9, 15): Decimal('13705.34'),
    date(2027, 10, 15): Decimal('13284.63'),
    date(2027, 11, 15): Decimal('12861.56'),
    date(2027, 12, 15): Decimal('12436.11'),
    date(2028, 1, 15): Decimal('12008.27'),
    date(2028, 2, 15): Decimal('11578.03'),
    date(2028, 3, 15): Decimal('11145.37'),
    date(2028, 4, 15): Decimal('10710.28'),
    date(2028, 5, 15): Decimal('10272.74'),
    date(2028, 6, 15): Decimal('9832.75'),
    date(2028, 7, 15): Decimal('9390.28'),
    date(2028, 8, 15): Decimal('8945.33'),
    date(2028, 9, 15): Decimal('8497.88'),
    date(2028, 10, 15): Decimal('8047.91'),
    date(2028, 11, 15): Decimal('7595.42'),
    date(2028, 12, 15): Decimal('7140.38'),
    date(2029, 1, 15): Decimal('6682.79'),
    date(2029, 2, 15): Decimal('6222.63'),
    date(2029, 3, 15): Decimal('5759.88'),
    date(2029, 4, 15): Decimal('5294.53'),
    date(2029, 5, 15): Decimal('4826.57'),
    date(2029, 6, 15): Decimal('4355.98'),
    date(2029, 7, 15): Decimal('3882.74'),
    date(2029, 8, 15): Decimal('3406.84'),
    date(2029, 9, 15): Decimal('2928.27'),
    date(2029, 10, 15): Decimal('2447.01'),
    date(2029, 11, 15): Decimal('1963.05'),
    date(2029, 12, 15): Decimal('1476.37'),
    date(2030, 1, 15): Decimal('986.95'),
    date(2030, 2, 15): Decimal('494.79'),
    date(2030, 3, 15): Decimal('0.00')
}

def darlehens_entwicklung(target_date: date) -> Decimal:
    # Finde den nächstgelegenen Stichtag
    stichtage = sorted(TILGUNGSPLAN.keys())
    vorheriger_stichtag = stichtage[0]
    for stichtag in stichtage:
        if stichtag > target_date:
            break
        vorheriger_stichtag = stichtag
    
    nächster_stichtag = vorheriger_stichtag + timedelta(days=30)  # Monatlicher Rhythmus
    
    # Lineare Interpolation zwischen den Stichtagen
    tage_gesamt = (nächster_stichtag - vorheriger_stichtag).days
    tage_seit_letztem = (target_date - vorheriger_stichtag).days
    anteil = Decimal(tage_seit_letztem) / Decimal(tage_gesamt)
    
    differenz = TILGUNGSPLAN.get(vorheriger_stichtag, Decimal('32000')) - TILGUNGSPLAN.get(nächster_stichtag, Decimal('0'))
    aktueller_stand = TILGUNGSPLAN[vorheriger_stichtag] - (differenz * anteil)
    
    return aktueller_stand.quantize(Decimal('1'), rounding=ROUND_DOWN)

def generiere_json():
    aktueller_stand = darlehens_entwicklung(date.today())
    return {
        "frames": [
            {
                "text": f"{aktueller_stand}€",
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
    # Vollständige Validierung aller Stichtage
    for stichtag, sollwert in TILGUNGSPLAN.items():
        assert darlehens_entwicklung(stichtag) == sollwert, f"Fehler am {stichtag}"
    
    with open("darlehen.json", "w") as f:
        json.dump(generiere_json(), f, indent=2, ensure_ascii=False)
