# Portscanner

Ett enkelt Python-verktyg som använder Nmap (via python-nmap) för att:
- skanna portar på en eller flera värdar,
- läsa in mål och portar från en JSON-fil,
- spara resultat till JSON- eller textfil,
- köras antingen interaktivt via textmenyer eller via kommandoraden (CLI).

Verktyget skriver ut för varje värd:
- värdnamn och status (up/down),
- protokoll (t.ex. tcp/udp),
- portnummer samt status (open/closed/filtered),
- tjänstens namn, produkt och version (om Nmap kan identifiera det).

---

## Innehåll
- Förutsättningar
- Installation
- Snabbstart
- Användning via textmeny (interaktiv)
- Användning via kommandoraden (CLI)
- Indata- och utdataformat
- Exempel
- Felsökning och vanliga fel
- Etik och ansvar

---

## Förutsättningar

- Python 3.8+ (rekommenderat 3.10+)
- Systempaket:
  - [Nmap](https://nmap.org/) måste vara installerat på systemet.
- Python-paket:
  - `python-nmap` (wrapper för Nmap)

Installera Nmap:
- macOS (Homebrew): `brew install nmap`
- Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y nmap`
- Fedora: `sudo dnf install -y nmap`
- Windows (chocolatey): `choco install nmap` eller ladda ner från [nmap.org](https://nmap.org/download.html)

Installera Python-beroendet:
```bash
python3 -m pip install python-nmap
```

---

## Installation

Placera `port_scanner.py` i valfri katalog. Valfritt: skapa en virtuell miljö.

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python3 -m pip install python-nmap
```

Säkerställ också att kommandot `nmap` fungerar i din terminal:
```bash
nmap -V
```

---

## Snabbstart

- Interaktivt läge (textmeny):
```bash
python3 port_scanner.py
```

- CLI (direkt från kommandoraden):
```bash
python3 port_scanner.py --host 192.168.1.10 --ports 22,80,443
```

- Spara resultat till filer:
```bash
python3 port_scanner.py --host scanme.nmap.org --ports 20-100 --output resultat.json --output-text resultat.txt
```

- Läsa in värd och portar från JSON-fil:
```bash
python3 port_scanner.py --input input.json
```

---

## Användning via textmeny (interaktiv)

Starta utan argument:
```bash
python3 port_scanner.py
```

Menyn låter dig:
1. Ange värd manuellt (t.ex. `scanme.nmap.org` eller `192.168.1.10`)
2. Ange port(ar) manuellt (t.ex. `80` eller `22,80,443` eller intervall `20-80`)
3. Ladda värd och portar från JSON-fil (se format nedan)
4. Starta skanning
5. Spara resultat till JSON-fil
6. Spara resultat till textfil
0. Avsluta

Typiskt flöde:
- Ange värd
- Ange portar
- Starta skanning
- Spara resultat (valfritt)

Notera:
- Skanningsresultat görs tillgängligt för sparfunktionerna efter att du kört alternativ 4.

---

## Användning via kommandoraden (CLI)

Visa hjälp:
```bash
python3 port_scanner.py -h
```

Flaggor:
- `--host, -H`         Värd att skanna (t.ex. `example.com` eller `192.168.1.10`)
- `--ports, -p`        Port(ar) att skanna (t.ex. `80`, `22,80,443` eller intervall `20-80`)
- `--input, -i`        Ladda värd och portar från en JSON-fil (se format nedan)
- `--output, -o`       Spara resultat till JSON-fil (rådata från Nmap)
- `--output-text, -t`  Spara resultat till textfil (läsbar sammanställning)

Observera:
- Du måste ange både `--host` och `--ports`, eller använda `--input` som innehåller båda.
- Om du startar skriptet utan argument går det in i det interaktiva läget med textmeny.

---

## Indata- och utdataformat

- JSON-indatafil för `--input`:
```json
{
  "host": "scanme.nmap.org",
  "ports": "20-80"
}
```

- JSON-utdata från `--output`:
  - Är den råa datastrukturen som `python-nmap` returnerar från `nmap.PortScanner().scan(...)`.
  - Lätt att vidarebearbeta med t.ex. `jq` eller i andra program.

- Textutdata från `--output-text`:
  - Mänskligt läsbar lista över värdar, protokoll, portar, status, namn, produkt och version (om tillgängligt).

---

## Exempel

- Skanna SSH och HTTP på en lokal värd:
```bash
python3 port_scanner.py --host 192.168.1.50 --ports 22,80
```

- Skanna ett portintervall och spara resultat:
```bash
python3 port_scanner.py --host scanme.nmap.org --ports 1-1024 --output scan.json --output-text scan.txt
```

- Använd JSON-indatafil:
```bash
# input.json
# {
#   "host": "scanme.nmap.org",
#   "ports": "20-80"
# }
python3 port_scanner.py --input input.json --output out.json
```

---

## Felsökning och vanliga fel

- “Fel vid skanning: …”
  - Kontrollera att `nmap` är installerat och åtkomligt i PATH (`nmap -V`).
  - Se till att du har behörigheter. Vissa skanningstyper kan kräva administratörsrättigheter.
- “Fel: Både --host och --ports måste anges”
  - Ange båda parametrarna, eller använd `--input` med båda fälten i JSON.
  - Alternativt: starta utan argument för att använda den interaktiva menyn.
- Tomma fält i resultat (t.ex. produkt/version):
  - Nmap kan inte alltid identifiera tjänstens produkt och version på en port.
- Resultat saknas när du försöker spara i menyläget:
  - Kör först “Starta skanning” (alternativ 4) i menyn, därefter spara.

Tips:
- Stora portintervall tar längre tid.
- Nätverksfilter/brandväggar kan påverka resultat (t.ex. “filtered”).

---

## Etik och ansvar

Använd endast detta verktyg för system du äger eller har uttryckligt tillstånd att testa. Obehörig portskanning kan vara olaglig och/eller bryta mot policyer. Du ansvarar själv för hur du använder verktyget.