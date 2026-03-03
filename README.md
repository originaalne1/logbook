# 🛠️ IT Hoolduspäevik Pro (v4.1)

IT Hoolduspäevik on Pythonis kirjutatud terviklik lahendus IT-hooldustööde, paranduste ja ülesannete haldamiseks. Rakendus pakub kahte kasutajaliidest ühes failis: kiiret CLI-d (käsurida) ja moodsat GUI-d (graafiline aken).

Projekt on loodud fookusega kasutusmugavusele, automaatsele salvestamisele ja andmete valideerimisele.

## ✨ Funktsionaalsus

### 🖥️ Kaks Liidest

GUI (Graafiline Liides): Moodne Flat Design välimus, värvikoodidega staatused (🔴 AVATUD / 🟢 TEHTUD), reaalajas otsing ja sorteeritav tabel.

CLI (Käsurida): Lihtne ja kiire tekstipõhine menüü terminalis kasutamiseks.

### 🚀 Põhiomadused

Automaatne salvestamine: Kõik toimingud (lisamine, kustutamine, muutmine) salvestatakse koheselt logbook.json faili.

Tark CSV Import: Tuvastab automaatselt eraldaja (koma või punktkoma) ja impordib andmed.

Vigade haldus: Vigased CSV read (nt vale kuupäev või lühike kirjeldus) ei riku andmebaasi, vaid salvestatakse eraldi faili import_errors.log.

Reaalajas otsing: Filtreeri töid pealkirja või kirjelduse järgi.

Andmete valideerimine:

Pealkiri: vähemalt 4 tähemärki.

Kirjeldus: vähemalt 10 tähemärki.

Staatus: ainult "OPEN" või "DONE".

Kuupäev: toetab ISO (YYYY-MM-DD) ja Eesti (DD.MM.YYYY) vorminguid.

## ⚙️ Paigaldamine ja Käivitamine

Projekt ei vaja väliseid lisateeke (kõik vajalik on Pythoni standardteegis).

### Eeldused

Python 3.x

### Käivitamine

Lae alla fail main.py.

Ava terminal või käsurida kaustas, kus fail asub.

Käivita rakendus:
```
python main.py
```

Vali käivitamisel soovitud liides:

Vajuta 1 ja Enter konsoolirežiimi (CLI) jaoks.

Vajuta 2 või lihtsalt Enter graafilise režiimi (GUI) jaoks.

## 📖 Kasutusjuhend (GUI)

Uue töö lisamine:

Täida väljad "Töö pealkiri" ja "Detailne kirjeldus".

Vajuta nuppu LISA KIRJE (või Enter).

Töö ilmub tabelisse staatusega "🔥 AVATUD".

Staatuse muutmine:

Vali tabelist rida.

Vajuta nuppu ✅ MÄRGI TEHTUKS / AVA.

Staatus muutub roheliseks (TEHTUD) või punaseks (AVATUD).

Kustutamine:

Vali rida ja vajuta 🗑️ KUSTUTA KIRJE.

CSV Importimine:

Vajuta 📂 IMPORTI CSV ja vali fail.

Programm annab teada, mitu rida õnnestus ja mitu ebaõnnestus.

## 📂 CSV Faili Vorming

Importimiseks sobib CSV fail, kus andmed on eraldatud koma (,) või punktkomaga (;). Päiserida ei ole kohustuslik, kuid veergude järjekord peab olema:

Kuupäev, Pealkiri, Kirjeldus, Staatus

Näide (import.csv):
```
2026-02-16 14:30:00, Printeri hooldus, Tooneri vahetus ja testprint, DONE
2026-02-16 15:00:00, Võrgu viga, Ruuteri taaskäivitus 2. korrusel, OPEN
16.02.2026 16:00:00, Serveri uuendus, Turvapaikade paigaldamine, OPEN
```

# 🏗️ Failistruktuur

main.py - Rakenduse lähtekood (käivitatav).

logbook.json - Peamine andmebaas (tekib automaatselt).

import_errors.log - Logifail vigaste importide jaoks (tekib vajadusel).

# 🎨 Tehniline info

Disain: Tkinter "Clam" teema kohandatud värvipaletiga.

Värvid:

Päis: #2C3E50 (Tumesinine)

Taust: #ECF0F1 (Helehall)

Edukas/Tehtud: #27AE60 (Roheline)

Hoiatus/Avatud: #E74C3C (Punane)

Aktsent: #3498DB (Sinine)

Märkus: See projekt on loodud õppeotstarbel, demonstreerimaks Pythoni objektorienteeritud programmeerimist (OOP), failihaldust ja GUI loomist.