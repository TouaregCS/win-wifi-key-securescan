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
[GitHub profile TouaregCS](https://github.com/TouaregCS/)

![CLI](https://private-user-images.githubusercontent.com/114004388/512818066-afc08b7d-ecb0-41af-ae6b-85183ed7df55.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjI4ODU3NjMsIm5iZiI6MTc2Mjg4NTQ2MywicGF0aCI6Ii8xMTQwMDQzODgvNTEyODE4MDY2LWFmYzA4YjdkLWVjYjAtNDFhZi1hZTZiLTg1MTgzZWQ3ZGY1NS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTExJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTExMVQxODI0MjNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iOTY4NDZlMjQ2MWFmNzkyMjBlMWQzOTZiOWQ2ZTgzYjdhNGJlMjE5M2MxZjJkMDNiYTU2NzU2MTUzNWEwMjg5JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.HXfvA7khfeSQtq338vmXmiRxwuvhkrZIFtycy45twxY)
