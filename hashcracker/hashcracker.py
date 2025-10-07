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
        elif choice == "0":
            print("Avslutar Hash Cracker.")
            break
        else:
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    main()