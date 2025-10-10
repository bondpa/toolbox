import hashlib
from urllib import response
from passlib.hash import nthash
import bcrypt
from argon2 import PasswordHasher
import requests
import argparse
import sys

# Färgkoder för terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def hash_password(password, hash_type="MD5"):
    if hash_type == "MD5":
        return hashlib.md5(password.encode()).hexdigest()
    elif hash_type == "SHA1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif hash_type == "SHA256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif hash_type == "SHA512":
        return hashlib.sha512(password.encode()).hexdigest()
    elif hash_type == "NTLM": 
        return nthash.hash(password)
    elif hash_type == "bcrypt": # https://www.geeksforgeeks.org/python/hashing-passwords-in-python-with-bcrypt/
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash.decode('utf-8')
    elif hash_type == "argon2": # https://stackoverflow.com/questions/58431973/argon2-library-that-hashes-passwords-without-a-secret-and-with-a-random-salt-tha
        ph = PasswordHasher()
        return ph.hash(password)

    return None  

def verify_password(password, hash_value, hash_type):
    try:
        if hash_type == "MD5" or hash_type == "SHA1" or hash_type == "SHA256" or hash_type == "SHA512" or hash_type == "NTLM":
            return hash_password(password, hash_type) == hash_value
        elif hash_type == "bcrypt":
            return bcrypt.checkpw(password.encode('utf-8'), hash_value.encode('utf-8'))
        elif hash_type == "argon2":
            ph = PasswordHasher()
            try:
                ph.verify(hash_value, password)
                return True
            except:
                return False
    except Exception as e:
        # Tyst felhantering - returnera bara False vid ogiltigt format
        return False

def crack_with_wordlist(hash_value, selected_hash, wordlist):
    try:
        with open(wordlist, 'r') as f:
            for password in f:
                password = password.strip()
                if verify_password(password, hash_value, selected_hash):
                    return password # Hittat!
        return None # Inte hittat
    except FileNotFoundError:
        print(f"{RED}Fel: Ordlistan {wordlist} hittades inte.{RESET}")
        return None
    except Exception as e:
        print(f"{RED}Fel vid läsning av ordlista: {e}{RESET}")
        return None

def check_hash_type(hash_value):
    if not hash_value:
        raise ValueError("Hashvärde kan inte vara tomt.")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gpt-oss:120b",
                "prompt": f"Identify this hash type. Return ONLY one word: MD5, SHA1, SHA256, SHA512, NTLM, bcrypt, or argon2\n\nHash: {hash_value}",
                "stream": False
            },
            timeout=30
        )
        return response.json()["response"].strip()
        
    except requests.exceptions.ConnectionError:
        print(f"{RED}Fel: Kunde inte ansluta till Ollama. Kontrollera att den körs på port 11434.{RESET}")
        return None
    except Exception as e:
        print(f"{RED}Fel vid hashidentifiering: {e}{RESET}")
        return None


def main_menu():
    # visar meny där vald typ av hash samt angivet hashvärde visas
    selected_hash = False
    hash_value = False
    wordlist = "rockyou.txt"  

    while True:
        print(f"\n{BLUE}===== Hash Cracker ====={RESET}")

        if selected_hash:
            print(f"{GREEN}✓ Hashtyp: {selected_hash}{RESET}")
        else:
            print(f"{RED}✗ Ingen hashtyp vald{RESET}")
        if hash_value:
            print(f"{GREEN}✓ Hashvärde: {hash_value}{RESET}")
        else:
            print(f"{RED}✗ Inget hashvärde angivet{RESET}")
        if wordlist:
            print(f"{GREEN}✓ Ordlista: {wordlist}{RESET}")
        else:
            print(f"{RED}✗ Ingen ordlista vald{RESET}")
        print("1. Ange hashtyp (t.ex. MD5, SHA1, SHA256)")
        print("2. Ange hashvärde")
        print("3. Välj ordlista")
        print("4. Starta knäckning")
        print("5. Hasha ett lösenord")
        print("6. Verifiera ett lösenord mot angivet hashvärde")
        print("7. Testa att identifiera hashtyp från hashvärde. Denna funktion kräver att en lokal instans av GPT-OSS körs på port 11434")
        print("0. Avsluta")
        choice = input("Välj ett alternativ: ")

        if choice == "1":
            print("\nVälj hash-typ:")
            print("1. MD5")
            print("2. SHA1")
            print("3. SHA256")
            print("4. SHA512")
            print("5. NTLM")
            print("6. bcrypt")
            print("7. argon2")

            ht_choice = input("\nVälj hashtyp (1-7): ").strip()

            if ht_choice == "1":
                selected_hash = "MD5"
            elif ht_choice == "2":
                selected_hash = "SHA1"
            elif ht_choice == "3":
                selected_hash = "SHA256"
            elif ht_choice == "4":
                selected_hash = "SHA512"
            elif ht_choice == "5":
                selected_hash = "NTLM"
            elif ht_choice == "6":
                selected_hash = "bcrypt"
            elif ht_choice == "7":
                selected_hash = "argon2"
            else:
                print(f"{RED}Ogiltigt val, försök igen.{RESET}")
                continue
        elif choice == "2":
            hash_value = input("Ange hashvärde: ").strip()
            if not hash_value:
                print(f"{RED}Hashvärde kan inte vara tomt.{RESET}")
                hash_value = False
                continue
        elif choice == "3":
            wl_choice = input("Ange sökväg till ordlista (standard: rockyou.txt): ").strip()
            if wl_choice:
                wordlist = wl_choice
            else:
                wordlist = "rockyou.txt"
            print(f"{GREEN}✓ Ordlista satt till: {wordlist}{RESET}")
        elif choice == "4":
            if not selected_hash or not hash_value:
                print(f"{YELLOW}⚠ Du måste ange både hashtyp och hashvärde innan du kan starta knäckning.{RESET}")
                continue
            print(f"Startar knäckning av {selected_hash} hash: {hash_value} med ordlista {wordlist}")
            crack_result =  crack_with_wordlist(hash_value, selected_hash, wordlist)
            if crack_result:
                print(f"{GREEN}✓ Lösenord hittat: {crack_result}{RESET}")
            else:
                print(f"{YELLOW}⚠ Lösenord hittades inte i ordlistan.{RESET}")
        elif choice == "5":
            if not selected_hash:
                print(f"{RED}Hashtyp kan inte vara tomt.{RESET}")
                continue
            pwd = input("Ange lösenord att hasha: ").strip()
            if not pwd:
                print(f"{RED}Lösenord kan inte vara tomt.{RESET}")
                continue
            hashed_pwd = hash_password(pwd, selected_hash)
            print(f"{GREEN}{selected_hash}-hash av '{pwd}' är: {hashed_pwd}{RESET}")
            use_hash = input("\nVill du använda denna hash som aktuellt hashvärde? (j/n): ").strip().lower()
            if use_hash == 'j' or use_hash == 'ja':
                hash_value = hashed_pwd
                print(f"{GREEN}✓ Hashvärde uppdaterat till: {hash_value}{RESET}")
        elif choice == "6":
            if not selected_hash or not hash_value:
                print(f"{YELLOW}⚠ Du måste ange både hashtyp och hashvärde innan verifiering.{RESET}")
                continue
            pwd = input("Ange lösenord att verifiera: ").strip()
            if not pwd:
                print(f"{RED}Lösenord kan inte vara tomt.{RESET}")
                continue
            print(f"{GREEN}✓ Lösenordet matchar hashvärdet!{RESET}" if verify_password(pwd, hash_value, selected_hash) else "Lösenordet matchar INTE hashvärdet.")
        elif choice == "7":
            if not hash_value:
                print(f"{YELLOW}⚠ Du måste ange ett hashvärde innan du kan testa.{RESET}")
                continue
            identified = check_hash_type(hash_value)
            if identified:
                print(f"{GREEN}✓ Identifierad hashtyp: {identified}{RESET}")
            else:
                print(f"{YELLOW}⚠ Kunde inte identifiera hashtypen.{RESET}")
        elif choice == "0":
            print("Avslutar Hash Cracker.")
            break
        else:
            print("Ogiltigt val, försök igen.")

def main():
    parser = argparse.ArgumentParser(description="Knäck hashade lösenord")
    parser.add_argument("--hash", "-H", help="Hashvärde att cracka")
    parser.add_argument("--type", "-t", help="Hashtyp (MD5, SHA1, SHA256, SHA512, NTLM, bcrypt, argon2)")
    parser.add_argument("--wordlist", "-w", default="rockyou.txt", help="Ordlista (standard: rockyou.txt)")
    parser.add_argument("--crack", "-c", action="store_true", help="Starta knäckning")
    parser.add_argument("--hash-password", help="Hasha ett lösenord")
    parser.add_argument("--identify", action="store_true", help="Identifiera hashtyp med AI (kräver Ollama)")
    
    args = parser.parse_args()

    if args.identify:
        if not args.hash:
            print("Fel: --hash måste anges för att identifiera hashtyp")
            parser.print_help()
            return
    
        print(f"Identifierar hashtyp för: {args.hash}")
        identified_type = check_hash_type(args.hash)
    
        if identified_type:
            print(f"Identifierad hashtyp: {identified_type}")
        else:
            print("Kunde inte identifiera hashtypen")
        return

    if args.hash_password:
        if not args.type:
            print("Fel: --type måste anges för att hasha ett lösenord")
            parser.print_help()
            return
    
        hashed = hash_password(args.hash_password, args.type)
        print(f"\n{args.type}-hash av '{args.hash_password}':")
        print(hashed)
        return

    if args.crack:
        if not args.hash or not args.type:
            print("Fel: --hash och --type måste anges för att starta knäckning")
            parser.print_help()
            return
        
        print(f"Startar knäckning av {args.type} hash: {args.hash}")
        print(f"Använder ordlista: {args.wordlist}")
    
        result = crack_with_wordlist(args.hash, args.type, args.wordlist)
    
        if result:
            print(f"\n✓ Lösenord hittat: {result}")
        else:
            print("\n✗ Lösenord hittades inte i ordlistan.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main_menu()
    else:
        main()