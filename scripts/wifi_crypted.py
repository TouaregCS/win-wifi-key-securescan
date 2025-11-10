#!/usr/bin/env python3
# wifi_encrypt.py
# Windows: extrahuje SSID a hesla, zašifruje výstup a uloží do souboru.
# Používejte v PowerShell/CMD spuštěném jako administrátor, pokud chcete číst hesla.

import subprocess, re, sys, os, argparse, getpass
from base64 import urlsafe_b64encode
from .logger_setup import get_logger
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

logger = get_logger("wifi_crypted")

MAGIC = b'WIFI'   # identifikátor formátu
SALT_SIZE = 16
KDF_ITERS = 390000     # dostatečně vysoké, ale nezpomalí přespříliš

def run_netsh(cmd):
    full_cmd = 'netsh ' + cmd
    try:
        raw = subprocess.check_output(full_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Chyba při spuštění: {full_cmd}\nKód: {e.returncode}")
        raise RuntimeError(f"Chyba při spuštění: {full_cmd}\nKód: {e.returncode}") from e

    for enc in ("cp1250","cp850","cp852","cp866","cp1252","utf-8"):
        try:
            logger.info(f"Trying to decode with encoding: {enc}")
            return raw.decode(enc)
        except Exception as e:
            logger.warning(f"Decoding with encoding {enc} failed: {e}")
            continue
    return raw.decode("utf-8", errors="replace")

def list_profiles():
    out = run_netsh("wlan show profiles")
    profiles = set()
    patterns = [r"All User Profile\s*:\s*(.+)",
                r"Profil uživatele\s*:\s*(.+)",
                r"Profile\s*:\s*(.+)",
                r"Profile\(s\)\s*:\s*(.+)"]
    for pat in patterns:
        for m in re.findall(pat, out, flags=re.IGNORECASE):
            name = m.strip().strip('"')
            if name:
                profiles.add(name)
    if not profiles:
        for line in out.splitlines():
            if ":" in line:
                left,right = line.split(":",1)
                if 0 < len(right.strip()) < 100 and len(left.strip()) < 40:
                    profiles.add(right.strip().strip('"'))
    return sorted(profiles)

def get_profile_password(profile):
    safe = profile.replace('"','')
    out = run_netsh(f'wlan show profile name="{safe}" key=clear')
    m = re.search(r"Key Content\s*:\s*(.+)", out, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"(?:Key|Klíč)[^\n:]{0,20}:\s*(.+)", out, re.IGNORECASE)
    if m2:
        candidate = m2.group(1).strip()
        if candidate and len(candidate) < 128:
            return candidate
    return None

def gather_text():
    profiles = list_profiles()
    if not profiles:
        return "Žádné Wi-Fi profily nebyly nalezeny.\n"
    lines = []
    lines.append("Export Wi-Fi profilů a hesel\n\n")
    lines.append("POZOR: obsahuje citlivé údaje. Uložte bezpečně.\n\n")
    lines.append("="*60 + "\n\n")
    for p in profiles:
        lines.append(f"SSID: {p}\n")
        try:
            logger.info(f"Zpracovávám profil: {p}")
            pwd = get_profile_password(p)
            if pwd:
                lines.append(f"Password: {pwd}\n")
            else:
                lines.append("Password: (nebylo nalezeno / enterprise / chráněné)\n")
        except Exception as e:
            logger.error(f"Chyba při čtení profilu {p}: {e}")
            lines.append(f"Password: (chyba při čtení: {e})\n")
        lines.append("\n")
    return "".join(lines)

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERS,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return urlsafe_b64encode(key)  # Fernet expects base64-urlsafe 32B key

def encrypt_bytes(plaintext: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password.encode('utf-8'), salt)
    f = Fernet(key)
    token = f.encrypt(plaintext)
    return MAGIC + salt + token

def decrypt_file_to_bytes(blob: bytes, password: str) -> bytes:
    if not blob.startswith(MAGIC):
        raise ValueError("Neznámý formát souboru.")
    salt = blob[len(MAGIC):len(MAGIC)+SALT_SIZE]
    token = blob[len(MAGIC)+SALT_SIZE:]
    key = derive_key(password.encode('utf-8'), salt)
    f = Fernet(key)
    try:
        logger.info("Začínám dešifrování souboru.")
        return f.decrypt(token)
    except InvalidToken as e:
        logger.error("Neplatné heslo nebo poškozený soubor (dešifrování selhalo).")
        raise InvalidToken("Neplatné heslo nebo poškozený soubor (dešifrování selhalo).") from e

def main():
    parser = argparse.ArgumentParser(description="Export a AES-šifrovaný zápis Wi-Fi profilů (Windows).")
    parser.add_argument('--out', '-o', default='wifi_passwords.txt.encrypted', help='Výstupní šifrovaný soubor.')
    parser.add_argument('--decrypt', '-d', metavar='FILE', help='Dešifrovat zadaný soubor a vypsat na stdout.')
    args = parser.parse_args()

    if args.decrypt:
        # dešifrovací mód
        if not os.path.exists(args.decrypt):
            print("Soubor neexistuje:", args.decrypt, file=sys.stderr); sys.exit(2)
        pwd = getpass.getpass("Zadej heslo pro dešifrování: ")
        with open(args.decrypt, 'rb') as f:
            blob = f.read()
        try:
            logger.info(f"Začínám dešifrování souboru: {args.decrypt}")
            plain = decrypt_file_to_bytes(blob, pwd)
        except Exception as e:
            logger.error(f"Chyba při dešifrování souboru {args.decrypt}: {e}")
            print("Chyba při dešifrování:", e, file=sys.stderr)
            sys.exit(3)
        # vypíšeme na stdout (bez uložení)
        sys.stdout.buffer.write(plain)
        return

    # běžný mód: export + šifrování
    print("Shromažďuji Wi-Fi profily (může být potřeba spustit jako správce)...")
    plaintext = gather_text().encode('utf-8')
    pwd = getpass.getpass("Zadej heslo pro šifrování (pečlivě si ho zapamatuj): ")
    pwd2 = getpass.getpass("Potvrď heslo: ")
    if pwd != pwd2:
        print("Hesla se neshodují. Přerušuji.", file=sys.stderr); sys.exit(1)
    blob = encrypt_bytes(plaintext, pwd)
    outfn = args.out
    with open(outfn, 'wb') as f:
        f.write(blob)
    print(f"\n\n HOTOVO.\n\n Šifrovaný výstup uložen do: {os.path.abspath(outfn)}. \n\n K dešifrování použijte vámi zvolené heslo.")

if __name__ == "__main__":
    main()
