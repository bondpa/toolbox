# skript som genererar en symmetrisk nyckel och sparar den i en fil

from cryptography.fernet import Fernet

def main():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Nyckel genererad och sparad i secret.key")

if __name__ == "__main__":
    main()