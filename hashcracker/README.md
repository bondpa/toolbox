# Hash Cracker

Ett enkelt, interaktivt Python-verktyg för att:
- hasha lösenord,
- verifiera lösenord mot ett givet hashvärde,
- försöka knäcka (cracka) hashade lösenord med en ordlista,
- identifiera sannolik hashtyp via en lokal AI-modell (Ollama).

Stöd för följande hashalgoritmer:
- MD5
- SHA1
- SHA256
- SHA512
- NTLM
- bcrypt
- argon2

Verktyget kan köras på två sätt:
1) Interaktiv textmeny (enkelt för manuell användning)
2) Kommandoraden med flaggor (smidigt för skriptning/automation)

---

## Innehåll
- Förutsättningar
- Ordlistor (viktigt!)
- Installation
- Snabbstart
- Användning via textmeny (interaktiv)
- Användning via kommandoraden (CLI)
- Exempel
- AI-baserad identifiering av hashtyp (Ollama)
- Felsökning och vanliga fel
- Noteringar och begränsningar
- Etik och ansvar

---

## Förutsättningar

- Python 3.8+ (rekommenderat 3.10+)
- Paket:
  - `passlib` (för NTLM via `passlib.hash.nthash`)
  - `bcrypt`
  - `argon2-cffi` (ger `from argon2 import PasswordHasher`)
  - `requests`

Installera Python-beroenden:
```bash
python3 -m pip install passlib bcrypt argon2-cffi requests
```

För AI-baserad hashtypidentifiering (valfritt):
- [Ollama](https://ollama.com/) installerad och igång lokalt på port `11434`
- En modell med namnet `gpt-oss:120b` tillgänglig i Ollama

---

## Ordlistor (viktigt!)

- Standardordlistan i verktyget är `rockyou.txt`, men OBS: den ingår inte i detta repo. Du behöver skaffa den separat om du vill använda den.
- För teständamål ingår en mycket liten delmängd: `passwords.txt`. Den kan användas för snabba, reproducerbara tester.
- Du kan peka på valfri egen ordlista via menyvalet ”Välj ordlista” eller flaggan `--wordlist`.

Exempel:
```bash
# Testa med den lilla testlistan
python3 hash_cracker.py --crack --hash "<HASHVÄRDE>" --type SHA1 --wordlist passwords.txt
```

---

## Installation

Placera `hash_cracker.py` i valfri katalog. Skapa gärna en virtuell miljö:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python3 -m pip install passlib bcrypt argon2-cffi requests
```

Lägg din ordlista (t.ex. `rockyou.txt` eller `passwords.txt`) i samma katalog eller ange full sökväg vid körning.

---

## Snabbstart

- Starta interaktiv meny:
```bash
python3 hash_cracker.py
```

- Cracking via CLI med testlistan:
```bash
python3 hash_cracker.py --crack --hash "<HASHVÄRDE>" --type SHA256 --wordlist passwords.txt
```

- Hasha ett lösenord via CLI:
```bash
python3 hash_cracker.py --hash-password "mittLösen" --type bcrypt
```

- Identifiera hashtyp via AI (Ollama krävs):
```bash
python3 hash_cracker.py --identify --hash "<HASHVÄRDE>"
```

---

## Användning via textmeny (interaktiv)

Kör:
```bash
python3 hash_cracker.py
```

Menyn visar aktuell status (vald hashtyp, hashvärde och ordlista) och följande alternativ:

1. Ange hashtyp (MD5, SHA1, SHA256, SHA512, NTLM, bcrypt, argon2)
2. Ange hashvärde
3. Välj ordlista (standard: rockyou.txt – ingår inte i repot; `passwords.txt` finns för test)
4. Starta knäckning (cracking)
5. Hasha ett lösenord (generera hash av ett klartextlösenord)
6. Verifiera ett lösenord mot det angivna hashvärdet
7. Identifiera hashtyp från angivet hashvärde (kräver Ollama på port 11434)
0. Avsluta

Typiska flöden:
- Knäcka en hash:
  1) Välj hashtyp
  2) Ange hashvärde
  3) Välj ordlista (t.ex. passwords.txt vid test)
  4) Starta knäckning
- Hasha ett lösenord:
  1) Välj hashtyp
  2) Välj "Hasha ett lösenord" och följ instruktionerna
  3) Du kan välja att använda det genererade hashvärdet direkt i menyn
- Verifiera ett lösenord:
  1) Välj hashtyp och ange hashvärde
  2) Välj "Verifiera ett lösenord" och skriv in lösenordet

---

## Användning via kommandoraden (CLI)

Visa hjälp:
```bash
python3 hash_cracker.py -h
```

Tillgängliga flaggor:
- `--hash, -H`         Hashvärde att bearbeta (crack/identifiera)
- `--type, -t`         Hashtyp: MD5, SHA1, SHA256, SHA512, NTLM, bcrypt, argon2
- `--wordlist, -w`     Sökväg till ordlista (standard: rockyou.txt – ingår inte i repot)
- `--crack, -c`        Starta knäckning
- `--hash-password`    Hasha ett lösenord (ange klartext)
- `--identify`         Identifiera hashtyp via AI (kräver Ollama)

Observera:
- Cracking kräver både `--hash` och `--type`.
- Hasha kräver `--hash-password` och `--type`.
- Identifiera kräver `--identify` och `--hash`.

---

## Exempel

- Hasha ett lösenord med SHA256:
```bash
python3 hash_cracker.py --hash-password "hemligt" --type SHA256
```

- Hasha ett lösenord med bcrypt (saltas automatiskt och blir nytt värde vid varje körning):
```bash
python3 hash_cracker.py --hash-password "hemligt" --type bcrypt
```

- Knäcka en SHA1-hash med testlistan `passwords.txt`:
```bash
python3 hash_cracker.py --crack --hash "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8" --type SHA1 --wordlist passwords.txt
```

- Identifiera hashtyp via AI:
```bash
python3 hash_cracker.py --identify --hash "$2b$12$C2w1q4..."   # exempel på bcrypt
```

- Starta interaktivt läge:
```bash
python3 hash_cracker.py
```

---

## AI-baserad identifiering av hashtyp (Ollama)

Funktionen i menyn (val 7) samt flaggan `--identify` skickar en förfrågan till en lokal Ollama-instans:
- URL: `http://localhost:11434/api/generate`
- Modell: `gpt-oss:120b`
- Svar förväntas vara EN av: `MD5`, `SHA1`, `SHA256`, `SHA512`, `NTLM`, `bcrypt`, `argon2`

Kom igång med Ollama (exempel):
```bash
# Installera ollama enligt deras dokumentation
# Starta ollama-tjänsten, sedan:
ollama pull gpt-oss:120b
# Låt Ollama vara igång på port 11434 (standard)
```

Om Ollama inte är igång eller modellen saknas kommer verktyget att skriva ett tydligt felmeddelande och inte krascha.

---

## Felsökning och vanliga fel

- Ordlista hittas inte:
  - Kontrollera sökvägen. Ange full sökväg eller placera filen i samma katalog.
  - Kom ihåg att `rockyou.txt` inte ingår i repot; använd `passwords.txt` för test eller peka på din egen ordlista.
- Ingen anslutning till Ollama:
  - Säkerställ att Ollama körs lokalt och lyssnar på `http://localhost:11434`.
  - Kontrollera att modellen `gpt-oss:120b` finns tillgänglig.
- Inget resultat vid cracking:
  - Lösenordet finns inte i den använda ordlistan.
  - Testa en större/annan ordlista.
- Långsam körning:
  - Cracking sker sekventiellt i Python. Stora ordlistor tar tid.

---

## Noteringar och begränsningar

- Saltade hashar (som `bcrypt` och `argon2`) genereras med slumpmässigt salt. Det innebär:
  - Samma lösenord ger olika hashvärden vid olika körningar.
  - Verifiering måste göras med algoritmens verifieringsfunktion (vilket programmet gör) – en ren strängjämförelse av hashvärden räcker inte för saltade format.
- NTLM stöds via `passlib.hash.nthash`.
- Programmet använder ett enkelt, linjärt ordlistetest. Det är främst för utbildning, labb och mindre tester – inte optimerat för massiva ordlistor eller distribuering.

---

## Etik och ansvar

Detta verktyg är avsett för utbildningsändamål, återställning av egna lösenord och säkerhetstester där du har uttryckligt tillstånd. Användning mot system eller data som du inte äger eller har behörighet till kan vara olaglig. Du ansvarar själv för hur du använder programmet.