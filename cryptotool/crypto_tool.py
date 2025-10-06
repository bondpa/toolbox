# Använder argparse för att hantera kommandoradsalternativ 
# och utför följande funktioner:
# 1. Krypterar en fil med en befintlig nyckel.
# 2. dekrypterar en krypterad fil och återställer originalet

import argparse
import sys
from cryptography.fernet import Fernet

def encrypt(file_path, key):
    print(f"Krypterar {file_path} med nyckeln {key}")

    with open(file_path, "rb") as f:
        file = f.read()

    with open(key, "rb") as k:
        key = k.read()
    
    fernet = Fernet(key)
    enc_file = fernet.encrypt(file)

    print(enc_file)

    enc_file_path = file_path + ".enc"

    with open(enc_file_path, "wb") as f:
        f.write(enc_file)

    print(f"Krypterad fil sparad som {enc_file_path}")
    

def decrypt(file_path, key):
    print(f"Dekrypterar {file_path} med nyckeln {key}")
    with open(file_path, "rb") as f:
        file = f.read()

    with open(key, "rb") as k:
        key = k.read()
    
    fernet = Fernet(key)
    dec_file = fernet.decrypt(file)

    print(dec_file)

    dec_file_path = file_path + ".dec"

    with open(dec_file_path, "wb") as f:
        f.write(dec_file)

    print(f"Dekrypterad fil sparad som {dec_file_path}")


def main():
    parser = argparse.ArgumentParser(description="Kryptera eller dekryptera fil")
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="Kryptera eller dekryptera filen")
    parser.add_argument("file", help="Sökväg till filen")
    parser.add_argument("key", default="secret.key", help="Sökväg till nyckeln")

    args = parser.parse_args()

    if args.action == "encrypt":
        encrypt(args.file, args.key)
    elif args.action == "decrypt":
        decrypt(args.file, args.key)


def main_menu():
    print("Huvudmeny")
    print("ska göras klart senare")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main_menu()
    else:
        main()