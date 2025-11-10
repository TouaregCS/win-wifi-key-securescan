import os
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " Wi-Fi Key SecureScan - CLI utility")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def menu():
    print(Fore.YELLOW + "1" + Fore.WHITE + "Vyhledej a ulož Wi-Fi klíče z tohoto počítače")
    print(Fore.YELLOW + "2" + Fore.WHITE + "Zobraz uložené Wi-Fi klíče")
    print(Fore.YELLOW + "3" + Fore.WHITE + "Exit")
    print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Chyba při spouštění {script_name}: {e}" + Style.RESET_ALL)
    input(Fore.BLUE + "\n Stiskněte Enter pro návrat do menu..." + Style.RESET_ALL)

def main():
    while True:
        clear_screen()
        banner()
        menu()
        choice = input(Fore.GREEN + "\n Vyberte možnost (1-3): " + Style.RESET_ALL)

        if choice == '1':
            run_script('scripts\wifi_crypted.py')
        elif choice == '2':
            run_script('scripts\wifi_decrypted.py')
        elif choice == '3':
            print(Fore.GREEN + "\n Ukončuji program. Nashledanou!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Neplatná volba. Zkuste to prosím znovu." + Style.RESET_ALL)
            input(Fore.BLUE + "\n Stiskněte Enter pro pokračování..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()