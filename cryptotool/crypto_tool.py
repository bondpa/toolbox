# Använder argparse för att hantera kommandoradsalternativ 
# och utför följande funktioner:
# 1. Krypterar en fil med en befintlig nyckel.
# 2. dekrypterar en krypterad fil och återställer originalet

import argparse
import sys
from cryptography.fernet import Fernet

# Färgkoder för terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def encrypt(file_path, key):
    print(f"Krypterar {file_path} med nyckeln {key}")

    try:
        with open(file_path, "rb") as f:
            file = f.read()
    except FileNotFoundError:
        print(f"Fel: Filen {file_path} hittades inte.")
        return
    except Exception as e:
        print(f"Fel vid läsning av fil: {e}")
        return

    try:
        with open(key, "rb") as k:
            key_data = k.read()
    except FileNotFoundError:
        print(f"Fel: Nyckelfilen {key} hittades inte.")
        return
    except Exception as e:
        print(f"Fel vid läsning av nyckel: {e}")
        return
    
    try:
        fernet = Fernet(key_data)
        enc_file = fernet.encrypt(file)
    except Exception as e:
        print(f"Fel vid kryptering (ogiltig nyckel?): {e}")
        return

    enc_file_path = file_path + ".enc"

    try:
        with open(enc_file_path, "wb") as f:
            f.write(enc_file)
        print(f"Krypterad fil sparad som {enc_file_path}")
    except Exception as e:
        print(f"Fel vid sparande av krypterad fil: {e}")
    

def decrypt(file_path, key):
    print(f"Dekrypterar {file_path} med nyckeln {key}")

    try:
        with open(file_path, "rb") as f:
            file = f.read()
    except FileNotFoundError:
        print(f"Fel: Filen {file_path} hittades inte.")
        return
    except Exception as e:
        print(f"Fel vid läsning av fil: {e}")
        return

    try:
        with open(key, "rb") as k:
            key_data = k.read()
    except FileNotFoundError:
        print(f"Fel: Nyckelfilen {key} hittades inte.")
        return
    except Exception as e:
        print(f"Fel vid läsning av nyckel: {e}")
        return
    
    try:
        fernet = Fernet(key_data)
        dec_file = fernet.decrypt(file)
    except Exception as e:
        print(f"Fel vid dekryptering (fel nyckel eller korrupt fil?): {e}")
        return
    
    print(dec_file)

    dec_file_path = file_path + ".dec"

    try:
        with open(dec_file_path, "wb") as f:
            f.write(dec_file)
        print(f"Dekrypterad fil sparad som {dec_file_path}")
    except Exception as e:
        print(f"Fel vid sparande av dekrypterad fil: {e}")


def generate_key(key_path):
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)


def main():
    parser = argparse.ArgumentParser(description="Kryptera eller dekryptera fil")
    parser.add_argument("--encrypt", help="Fil att kryptera")
    parser.add_argument("--decrypt", help="Fil att dekryptera")
    parser.add_argument("--key", default="secret.key", help="Nyckel att använda (standard: secret.key)")
    parser.add_argument("--generate-key", help="Generera ny nyckel och spara till fil")

    args = parser.parse_args()

    if args.generate_key:
        generate_key(args.generate_key)
        print(f"Nyckel genererad och sparad i {args.generate_key}")
    elif args.encrypt:
        encrypt(args.encrypt, args.key)
    elif args.decrypt:
        decrypt(args.decrypt, args.key)
    else:
        print("Fel: Du måste ange antingen --encrypt, --decrypt eller --generate-key")
        parser.print_help()

def main_menu():
    file_path = ""
    key_path = "secret.key"

    print("Huvudmeny")
    while True:
        print("\n=== Krypterings/Dekrypteringsverktyg ===")
        if file_path:
            print(f"{GREEN}✓ Vald fil: {file_path}{RESET}")
        else:
            print(f"{RED}✗ Ingen fil vald{RESET}")
            
        if key_path:
            print(f"{GREEN}✓ Vald nyckel: {key_path}{RESET}")
        else:
            print(f"{RED}✗ Ingen nyckel vald{RESET}")
        print("\n1. Ange filsökväg")
        print("2. Ange nyckelsökväg")
        print("3. Generera ny nyckel")
        print("4. Kryptera fil")
        print("5. Dekryptera fil")
        print("0. Avsluta")
        
        choice = input("\nVälj alternativ: ")
        if choice == '1':
            file_path = input("Ange fil att kryptera/dekryptera: ")
        elif choice == '2':
            key_path = input("Ange nyckelfil: ")
        elif choice == '3':
            key_path = input("Filnamn för nyckelfil (enter för 'secret.key'): ") or "secret.key"
            generate_key(key_path)
        elif choice == '4':
            if file_path and key_path:
                encrypt(file_path, key_path)
            else:
                print("Ange nyckel samt fil före kryptering.")
        elif choice == '5':
            if file_path and key_path:
                decrypt(file_path, key_path)
            else:
                print("Ange nyckel samt fil före dekryptering.")
        elif choice == '0':
            print("Avslutar...")
            break
        else:
            print("Ogiltigt val. Försök igen.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main_menu()
    else:
        main()