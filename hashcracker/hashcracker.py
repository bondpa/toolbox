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
            print("Välj hashtyp")
        elif choice == "2":
            print("Ange hashvärde")
        elif choice == "3":
            print("Välj ordlista")
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