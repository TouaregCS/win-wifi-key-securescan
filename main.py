import os
import subprocess
from colorama import Fore, Style, init
from scripts.logger_setup import get_logger

logger = get_logger("main")

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " Wi-Fi Key SecureScan - CLI utility")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def menu():
    print(Fore.YELLOW + "1" + Fore.WHITE + " Vyhledej a ulož Wi-Fi klíče z tohoto počítače")
    print(Fore.YELLOW + "2" + Fore.WHITE + " Zobraz uložené Wi-Fi klíče")
    print(Fore.YELLOW + "3" + Fore.WHITE + " Ukonči program")
    print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)

def run_script(script_name):
    try:
        logger.info(f"Spouštím skript: {script_name}")
        subprocess.run(
            ['python', f"scripts/{script_name}"],
            check=True,
            text=True,
            stdin=None,
            stdout=None,
            stderr=None
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Chyba při spouštění {script_name}: {e}")
        print(Fore.RED + f"Chyba při spouštění {script_name}: {e}" + Style.RESET_ALL)
    input(Fore.GREEN + "\n Stiskněte ENTER pro návrat do menu ..." + Style.RESET_ALL)

def main():
    while True:
        clear_screen()
        banner()
        menu()
        choice = input(Fore.GREEN + "\n Vyberte možnost (1-3): " + Style.RESET_ALL)

        if choice == '1':
            run_script('wifi_crypted.py')
        elif choice == '2':
            run_script('wifi_decrypted.py')
        elif choice == '3':
            print(Fore.GREEN + "\n Ukončuji program. Nashledanou!" + Style.RESET_ALL)
            print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
            logger.info("Program ukončen uživatelem.")
            break
        else:
            print(Fore.RED + "Neplatná volba. Zkuste to prosím znovu." + Style.RESET_ALL)
            input(Fore.GREEN + "\n Stiskněte Enter pro pokračování..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()