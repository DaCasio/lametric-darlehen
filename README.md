Hier ist eine ausführlichere und detaillierte Beschreibung für die `README.md`, die alle Aspekte deines Projektes erklärt und gleichzeitig professionell und gut strukturiert ist:

---

# LaMetric Darlehen Tracker

Dieses Projekt bietet eine automatisierte Möglichkeit, den Verlauf eines Darlehens zu verfolgen und die aktuellen Werte täglich in einer JSON-Datei zu speichern. Das Ziel ist, die Daten in die LaMetric My Data DIY App zu integrieren, damit der Darlehensstand bequem und visuell dargestellt werden kann.

---

## Überblick

Das **LaMetric Darlehen Tracker** ermöglicht die Berechnung und Aktualisierung eines Darlehens basierend auf den folgenden Parametern:

- **Startdatum:** 15. Januar 2025
- **Enddatum:** 15. März 2030
- **Startkapital:** 25.995,73 €
- **Monatsrate:** 503,16 €
- **Zinssatz:** 6,74 % p.a. (360-Tage-Jahr, nach der 30/360-Methode)

Das Python-Skript berechnet den verbleibenden Betrag dieses Darlehens basierend auf täglichen Zinsen sowie monatlichen Raten und schreibt die Ergebnisse in eine `darlehen.json`-Datei. Diese Datei kann direkt in die LaMetric App eingebunden werden, sodass die Live-Daten jederzeit abrufbar sind.

Die gesamte Berechnung wird durch **GitHub Actions** automatisiert, welche das Skript täglich um Mitternacht (UTC) ausführt und sicherstellt, dass die JSON-Daten aktuell bleiben.

---

## Projektstruktur

Die Repository-Struktur sieht wie folgt aus:

```
lametric-darlehen/
│
├── update_loan.py              # Python-Skript zur Berechnung der Darlehensdaten
├── darlehen.json               # Automatisch generierte JSON-Datei mit den Daten
├── .github/
│   └── workflows/
│       └── update.yml          # GitHub Actions Workflow zur täglichen Ausführung
├── README.md                   # Projektbeschreibung (diese Datei)
```

### **Dateien im Detail**

#### **1. `update_loan.py`**

- Diese Datei enthält das Python-Skript, das den Darlehensverlauf täglich berechnet.
- Es basiert auf den o.g. Parametern (Startkapital, Zinssatz, Monatsraten, etc.).
- Es nutzt das 30/360-Konzept für die Zinssatzberechnung.
- Die Ergebnisse werden in eine JSON-Datei (`darlehen.json`) geschrieben.

#### **2. `darlehen.json`**

- Diese Datei wird automatisch durch `update_loan.py` erstellt und enthält die aktuellen Darlehensstände im JSON-Format.
- Beispielausgabe:

```json
{
  "frames": [
    {
      "text": "25360€",
      "icon": "i616",
      "goalData": {
        "start": 25996,
        "current": 25360,
        "end": 0,
        "unit": "€"
      }
    }
  ]
}
```

- Die Datei kann direkt in die **LaMetric My Data App** eingebunden werden, um den Darlehensstand auf einem LaMetric-Display anzuzeigen.

#### **3. `.github/workflows/update.yml`**

- Dieser Workflow sorgt dafür, dass das Python-Skript täglich um Mitternacht (UTC) ausgeführt wird.
- Nach der Berechnung werden Änderungen an `darlehen.json` automatisch ins Repository zurückgeschrieben.
- Der Workflow wurde so konzipiert, dass er auch manuell auslösbar ist, falls ein sofortiges Update benötigt wird.

---

## Funktionsweise & Ablauf

### Wie es funktioniert:

1. **Automatische tägliche Berechnung**  
   Täglich wird das Python-Skript ausgeführt, welches:
   - Die Zinsen für jeden Tag basierend auf dem aktuellen Kapitalstand berechnet.
   - Jeden Monat (am 15.) die Monatsrate abzieht.
   - Den neuen Stand in die Datei `darlehen.json` schreibt.

2. **Datenvalidierung**  
   - Am Stichtag **15. Februar 2025** wird das Ergebnis mit einem Zielwert validiert (25.644 € ± 2€).  
   - Falls der Wert außerhalb dieser Toleranz liegt, wird die Ausführung gestoppt.  
   - Nach diesem Datum wird die Validierung automatisch entfernt.

3. **Integration mit LaMetric**  
   - Die generierte JSON-Datei kann in die LaMetric My Data DIY App importiert werden.  
   - Die App visualisiert den Darlehensstand auf einem LaMetric-Display.

4. **GitHub Actions Automatisierung**  
   - Eine GitHub Action führt das Skript täglich aus, aktualisiert die JSON-Datei und committet die Änderungen zurück ins Repository.  
   - Es ist keine manuelle Interaktion erforderlich.

---

## Einrichtung

### Voraussetzungen

- Python 3.9 oder höher sollte lokal installiert sein.
- Ein GitHub-Repository mit aktiviertem GitHub Actions Feature.

### Schritte zur Einrichtung

1. **Repository erstellen**  
   Erstelle ein neues GitHub-Repository mit einem beliebigen Namen (z.B. `lametric-darlehen`).

2. **Dateien hinzufügen**  
   - Füge die Datei `update_loan.py` mit dem bereitgestellten Python-Code hinzu.
   - Lege die Datei `.github/workflows/update.yml` an, um die täglichen Updates zu automatisieren.
   - Erstelle die `README.md`-Datei (diese Datei) und passe sie bei Bedarf an.

3. **Erster Commit & Push**  
   Committe alle Änderungen und pushe sie ins Repository.

4. **LaMetric My Data konfigurieren**  
   - Gehe zur LaMetric App und richte eine neue My Data DIY App ein.  
   - Verlinke die generierte `darlehen.json`-Datei als Datenquelle.

---

## Anpassungen

Da das Projekt flexibel ist, kannst du es bei Bedarf anpassen:

### **1. Darlehensparameter ändern**
- Bearbeite die `darlehen`-Variable in `update_loan.py`, um neue Startwerte (Kapital, Zins, Monatsrate etc.) festzulegen.

```python
darlehen = {
    'start_date': date(2025, 1, 15),
    'end_date': date(2030, 3, 15),
    'start_kapital': Decimal('25995.73'),
    'monatsrate': Decimal('503.16'),
    'zins_satz': Decimal('6.74') / 100,
    'zinsmethode': '30/360'
}
```

### **2. Zielwertvalidierung anpassen**
- Der Zielwert am **15. Februar 2025** kann ebenfalls angepasst werden. Ändere einfach die Toleranz oder das Ziel in der folgenden Zeile:

```python
assert 25642 <= aktueller_wert <= 25646, f"Abweichung: {aktueller_wert}€ statt 25644€"
```

### **3. Workflow-Zeitplan ändern**
- Die Ausführungszeit des Workflows kann in der `update.yml`-Datei leicht geändert werden, indem du den CRON-Ausdruck anpasst:

```yaml
schedule:
  - cron: '0 0 * * *'  # Aktuell: Täglich um 00:00 UTC
```

---

## Beispiel: Verwendung der LaMetric DIY App

1. Rufe die generierte Datei `darlehen.json` im Browser auf, z.B.:  
   `https://raw.githubusercontent.com/username/lametric-darlehen/main/darlehen.json`.

2. Kopiere die URL und füge sie in der **My Data**-App von LaMetric ein.

3. Konfiguriere die Anzeige (z.B. Icon, Werte etc.), um live den Darlehensstand zu verfolgen.

---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details findest du in der Datei `LICENSE`.

---

Viel Erfolg mit dem **LaMetric Darlehen Tracker**! 🎉

--- 
