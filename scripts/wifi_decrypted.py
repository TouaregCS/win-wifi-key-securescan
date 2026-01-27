#!/usr/bin/env python3
# wifi_decrypt.py
# Dešifruje soubor vytvořený wifi_encrypt.py (formát: MAGIC + salt + fernet_token).
# Použití:
#   python wifi_decrypt.py               # použije výchozí wifi_passwords.txt.encrypted a vypíše plaintext
#   python wifi_decrypt.py -f file.enc   # nebo --file cesta_k_souboru
#   python wifi_decrypt.py -f file.enc -o out.txt  # uloží dešifrovaný obsah do souboru

import argparse
import sys
import os
import getpass

from base64 import urlsafe_b64encode
from scripts.logger_setup import get_logger
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken

logger = get_logger("wifi_decrypted")

MAGIC = b'WIFI'
SALT_SIZE = 16
KDF_ITERS = 390000

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERS,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return urlsafe_b64encode(key)

def decrypt_blob(blob: bytes, password: str) -> bytes:
    if not blob.startswith(MAGIC):
        raise ValueError("Neznámý formát souboru (MAGIC mismatch).")
    salt = blob[len(MAGIC):len(MAGIC)+SALT_SIZE]
    token = blob[len(MAGIC)+SALT_SIZE:]
    key = derive_key(password.encode('utf-8'), salt)
    f = Fernet(key)
    try:
        logger.info("Začínám dešifrování souboru.")
        return f.decrypt(token)
    except InvalidToken:
        logger.error("Neplatné heslo nebo poškozený soubor (dešifrování selhalo).")
        raise InvalidToken("Neplatné heslo nebo poškozený soubor (dešifrování selhalo).")

def main():
    parser = argparse.ArgumentParser(description="Dešifruje Wi-Fi export vytvořený wifi_encrypt.py")
    parser.add_argument('-f','--file', default='wifi_passwords.txt.encrypted', help='Šifrovaný vstupní soubor')
    parser.add_argument('-o','--out', help='Volitelně: uložit dešifrovaný výstup do souboru')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Soubor nenalezen: {args.file}", file=sys.stderr)
        sys.exit(2)

    pwd = getpass.getpass("Zadej heslo pro dešifrování: ")
    with open(args.file, 'rb') as f:
        blob = f.read()

    try:
        logger.info(f"Začínám dešifrování souboru: {args.file}")
        plain = decrypt_blob(blob, pwd)
    except Exception as e:
        logger.error(f"Chyba při dešifrování souboru {args.file}: {e}")
        print("Chyba při dešifrování:", e, file=sys.stderr)
        sys.exit(3)
    input("Stiskni Enter pro ukončení...")


    # Plaintext je bajtový obsah (utf-8). Pokusíme se dekódovat pro čitelné zobrazení.
    try:
        text = plain.decode('utf-8')
    except Exception:
        # fallback: binární data -> uložit pokud -o, nebo vypíše surově do stdout.buffer
        if args.out:
            with open(args.out, 'wb') as f:
                f.write(plain)
            print(f"Dešifrováno a uloženo do {args.out}")
            
        else:
            # zapíšeme do stdout binárně
            sys.stdout.buffer.write(plain)
            return

    # Pokud uživatel zadal -o, uložíme do souboru, jinak vypíšeme na stdout
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Dešifrováno a uloženo do {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()
