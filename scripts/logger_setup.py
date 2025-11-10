import logging
import os

# Nastaveni cesty k log souboru
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True) # Vytvori adresar, pokud neexistuje 
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Konfigurace logovani
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Vytvoření loggeru pro import
def get_logger(name):
    return logging.getLogger(name)