# Toolbox

Observera: All dokumentation i detta repo är AI-genererad.

Toolbox är ett paket med flera Python-baserade verktyg som kan användas i utbildningssyfte inom IT-säkerhet och enklare penetrationstester. Paketet innehåller:
- Portscanner (Nmap-baserad)
- Krypteringsverktyg (filkryptering/-dekryptering med Fernet)
- Hash Cracker (hashning, verifiering, ordlistebaserad knäckning och AI-baserad hashtypidentifiering)

Du kan köra hela toolboxen via en gemensam meny eller använda varje verktyg fristående via kommandoraden.

---

## Innehåll
- Installation och setup (venv + requirements.txt)
- Snabbstart
- Köra hela toolboxen (huvudmeny)
- Köra enskilda verktyg
  - Portscanner
  - Krypteringsverktyg
  - Hash Cracker
- Ordlistor (Hash Cracker)
- Felsökning
- Etik och ansvar

---

## Installation och setup (venv + requirements.txt)

Förutsättningar:
- Python 3.8+ (rekommenderat 3.10+)
- Git (om du klonar repo)
- Systempaket för portscanning:
  - Nmap måste vara installerat och åtkomligt via ditt PATH (krävs för portscannern)
    - macOS (Homebrew): `brew install nmap`
    - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y nmap`
    - Fedora: `sudo dnf install -y nmap`
    - Windows: `choco install nmap` eller ladda ner från [nmap.org](https://nmap.org/download.html)

Rekommenderad installation med virtuell miljö samt requirements.txt:
```bash
# 1) Klona repo (om tillämpligt)
git clone <REPO-URL>
cd <REPO-KATALOG>

# 2) Skapa och aktivera virtuell miljö
python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1
# Windows (cmd):
# .venv\Scripts\activate.bat

# 3) Uppgradera pip (valfritt men rekommenderat)
python -m pip install --upgrade pip

# 4) Installera alla Python-beroenden
pip install -r requirements.txt

# 5) Verifiera att nmap fungerar (krävs för portscannern)
nmap -V
```

Valfritt (för Hash Crackerns AI-baserade hashtypidentifiering):
- Installera [Ollama](https://ollama.com/) och se till att den körs på `http://localhost:11434`
- Hämta modellen `gpt-oss:120b`:
```bash
ollama pull gpt-oss:120b
```

---

## Snabbstart

- Starta hela toolboxen (huvudmeny):
```bash
python toolbox.py
# eller, om paketet är installerat som modul:
# python -m toolbox
```

- Starta ett enskilt verktyg direkt (som modul):
```bash
# Portscanner (interaktivt läge om inga argument ges)
python -m portscanner.portscanner

# Krypteringsverktyg (interaktivt läge om inga argument ges)
python -m cryptotool.crypto_tool

# Hash Cracker (interaktivt läge om inga argument ges)
python -m hashcracker.hashcracker
```

Tips: Varje verktyg har inbyggd CLI-hjälp:
```bash
python -m portscanner.portscanner -h
python -m cryptotool.crypto_tool -h
python -m hashcracker.hashcracker -h
```

---

## Köra hela toolboxen (huvudmeny)

Kör:
```bash
python toolbox.py
```

Du får en meny:
- 1. Portscanner
- 2. Krypteringsverktyg
- 3. Hash Cracker
- 0. Avsluta

Välj ett verktyg och följ de interaktiva menyerna för att mata in värd/portar (portscanner), fil/nyckel (kryptering) eller hashtyp/hashvärde/ordlista (hash cracker).

---

## Köra enskilda verktyg

### 1) Portscanner

Beskrivning:
- Skannar portar på en eller flera värdar via Nmap (via `python-nmap`).
- Kan läsa mål/portar från JSON, skriva resultat till JSON eller text.
- Interaktiv meny eller CLI.

Interaktivt läge:
```bash
python -m portscanner.portscanner
```
Menyn låter dig:
- ange värd och portar manuellt,
- ladda indata från JSON-fil,
- starta skanning,
- spara resultat till JSON eller textfil.

CLI-exempel:
```bash
# Skanna specifika portar
python -m portscanner.portscanner --host scanme.nmap.org --ports 22,80,443

# Skanna intervall och spara resultat
python -m portscanner.portscanner --host scanme.nmap.org --ports 1-1024 \
  --output resultat.json --output-text resultat.txt

# Ladda indata från JSON
# input.json:
# {
#   "host": "scanme.nmap.org",
#   "ports": "20-80"
# }
python -m portscanner.portscanner --input input.json --output out.json
```

Obs:
- Nmap måste vara installerat i systemet (`nmap -V`).
- Vissa skanningar kan kräva administratörsrättigheter.
- Brandväggar/filtrering kan påverka resultat.

---

### 2) Krypteringsverktyg (Fernet)

Beskrivning:
- Generera Fernet-nyckel.
- Kryptera fil med nyckel.
- Dekryptera tidigare krypterad fil.
- Interaktiv meny eller CLI.
- Fernet ger autenticerad kryptering; fel nyckel eller manipulerad fil ger dekrypteringsfel.

Interaktivt läge:
```bash
python -m cryptotool.crypto_tool
```

CLI-exempel:
```bash
# Generera ny nyckel
python -m cryptotool.crypto_tool --generate-key secret.key

# Kryptera fil
python -m cryptotool.crypto_tool --encrypt rapport.pdf --key secret.key
# => rapport.pdf.enc

# Dekryptera fil
python -m cryptotool.crypto_tool --decrypt rapport.pdf.enc --key secret.key
# => rapport.pdf.enc.dec
```

Obs:
- Nyckelfiler är känsliga – lagra och säkerhetskopiera säkert.
- Verktyget läser hela filen i minnet (mycket stora filer kan påverka minnesanvändning).

---

### 3) Hash Cracker

Beskrivning:
- Stöder: MD5, SHA1, SHA256, SHA512, NTLM, bcrypt, argon2.
- Funktioner: hasha lösenord, verifiera lösenord mot hash, knäcka hash med ordlista, identifiera hashtyp via AI (Ollama).
- Interaktiv meny eller CLI.

Interaktivt läge:
```bash
python -m hashcracker.hashcracker
```

CLI-exempel:
```bash
# Hasha ett lösenord
python -m hashcracker.hashcracker --hash-password "hemligt" --type SHA256

# Knäcka hash med ordlista
python -m hashcracker.hashcracker --crack --hash "<HASHVÄRDE>" --type SHA1 --wordlist passwords.txt

# Identifiera hashtyp via AI (kräver Ollama + modell gpt-oss:120b)
python -m hashcracker.hashcracker --identify --hash "<HASHVÄRDE>"
```

AI-baserad identifiering (valfritt):
- Ollama måste köras lokalt på `http://localhost:11434`
- Modellen `gpt-oss:120b` måste finnas: `ollama pull gpt-oss:120b`

---

## Ordlistor (Hash Cracker)

- Standardordlistan refererad i verktyget är `rockyou.txt` – OBS: den ingår inte i detta repo.
- För teständamål ingår en mycket liten delmängd: `passwords.txt`.
- Du kan ange valfri egen ordlista via menyn eller `--wordlist`.

Exempel:
```bash
python -m hashcracker.hashcracker --crack --hash "<HASHVÄRDE>" --type SHA1 --wordlist passwords.txt
```

---

## Felsökning

Allmänt:
- Säkerställ att den virtuella miljön är aktiv när du kör kommandon (`source .venv/bin/activate` eller motsvarande på Windows).
- Kör `pip install -r requirements.txt` efter att ha aktiverat venv.

Portscanner:
- “Fel vid skanning”: Verifiera att `nmap` är korrekt installerat (`nmap -V`) och åtkomligt i PATH.
- Tomma fält (produkt/version) kan förekomma om Nmap inte kan identifiera tjänsten.
- Stora portintervall tar lång tid; brandväggar kan rapportera “filtered”.

Krypteringsverktyg:
- “Fel: Nyckelfilen hittades inte” – generera en ny med `--generate-key` eller ange korrekt sökväg.
- “Fel vid kryptering/dekryptering” – kontrollera att nyckeln är en giltig Fernet-nyckel och att filen inte är skadad.

Hash Cracker:
- “Ordlista hittas inte” – kontrollera sökväg; `rockyou.txt` ingår inte i repo, använd `passwords.txt` för test.
- Ingen träff vid knäckning – lösenordet finns inte i ordlistan, testa större/annan ordlista.
- AI-identifiering misslyckas – kontrollera att Ollama körs och att `gpt-oss:120b` finns.

---

## Etik och ansvar

Dessa verktyg är avsedda för utbildning, återställning av egna uppgifter och säkerhetstester där du har uttryckligt tillstånd. Obehörig användning mot system du inte äger eller har tillstånd att testa kan vara olaglig. Du ansvarar själv för hur du använder verktygen.