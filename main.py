import cryptotool.crypto_tool as ct
import portscanner.portscanner as ps

def menu():
    while True:
        print("\n===== IT-säkerhetsverktyg =====")
        print("1. Portscanner")
        print("2. Krypteringsverktyg")
        print("3. Subdomain Enumeration")
        print("0. Avsluta")
        choice = input("Välj ett verktyg (0-3): ")

        if choice == "1":
            print("portscanner")
            ps.main("", "")
            
        elif choice == "2":
            print("krypteringsverktyg")
            ct.main_menu()
            
        elif choice == "3":
            print("subdomain enumeration")
            input()
            
        elif choice == "0":
            print("Avslutar programmet. Hej då!")
            break
        else:
            print("Felaktigt val, försök igen.")

if __name__ == "__main__":
    menu()