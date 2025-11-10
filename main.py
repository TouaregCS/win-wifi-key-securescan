import os
import subprocess
import sys
from colorama import Fore, Style, init

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from scripts import logger_setup, wifi_crypted, wifi_decrypted


logger = logger_setup.get_logger("main")

init(autoreset=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + " Wi-Fi Key SecureScan - CLI utility")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def menu():
    print(Fore.YELLOW + " 1 " + Fore.WHITE + " Vyhledej a ulož Wi-Fi klíče z tohoto počítače")
    print(Fore.YELLOW + " 2 " + Fore.WHITE + " Zobraz uložené Wi-Fi klíče")
    print(Fore.YELLOW + " 3 " + Fore.WHITE + " Exit")
    print(Fore.CYAN + "-" * 50 + Style.RESET_ALL)

def run_script(script_name):
    try:
      
      if script_name == 'wifi_crypted.py':
        wifi_crypted.main()
      elif script_name == 'wifi_decrypted.py':
        wifi_decrypted.main()
      else:
        print(Fore.RED + "Neznámý skript: " + script_name + Style.RESET_ALL)
    
    except Exception as e:
        logger.error(f"Chyba při spuštění skriptu {script_name}: {e}")
        print(Fore.RED + f"Chyba při spuštění skriptu {script_name}: {e}" + Style.RESET_ALL)
    
    finally:
        input(Fore.GREEN + "\n Stiskněte ENTER pro návrat do menu..." + Style.RESET_ALL)

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
            print(Fore.GREEN + "\n Ukončuji program. Nashledanou!\n" + Style.RESET_ALL)
            print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Neplatná volba. Zkuste to prosím znovu." + Style.RESET_ALL)
            input(Fore.GREEN + "\n Stiskněte ENTER pro pokračování..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()