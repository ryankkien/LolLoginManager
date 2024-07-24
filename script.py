import json
import os
import subprocess

class LeagueLoginManager:
    def __init__(self):
        # File to store account information
        self.accounts_file = "lol_accounts.json"
        # Load existing accounts or create an empty dictionary
        self.accounts = self.load_accounts()

    def load_accounts(self):
        # Check if the accounts file exists
        if os.path.exists(self.accounts_file):
            # If it exists, load the accounts from the file
            with open(self.accounts_file, "r") as f:
                return json.load(f)
        # If the file doesn't exist, return an empty dictionary
        return {}

    def save_accounts(self):
        # Save the current accounts to the file
        with open(self.accounts_file, "w") as f:
            json.dump(self.accounts, f)

    def add_account(self, name, username, password):
        # Add a new account to the dictionary
        self.accounts[name] = {"username": username, "password": password}
        # Save the updated accounts to the file
        self.save_accounts()
        print(f"Account '{name}' added successfully.")

    def remove_account(self, name):
        # Check if the account exists
        if name in self.accounts:
            # If it does, remove it from the dictionary
            del self.accounts[name]
            # Save the updated accounts to the file
            self.save_accounts()
            print(f"Account '{name}' removed successfully.")
        else:
            print(f"Account '{name}' not found.")

    def list_accounts(self):
        # Check if there are any saved accounts
        if self.accounts:
            print("Saved accounts:")
            # Print the name of each saved account
            for name in self.accounts:
                print(f"- {name}")
        else:
            print("No saved accounts.")

    def login(self, name):
        # Check if the account exists
        if name in self.accounts:
            account = self.accounts[name]
            print(f"Logging in as {account['username']}...")
            
            # Path to League of Legends client (may need to be updated)
            lol_path = r"C:\Riot Games\League of Legends\LeagueClient.exe"
            
            # Construct the command to launch League with the account credentials
            cmd = f'"{lol_path}" --username {account["username"]} --password {account["password"]}'
            
            # Launch League of Legends with the specified account
            subprocess.Popen(cmd, shell=True)
        else:
            print(f"Account '{name}' not found.")

    def run(self):
        while True:
            # Display the main menu
            print("\nLeague of Legends Login Manager")
            print("1. Add account")
            print("2. Remove account")
            print("3. List accounts")
            print("4. Login")
            print("5. Exit")
            
            # Get user's choice
            choice = input("Enter your choice (1-5): ")
            
            # Process the user's choice
            if choice == "1":
                name = input("Enter account name: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.add_account(name, username, password)
            elif choice == "2":
                name = input("Enter account name to remove: ")
                self.remove_account(name)
            elif choice == "3":
                self.list_accounts()
            elif choice == "4":
                name = input("Enter account name to login: ")
                self.login(name)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    # Create an instance of the LeagueLoginManager
    manager = LeagueLoginManager()
    # Start the main loop
    manager.run()
    