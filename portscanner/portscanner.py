"""
Example JSON input file:

{
    "host": "bondpa.se",
    "ports": "22, 80, 443"
}
"""
import nmap
import json
import argparse 
import sys

# Färgkoder för terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

nm = nmap.PortScanner()

def scan_hosts(host, ports):
    try:
        result = nm.scan(hosts=host, ports=ports)
        return result
    except Exception as e:
        print(f"Fel vid skanning: {e}")
        return None

def save_to_file(result, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(result, file)
        print(f"Resultatet sparades i {filename}")
    except Exception as e:
        print(f"Ett fel uppstod då filen skulle sparas: {e}")

def save_to_textfile(string_to_save, filename):
    with open(filename, 'w') as file:
        file.write(string_to_save)

def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Fel: Filen {filename} hittades inte.")
        return None
    except json.JSONDecodeError:
        print(f"Fel: Filen {filename} är inte en giltig JSON-fil.")
        return None
    except Exception as e:
        print(f"Fel vid läsning av fil: {e}")
        return None

def main_menu(host, ports):
    while True:
        print("\n=== Portscanner ===")
        if host:
            print(f"{GREEN}✓ Vald värd: {host}{RESET}")
        else:
            print(f"{RED}✗ Ingen värd vald{RESET}")
        if ports:
            print(f"{GREEN}✓ Valda portar: {ports}{RESET}")
        else:
            print(f"{RED}✗ Inga portar valda{RESET}")
        print("1. Ange värd manuellt")
        print("2. Ange port(ar) manuellt")
        print("3. Ladda värd och portar från JSON-fil")
        print("4. Starta skanning")
        print("5. Spara resultat till JSON-fil")
        print("6. Spara resultat till textfil")
        print("0. Avsluta")

        choice = input("Välj alternativ: ")

        if choice == '1':
            host = input("Ange värd att skanna: ")
        elif choice == '2':
            ports = input("Ange en eller flera portar eller ett intervall, t.ex. 80 eller 20-80: ")
        elif choice == '3':
            filename = input("Ange JSON-fil med indata: ")
            data = load_from_file(filename)
            host = data.get('host', '')
            ports = data.get('ports', '')
            print(f"Laddade värd: {host}")
            print(f"Laddade portar: {ports}")
        elif choice == '4':
            if host and ports:
                print(f"Startar skanning på värd: {host} av port(ar): {ports}")
                result = scan_hosts(host, ports)
                print("Resultat:") 
                for host in nm.all_hosts():
                    print('Värd : %s (%s)' % (host, nm[host].hostname()))
                    print('State : %s' % nm[host].state())
                    for proto in nm[host].all_protocols():
                        print('Protocol : %s' % proto)
                        lport = nm[host][proto].keys()
                        for port in lport:
                            print ('port: %s\tstatus: %s\tnamn: %s\tprodukt: %s\tversion: %s' % (port, nm[host][proto][port]['state'], nm[host][proto][port]['name'], nm[host][proto][port]['product'], nm[host][proto][port]['version']))
            else:
                print("Värd och portar måste anges före skanning.")
        elif choice == '5':
            if result:
                filename = input("Ange JSON-fil för att spara resultatet: ")
                save_to_file(result, filename)
                print(f"Resultatet sparades i {filename}")
            else:
                print("Inget resultat att spara. Kör en skanning först.")
        elif choice == '6':
            if result:
                filename = input("Ange textfil för att spara resultatet: ")
                string_to_save = "Resultat:\n"
                for host in nm.all_hosts():
                    string_to_save += 'Värd : %s (%s)\n' % (host, nm[host].hostname())
                    string_to_save += 'State : %s\n' % nm[host].state()
                    for proto in nm[host].all_protocols():
                        string_to_save += 'Protocol : %s\n' % proto
                        lport = nm[host][proto].keys()
                        for port in lport:
                            string_to_save += 'port: %s\tstatus: %s\tnamn: %s\tprodukt: %s\tversion: %s\n' % (port, nm[host][proto][port]['state'], nm[host][proto][port]['name'], nm[host][proto][port]['product'], nm[host][proto][port]['version'])
                save_to_textfile(string_to_save, filename)
                print(f"Resultatet sparades i {filename}")
            else:
                print("Inget resultat att spara. Kör en skanning först.")
        elif choice == '0':
            print("Avslutar...")
            break
        else:
            print("Ogiltigt val. Försök igen.")

def main():
    parser = argparse.ArgumentParser(description="Skanna portar på en värd")
    parser.add_argument("--host", "-H", help="Värd att skanna (t.ex. example.com)")
    parser.add_argument("--ports", "-p", help="Port(ar) att skanna (t.ex. 80 eller 20-80)")
    parser.add_argument("--input", "-i", help="Ladda värd och portar från JSON-fil")
    parser.add_argument("--output", "-o", help="Spara resultat till JSON-fil")
    parser.add_argument("--output-text", "-t", help="Spara resultat till textfil")
    args = parser.parse_args()

    host = ""
    ports = ""

    if args.input:
        data = load_from_file(args.input)
        if data:
            host = data.get('host', '')
            ports = data.get('ports', '')
            print(f"Laddade från {args.input}: värd={host}, portar={ports}")

    if not host and args.host:
        host = args.host
    if not ports and args.ports:
        ports = args.ports

    if not host or not ports:
        print("Fel: Både --host och --ports måste anges (eller --input med båda värdena)")
        parser.print_help()
        return
    
    print(f"Skannar {host} på port(ar) {ports}")
    result = scan_hosts(host, ports)
    
    if result:
        print("Resultat:")
        for host in nm.all_hosts():
            print('Värd : %s (%s)' % (host, nm[host].hostname()))
            print('State : %s' % nm[host].state())
            for proto in nm[host].all_protocols():
                print('Protocol : %s' % proto)
                lport = nm[host][proto].keys()
                for port in lport:
                    print ('port: %s\tstatus: %s\tnamn: %s\tprodukt: %s\tversion: %s' % (port, nm[host][proto][port]['state'], nm[host][proto][port]['name'], nm[host][proto][port]['product'], nm[host][proto][port]['version']))

        if args.output:
            save_to_file(result, args.output)

        if args.output_text:
            string_to_save = "Resultat:\n"
            for h in nm.all_hosts():
                string_to_save += 'Värd : %s (%s)\n' % (h, nm[h].hostname())
                string_to_save += 'State : %s\n' % nm[h].state()
                for proto in nm[h].all_protocols():
                    string_to_save += 'Protocol : %s\n' % proto
                    lport = nm[h][proto].keys()
                    for port in lport:
                        string_to_save += 'port: %s\tstatus: %s\tnamn: %s\tprodukt: %s\tversion: %s\n' % (port, nm[h][proto][port]['state'], nm[h][proto][port]['name'], nm[h][proto][port]['product'], nm[h][proto][port]['version'])
            save_to_textfile(string_to_save, args.output_text)
            print(f"Resultatet sparades i {args.output_text}")

if __name__ == "__main__":
    host = ""
    ports = ""
    result = None
    if len(sys.argv) == 1:
        main_menu(host, ports)
    else:
        main()