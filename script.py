import json
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from pyautogui import locateOnScreen, click, write, press
import win32gui
import win32con



class LeagueLoginManager(QWidget):
    def __init__(self):
        super().__init__()
        self.accounts_file = "lol_accounts.json"
        self.accounts = self.load_accounts()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('League of Legends Login Manager')
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Account list
        self.account_list = QListWidget()
        self.update_account_list()
        layout.addWidget(self.account_list)

        # Add account section
        add_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Account Name")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        add_button = QPushButton("Add Account")
        add_button.clicked.connect(self.add_account)

        add_layout.addWidget(self.name_input)
        add_layout.addWidget(self.username_input)
        add_layout.addWidget(self.password_input)
        add_layout.addWidget(add_button)

        layout.addLayout(add_layout)

        # Action buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        remove_button = QPushButton("Remove Account")
        remove_button.clicked.connect(self.remove_account)

        button_layout.addWidget(login_button)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_accounts(self):
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as f:
                return json.load(f)
        return {}

    def save_accounts(self):
        with open(self.accounts_file, "w") as f:
            json.dump(self.accounts, f)

    def update_account_list(self):
        self.account_list.clear()
        for name in self.accounts:
            self.account_list.addItem(name)

    def add_account(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if name and username and password:
            self.accounts[name] = {"username": username, "password": password}
            self.save_accounts()
            self.update_account_list()
            self.name_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            QMessageBox.information(self, "Success", f"Account '{name}' added successfully.")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def remove_account(self):
        current_item = self.account_list.currentItem()
        if current_item:
            name = current_item.text()
            del self.accounts[name]
            self.save_accounts()
            self.update_account_list()
            QMessageBox.information(self, "Success", f"Account '{name}' removed successfully.")
        else:
            QMessageBox.warning(self, "Error", "Please select an account to remove.")

    def login(self):
        # After clicking the login button:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        current_item = self.account_list.currentItem()
        if current_item:
            name = current_item.text()
            account = self.accounts[name]
            
            # Locate the username field
            username_field = locateOnScreen('username_field.png', confidence=0.95)
            if username_field:
                click(username_field)
                write(account["username"])
            else:
                QMessageBox.warning(self, "Error", "Couldn't find username field. Is the client open?")
                return

            # Locate the password field
            password_field = locateOnScreen('password_field.png', confidence=0.95)
            if password_field:
                click(password_field)
                write(account["password"])
            else:
                QMessageBox.warning(self, "Error", "Couldn't find password field. Is the client open?")
                return

            # Locate and click the login button
            login_button = locateOnScreen('login_button.png', confidence=0.95)
            if login_button:
                click(login_button)
                QMessageBox.information(self, "Login", f"Credentials filled for {account['username']}. Click login to proceed.")
            else:
                QMessageBox.warning(self, "Error", "Couldn't find login button. Is the client open?")
        else:
            QMessageBox.warning(self, "Error", "Please select an account to login.")

app = QApplication([])
manager = LeagueLoginManager()
manager.show()
app.exec_()
