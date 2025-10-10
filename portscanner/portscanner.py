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

nm = nmap.PortScanner()

def scan_hosts(host, ports):
    result = nm.scan(hosts=host, ports=ports)
    return result

def save_to_file(result, filename):
    with open(filename, 'w') as file:
        json.dump(result, file)

def save_to_textfile(string_to_save, filename):
    with open(filename, 'w') as file:
        file.write(string_to_save)

def load_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def main_menu(host, ports):
    while True:
        print("\nMeny:")
        if host:
            print(f"Vald värd: {host}")
        if ports:
            print(f"Valda portar: {ports}")
        print("1. Ange värd manuellt")
        print("2. Ange port(ar) manuellt")
        print("3. Ladda värd och portar från JSON-fil")
        print("4. Starta skanning")
        print("5. Spara resultat till JSON-fil")
        print("6. Spara resultat till textfil")
        print("7. Avsluta")

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
        elif choice == '7':
            print("Avslutar...")
            break
        else:
            print("Ogiltigt val. Försök igen.")

def main():
    parser = argparse.ArgumentParser(description="Skanna portar på en värd")
    parser.add_argument("--host", "-H", help="Värd att skanna (t.ex. example.com)")
    parser.add_argument("--ports", "-p", help="Port(ar) att skanna (t.ex. 80 eller 20-80)")
    args = parser.parse_args()

    if not args.host or not args.ports:
        print("Fel: Både --host och --ports måste anges")
        parser.print_help()
        return
    
    print(f"Skannar {args.host} på port(ar) {args.ports}")
    result = scan_hosts(args.host, args.ports)
    
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


if __name__ == "__main__":
    host = ""
    ports = ""
    result = None
    if len(sys.argv) == 1:
        main_menu(host, ports)
    else:
        main()