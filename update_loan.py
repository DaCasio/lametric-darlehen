from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN
import json

# KOMPLETTER TILGUNGSPLAN (2023-2030)
TILGUNGSPLAN = {
    date(2023, 8, 15): Decimal('32000.00'),
    date(2023, 9, 15): Decimal('31502.29'),
    date(2023, 10, 15): Decimal('31004.58'),
    date(2023, 11, 15): Decimal('30506.87'),
    date(2023, 12, 15): Decimal('30009.16'),
    date(2024, 1, 15): Decimal('29511.45'),
    date(2024, 2, 15): Decimal('29013.74'),
    date(2024, 3, 15): Decimal('28516.03'),
    date(2024, 4, 15): Decimal('28018.32'),
    date(2024, 5, 15): Decimal('27520.61'),
    date(2024, 6, 15): Decimal('27022.90'),
    date(2024, 7, 15): Decimal('26525.19'),
    date(2024, 8, 15): Decimal('26027.48'),
    date(2024, 9, 15): Decimal('25529.77'),
    date(2024, 10, 15): Decimal('25032.06'),
    date(2024, 11, 15): Decimal('24534.35'),
    date(2024, 12, 15): Decimal('24036.64'),
    date(2025, 1, 15): Decimal('23538.93'),
    date(2025, 2, 15): Decimal('23041.22'),
    date(2025, 3, 15): Decimal('22543.51'),
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
    # 1. Finde den letzten Stichtag vor/nach dem Target-Datum
    stichtage = sorted(TILGUNGSPLAN.keys())
    
    if target_date < stichtage[0]:
        return TILGUNGSPLAN[stichtage[0]]
    
    if target_date >= stichtage[-1]:
        return Decimal('0.00')
    
    for i, stichtag in enumerate(stichtage):
        if stichtag > target_date:
            vorheriger_stichtag = stichtage[i-1]
            nächster_stichtag = stichtag
            break
    
    # 2. Exakter Wert für Stichtage
    if target_date == vorheriger_stichtag:
        return TILGUNGSPLAN[vorheriger_stichtag]
    
    # 3. Tägliche lineare Reduktion
    tage_zwischen = (nächster_stichtag - vorheriger_stichtag).days
    tage_seit_letztem = (target_date - vorheriger_stichtag).days
    
    differenz = TILGUNGSPLAN[vorheriger_stichtag] - TILGUNGSPLAN[nächster_stichtag]
    tägliche_reduktion = differenz / tage_zwischen
    aktueller_stand = TILGUNGSPLAN[vorheriger_stichtag] - (tägliche_reduktion * tage_seit_letztem)
    
    return aktueller_stand.quantize(Decimal('1.00'), rounding=ROUND_DOWN)

def generiere_json():
    return {
        "frames": [
            {
                "text": f"{darlehens_entwicklung(date.today()):.0f}€",
                "icon": "3309",
                "goalData": {
                    "start": 32000,
                    "current": int(darlehens_entwicklung(date.today())),
                    "end": 0,
                    "unit": "€"
                }
            }
        ]
    }

if __name__ == "__main__":
    # HARTKODIERTE VALIDIERUNG
    assert darlehens_entwicklung(date(2025,4,15)) == Decimal('24934.82'), "April 2025 fehlerhaft"
    assert darlehens_entwicklung(date(2025,5,15)) == Decimal('24577.20'), "Mai 2025 fehlerhaft"
    
    with open("darlehen.json", "w") as f:
        json.dump(generiere_json(), f, indent=2, ensure_ascii=False)
