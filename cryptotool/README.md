# Crypto Tool

Ett enkelt Python-verktyg för att:
- generera en symmetrisk krypteringsnyckel (Fernet),
- kryptera en fil med en befintlig nyckel,
- dekryptera en tidigare krypterad fil och återskapa originalet.

Stödjer både:
- Interaktivt läge via textmenyer (för manuell användning)
- Kommandoradsflaggor (CLI) för snabb användning och skriptning

Verktyget använder Fernet (ur biblioteket `cryptography`) som erbjuder autenticerad kryptering (AES-128 i CBC med HMAC), vilket innebär att dekryptering misslyckas om fel nyckel används eller om filen har manipulerats.

---

## Innehåll
- Förutsättningar
- Installation
- Snabbstart
- Användning via textmeny (interaktiv)
- Användning via kommandoraden (CLI)
- Exempel
- Filnamn och utdata
- Säkerhet och begränsningar
- Felsökning

---

## Förutsättningar

- Python 3.8+ (rekommenderat 3.10+)
- Python-paket:
  - `cryptography`

Installera beroenden:
```bash
python3 -m pip install cryptography
```

---

## Installation

1) Placera `file_encryptor.py` i valfri katalog.
2) (Valfritt) Skapa en virtuell miljö:
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python3 -m pip install cryptography
```

---

## Snabbstart

- Generera en ny nyckel:
```bash
python3 file_encryptor.py --generate-key secret.key
```

- Kryptera en fil:
```bash
python3 file_encryptor.py --encrypt minfil.txt --key secret.key
```

- Dekryptera en fil:
```bash
python3 file_encryptor.py --decrypt minfil.txt.enc --key secret.key
```

- Starta interaktivt meny-läge:
```bash
python3 file_encryptor.py
```

---

## Användning via textmeny (interaktiv)

Starta utan argument:
```bash
python3 file_encryptor.py
```

Menyn visar aktuell fil och nyckel (standardnyckel: `secret.key`) och erbjuder:
1. Ange filsökväg
2. Ange nyckelsökväg
3. Generera ny nyckel (du kan välja filnamn; standard `secret.key`)
4. Kryptera fil
5. Dekryptera fil
0. Avsluta

Typiska flöden:
- Skapa och använd nyckel:
  1) Välj 3 för att generera ny nyckel (ange filnamn eller tryck Enter)
  2) Välj 1 för att ange fil
  3) Välj 4 för att kryptera
- Dekryptera en fil:
  1) Välj 2 för att peka på rätt nyckelfil
  2) Välj 1 för att ange den krypterade filen (t.ex. something.enc)
  3) Välj 5 för att dekryptera

---

## Användning via kommandoraden (CLI)

Visa hjälp:
```bash
python3 file_encryptor.py -h
```

Flaggor:
- `--generate-key <path>`  Generera en ny Fernet-nyckel och spara till filen `<path>`
- `--encrypt <file>`       Kryptera angiven fil
- `--decrypt <file>`       Dekryptera angiven fil
- `--key <path>`           Nyckelfil att använda (standard: `secret.key`)

Observera:
- Vid kryptering måste du ha en giltig nyckelfil (skapa med `--generate-key`).
- Vid dekryptering krävs samma nyckel som användes vid krypteringen.

---

## Exempel

- Generera en nyckel i standardfilen:
```bash
python3 file_encryptor.py --generate-key secret.key
```

- Kryptera en PDF:
```bash
python3 file_encryptor.py --encrypt rapport.pdf --key secret.key
# => Skapar rapport.pdf.enc
```

- Dekryptera tillbaka:
```bash
python3 file_encryptor.py --decrypt rapport.pdf.enc --key secret.key
# => Skapar rapport.pdf.enc.dec
```

- Använd annan nyckelfil:
```bash
python3 file_encryptor.py --generate-key nycklar/prod.key
python3 file_encryptor.py --encrypt data.bin --key nycklar/prod.key
```

---

## Filnamn och utdata

- Kryptering:
  - Läser: originalfil (t.ex. `fil.txt`)
  - Skriver: `fil.txt.enc` (binär krypterad fil)

- Dekryptering:
  - Läser: krypterad fil (t.ex. `fil.txt.enc`)
  - Skriver: `fil.txt.enc.dec` (binär dekrypterad fil, samma innehåll som originalet)

Notera:
- Under dekryptering skrivs det dekrypterade innehållet även ut i terminalen. Om filen är binär kan detta ge oläslig utskrift. Innehållet sparas oavsett till `.dec`-filen.

---

## Säkerhet och begränsningar

- Nyckelhantering:
  - Förvara nyckelfiler säkert och gör säkerhetskopior.
  - Dela aldrig nycklar i klartext och committa dem inte till versionshantering.
- Nyckelformat:
  - Endast Fernet-nycklar accepteras (URL-säker base64-kodad 32-byte). Generera alltid nycklar via verktyget.
- Integritet:
  - Fernet ger autenticerad kryptering. Fel nyckel eller manipulerad fil leder till dekrypteringsfel.
- Filstorlek och prestanda:
  - Verktyget läser hela filen i minnet. Mycket stora filer kan påverka minnesanvändning.

---

## Felsökning

- “Fel: Filen X hittades inte.”
  - Kontrollera sökvägen och filnamnet.
- “Fel: Nyckelfilen Y hittades inte.”
  - Ange korrekt sökväg eller generera en ny nyckel med `--generate-key`.
- “Fel vid kryptering (ogiltig nyckel?)”
  - Nyckeln är inte en giltig Fernet-nyckel. Skapa ny med `--generate-key`.
- “Fel vid dekryptering (fel nyckel eller korrupt fil?)”
  - Säkerställ att du använder samma nyckel som vid kryptering och att filen inte skadats.
- “Terminalen fylls med konstiga tecken vid dekryptering”
  - Det är normalt för binära filer. Använd `.dec`-filen som sparas på disk; ignorera terminalutskriften.

---