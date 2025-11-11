# 🔐 Wi-Fi Keys Tools for Windows

A small utility set for exporting, encrypting, and decrypting saved Wi-Fi passwords on **Windows**.  
It allows secure backup and recovery of Wi-Fi credentials using **strong AES-256 encryption (Fernet)**.

> [!CAUTION]
> This tool is **only for personal use**.
> Author does **not take any responsibility** for misuse, data loss, or any damage caused by using this tool.

## 🔒 Security

- The password is never stored!
- Encryption uses:
        - ```PBKDF2HMAC``` (390k iterations, 16B salt)
        - ```AES-256``` (Fernet)
- The output file contains no readable data!

## ⚠️ Disclaimer

By using Wi-Fi Key SecureScan, you agree to the following:

- You are **authorized** to access and extract Wi-Fi profiles from the system where this tool is executed.  
- You will **not** use this software to access, store, or share credentials that you do not have permission to view.  
- You understand that Wi-Fi passwords are **sensitive information** and must be handled responsibly.

> [!WARNING]
> This project was created to **help users understand and manage their own network credentials securely**, not to be used for any malicious or unauthorized purpose.

---
Sada nástrojů pro export, šifrování a dešifrování uložených Wi-Fi hesel v systému **Windows**.  
Umožňuje bezpečně zálohovat a obnovit Wi-Fi přihlašovací údaje pomocí **silného šifrování AES-256 (Fernet)**.

## 🧠 Architektura

| Vrstva     | Popis                                                 |
| ---------- | ----------------------------------------------------- |
| ```scripts/``` | Obsahuje logiku pro šifrování, dešifrování a logování |
| ```main.py```  | Řídicí CLI aplikace (menu)                            |
| ```assets/```  | Ikony a grafické soubory                              |

## 🔐 Použité knihovny

- ```cryptography``` - bezpečné šifrování pomocí Fernet (AES-256)
- ```colorama``` - barevný výstup v terminálu
- ```logging``` - záznam událostí do logu

---

## 💬 Autor

**TouaregCS**
[GitHub](https://github.com/TouaregCS)
