import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLineEdit, 
                             QLabel, QFileDialog, QMessageBox, QFrame, QGridLayout)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from colorama import Fore, Style, init
from scripts import logger_setup, wifi_crypted, wifi_decrypted

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class WifiScanGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinWifiScan Professional")
        self.setMinimumSize(900, 600)
        
        icon_path = resource_path(os.path.join('assets', 'klic.ico'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- 1. KROK: SKENOVÁNÍ ---
        scan_btn_layout = QGridLayout()

        self.btn_scan = QPushButton("🔍 1. SPUSTIT SKENOVÁNÍ (Zobrazit nález)")
        self.btn_scan.setStyleSheet("""
            QPushButton { background-color: #2c3e50; color: white; height: 50px; font-weight: bold; font-size: 14px; border-radius: 5px; border: 2px solid #000000}
            QPushButton:hover { background-color: #34495e; }
        """)
        self.btn_scan.clicked.connect(self.action_just_scan)

        self.btn_help = QPushButton("❓ Nápověda")
        self.btn_help.setStyleSheet("""
            QPushButton { background-color: #f39c12; color: #000000; height: 50px; font-weight: bold; font-size: 16px; border-radius: 5px; border: 2px solid #000000}
            QPushButton:hover { background-color: #e67e22; }
        """)
        self.btn_help.clicked.connect(self.show_help)

        scan_btn_layout.addWidget(self.btn_scan, 0, 0, 1, 5)
        scan_btn_layout.addWidget(self.btn_help, 0, 6)

        main_layout.addLayout(scan_btn_layout)

        # --- KONZOLE PRO ZOBRAZENÍ VÝSLEDKŮ ---
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(False) # Povolíme editaci, kdyby chtěl uživatel něco smazat před uložením
        self.log_display.setFont(QFont("Consolas", 10))
        self.log_display.setStyleSheet("""
                        background-color: #1e1e1e; 
                        color: #55ff55; /* Svítivě zelená */
                        padding: 10px; 
                        border: 2px solid #333;
                        selection-background-color: #2c3e50;
                        """)
        main_layout.addWidget(self.log_display)

        # --- 2. KROK: ZABEZPEČENÍ ---
        self.save_frame = QFrame()
        self.save_frame.setStyleSheet("background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
        save_layout = QVBoxLayout(self.save_frame)
        
        save_layout.addWidget(QLabel("<b>2. ZABEZPEČENÍ NÁLEZU:</b>"))
        
        h_pass_layout = QVBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Zadejte šifrovací heslo...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumWidth(200)
        
        self.password_confirm = QLineEdit()
        self.password_confirm.setPlaceholderText("Potvrďte heslo...")
        self.password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm.setMinimumWidth(200)

        h_pass_layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        h_pass_layout.addWidget(self.password_confirm, alignment=Qt.AlignmentFlag.AlignCenter)
        save_layout.addLayout(h_pass_layout)

        h_btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("💾 Zašifrovat a uložit do souboru")
        self.btn_save.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: #000000; height: 40px; font-weight: bold; font-size: 18px; margin-top: 5px; border: 2px solid #000000}
            QPushButton:hover { background-color: #2ecc71; }
        """)
        self.btn_save.clicked.connect(self.action_encrypt_and_save)
        
        self.btn_decrypt = QPushButton("🔓 Dešifrovat existující soubor")
        self.btn_decrypt.setStyleSheet("""
            QPushButton { background-color: #c0392b; color: #000000; height: 40px; font-weight: bold; font-size: 18px; margin-top: 5px; border: 2px solid #000000}
            QPushButton:hover { background-color: #e74c3c; }
        """)
        self.btn_decrypt.clicked.connect(self.action_decrypt_existing)
        
        h_btn_layout.addWidget(self.btn_save)
        h_btn_layout.addWidget(self.btn_decrypt)
        save_layout.addLayout(h_btn_layout)
        
        main_layout.addWidget(self.save_frame)

        self.apply_outline(self.btn_scan)
        self.apply_outline(self.btn_help)
        self.apply_outline(self.btn_save)
        self.apply_outline(self.btn_decrypt)

    def apply_outline(self, widget):
        """Pomocná metoda pro přidání 'tvrdého' stínu, který simuluje ohraničení textu"""
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor

        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(3)       # Ostrý okraj
        effect.setXOffset(3)          # Posun pro efekt tloušťky
        effect.setYOffset(3)
        effect.setColor(QColor(0, 0, 0, 255)) # Černá barva "okraje"
        widget.setGraphicsEffect(effect)

    # --- LOGIKA ---
    def show_help(self):
        """Zobrazí nápovědu uživateli"""
        help_text = (
            "1. Klikněte na 'SPUSTIT SKENOVÁNÍ' pro získání Wi-Fi profilů a hesel z vašeho systému.\n"
            "2. Zadejte silné heslo do obou polí pro zabezpečení dat.\n"
            "3. Klikněte na 'Zašifrovat a uložit do souboru' pro uložení šifrovaného nálezu.\n"
            "4. Pro dešifrování existujícího souboru klikněte na 'Dešifrovat existující soubor' a zadejte heslo."
        )
        QMessageBox.information(self, "Nápověda", help_text)

    def action_just_scan(self):
        """Pouze vytáhne data a ukáže je v okně"""
        self.log_display.clear()
        self.log_display.append("--- Probíhá skenování systému netsh... ---")
        try:
            results = wifi_crypted.gather_text()
            self.log_display.clear()
            self.log_display.append(results)
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Nepodařilo se načíst Wi-Fi data: {e}")

    def action_encrypt_and_save(self):
        """Vezme text z okna, heslo z políček a uloží soubor"""
        content = self.log_display.toPlainText()
        pwd = self.password_input.text()
        pwd_conf = self.password_confirm.text()

        if not content.strip() or "Export Wi-Fi profilů" not in content:
            QMessageBox.warning(self, "Prázdná data", "Nejdříve spusťte skenování, aby bylo co ukládat!")
            return

        if not pwd or pwd != pwd_conf:
            QMessageBox.critical(self, "Chyba hesla", "Hesla se musí shodovat!")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Uložit šifrovaný nález", "wifi_backup.encrypted", "Encrypted (*.encrypted)")
        
        if file_path:
            try:
                blob = wifi_crypted.encrypt_bytes(content.encode('utf-8'), pwd)
                with open(file_path, 'wb') as f:
                    f.write(blob)
                QMessageBox.information(self, "Úspěch", f"Data byla zabezpečena a uložena do:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Chyba při ukládání", str(e))

    def action_decrypt_existing(self):
        """Klasické dešifrování souboru z disku"""
        pwd = self.password_input.text()
        if not pwd:
            QMessageBox.warning(self, "Heslo", "Zadejte heslo pro dešifrování do pole výše.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Otevřít šifrovaný soubor", "", "Encrypted (*.encrypted)")
        if file_path:
            try:
                text = wifi_decrypted.decrypt_file(file_path, pwd)
                self.log_display.clear()
                self.log_display.append(text)
            except Exception:
                QMessageBox.critical(self, "Chyba", "Nesprávné heslo nebo poškozený soubor.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    gui = WifiScanGUI()
    gui.show()
    sys.exit(app.exec())

