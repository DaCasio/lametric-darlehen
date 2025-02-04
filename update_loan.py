from datetime import datetime

start_date = datetime(2025, 1, 15)
end_date = datetime(2030, 3, 15)
total_days = (end_date - start_date).days
today = datetime.now()
days_passed = (today - start_date).days

start_amount = 25995.73
current_value = start_amount - (start_amount / total_days) * days_passed

with open("darlehen.json", "w") as f:
    f.write(f'''{{
    "frames": [
        {{
            "text": "{max(current_value, 0):.2f}€",
            "icon": "i3219",
            "goalData": {{
                "start": {start_amount},
                "current": {max(current_value, 0)},
                "end": 0,
                "unit": "€"
            }}
        }}
    ]
}}''')
