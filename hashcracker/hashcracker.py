import hashlib
from urllib import response
from passlib.hash import nthash
import bcrypt
from argon2 import PasswordHasher
import requests


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
    raise NotImplementedError("Verification not implemented for this hash type.")


def crack_with_wordlist(hash_value, selected_hash, wordlist):
    with open(wordlist, 'r') as f:
        for password in f:
            password = password.strip()
            if verify_password(password, hash_value, selected_hash):
                return password  # Hittat!
    return None  # Inte hittat

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
        
    except Exception as e:
        print("Status kod:", response.status_code)
        print("Helt svar:")
        print(response.json())
        print(f"Kunde inte identifiera hashtyp: {e}")
        return None


def main():
    # visar meny där vald typ av hash samt angivet hashvärde visas
    selected_hash = False
    hash_value = False
    wordlist = "rockyou.txt"  

    while True:
        print("\n===== Hash Cracker =====")
        print("Hashtyp", selected_hash if selected_hash else "Du måste ange hashtyp")
        print("Hashvärde: ", hash_value if hash_value else "Du måste ange hashvärde")
        print("Ordlista: ", wordlist)
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
                print("Ogiltigt val, försök igen.")
                continue
        elif choice == "2":
            hash_value = input("Ange hashvärde: ").strip()
            if not hash_value:
                print("Hashvärde kan inte vara tomt.")
                hash_value = False
                continue
        elif choice == "3":
            wl_choice = input("Ange sökväg till ordlista (standard: rockyou.txt): ").strip()
            if wl_choice:
                wordlist = wl_choice
            else:
                wordlist = "rockyou.txt"
            print(f"Ordlista satt till: {wordlist}")
        elif choice == "4":
            if not selected_hash or not hash_value:
                print("Du måste ange både hashtyp och hashvärde innan du kan starta knäckning.")
                continue
            print(f"Startar knäckning av {selected_hash} hash: {hash_value} med ordlista {wordlist}")
            crack_result =  crack_with_wordlist(hash_value, selected_hash, wordlist)
            if crack_result:
                print(f"Lösenord hittat: {crack_result}")
            else:
                print("Lösenord hittades inte i ordlistan.")
        elif choice == "5":
            if not selected_hash:
                print("Hashtyp kan inte vara tomt.")
                continue
            pwd = input("Ange lösenord att hasha: ").strip()
            if not pwd:
                print("Lösenord kan inte vara tomt.")
                continue
            hashed_pwd = hash_password(pwd, selected_hash)
            print(f"{selected_hash}-hash av '{pwd}' är: {hashed_pwd}")
            use_hash = input("\nVill du använda denna hash som aktuellt hashvärde? (j/n): ").strip().lower()
            if use_hash == 'j' or use_hash == 'ja':
                hash_value = hashed_pwd
                print(f"Hashvärde uppdaterat till: {hash_value}")
        elif choice == "6":
            if not selected_hash or not hash_value:
                print("Du måste ange både hashtyp och hashvärde innan verifiering.")
                continue
            pwd = input("Ange lösenord att verifiera: ").strip()
            if not pwd:
                print("Lösenord kan inte vara tomt.")
                continue
            print("Lösenordet matchar hashvärdet!" if verify_password(pwd, hash_value, selected_hash) else "Lösenordet matchar INTE hashvärdet.")
        elif choice == "7":
            if not hash_value:
                print("Du måste ange ett hashvärde innan du kan testa.")
                continue
            print(check_hash_type(hash_value))
        elif choice == "0":
            print("Avslutar Hash Cracker.")
            break
        else:
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    main()