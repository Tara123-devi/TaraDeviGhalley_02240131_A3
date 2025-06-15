import tkinter as tk
from tkinter import messagebox, simpledialog
import sys

class BankingError(Exception):
    #Base exception class for banking application errors
    pass

class InsufficientFundsError(BankingError):
    #Exception raised when account has insufficient funds
    pass

class InvalidAmountError(BankingError):
    #Exception raised when an invalid amount is entered
    pass

class AccountNotFoundError(BankingError):
    #Exception raised when an account is not found
    pass

class BankAccount:
    #Class representing a bank account with basic operations
    
    def __init__(self, name, initial_balance=0):
        """
        Initialize a bank account
        
        Args:
            name (str): Account holder name
            initial_balance (float): Starting balance (default 0)
        """
        self.name = name
        self.balance = initial_balance
        self.transactions = []
    
    def deposit(self, amount):
        """
        Deposit money into the account
        
        Args:
            amount (float): Amount to deposit
            
        Raises:
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")
    
    def withdraw(self, amount):
        """
        Withdraw money from the account
        
        Args:
            amount (float): Amount to withdraw
            
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
        """
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.balance -= amount
        self.transactions.append(f"Withdrew: {amount}")
    
    def transfer(self, amount, target_account):
        """
        Transfer money to another account
        
        Args:
            amount (float): Amount to transfer
            target_account (BankAccount): Account to transfer to
            
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
        """
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for transfer")
        self.balance -= amount
        target_account.balance += amount
        self.transactions.append(f"Transferred: {amount} to {target_account.name}")
        target_account.transactions.append(f"Received: {amount} from {self.name}")
    
    def mobile_topup(self, amount, phone_number):
        """
        Top up mobile phone balance
        
        Args:
            amount (float): Amount to top up
            phone_number (str): Phone number to top up
            
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If account has insufficient funds
        """
        if amount <= 0:
            raise InvalidAmountError("Top-up amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for top-up")
        self.balance -= amount
        self.transactions.append(f"Mobile top-up: {amount} to {phone_number}")
    
    def get_transactions(self):
        #Return list of transactions
        return self.transactions
    
    def _str_(self):
        """String representation of account"""
        return f"Account(name={self.name}, balance={self.balance})"

class BankingAppGUI:
    #Class providing a GUI for the banking application
    
    def __init__(self, master):
        """
        Initialize the banking application GUI
        
        Args:
            master: The root window
        """
        self.master = master
        master.title("Banking Application")
        
        self.accounts = {}
        self.current_account = None
        
        # Create widgets
        self.label = tk.Label(master, text="Welcome to Banking App")
        self.label.pack()
        
        self.create_account_button = tk.Button(master, text="Create Account", command=self.create_account)
        self.create_account_button.pack()
        
        self.select_account_button = tk.Button(master, text="Select Account", command=self.select_account)
        self.select_account_button.pack()
        
        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit, state=tk.DISABLED)
        self.deposit_button.pack()
        
        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw, state=tk.DISABLED)
        self.withdraw_button.pack()
        
        self.transfer_button = tk.Button(master, text="Transfer", command=self.transfer, state=tk.DISABLED)
        self.transfer_button.pack()
        
        self.topup_button = tk.Button(master, text="Mobile Top-up", command=self.mobile_topup, state=tk.DISABLED)
        self.topup_button.pack()
        
        self.delete_button = tk.Button(master, text="Delete Account", command=self.delete_account, state=tk.DISABLED)
        self.delete_button.pack()
        
        self.balance_label = tk.Label(master, text="No account selected")
        self.balance_label.pack()
        
        self.transactions_text = tk.Text(master, height=10, width=50, state=tk.DISABLED)
        self.transactions_text.pack()
        
        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()
    
    def create_account(self):
        #Create a new bank account
        name = simpledialog.askstring("Create Account", "Enter account holder name:")
        if name:
            if name in self.accounts:
                messagebox.showerror("Error", "Account with this name already exists")
            else:
                initial_balance = simpledialog.askfloat("Create Account", "Enter initial balance:", minvalue=0)
                if initial_balance is not None:
                    self.accounts[name] = BankAccount(name, initial_balance)
                    messagebox.showinfo("Success", f"Account created for {name}")
    
    def select_account(self):
        #Select an existing account
        if not self.accounts:
            messagebox.showerror("Error", "No accounts exist yet")
            return
        
        name = simpledialog.askstring("Select Account", "Enter account holder name:")
        if name and name in self.accounts:
            self.current_account = self.accounts[name]
            self.update_display()
            self.enable_account_buttons()
        elif name:
            messagebox.showerror("Error", "Account not found")
    
    def update_display(self):
        #Update the display with current account info
        if self.current_account:
            self.balance_label.config(text=f"Balance for {self.current_account.name}: ${self.current_account.balance:.2f}")
            
            self.transactions_text.config(state=tk.NORMAL)
            self.transactions_text.delete(1.0, tk.END)
            transactions = self.current_account.get_transactions()
            if transactions:
                self.transactions_text.insert(tk.END, "Transaction History:\n")
                for txn in transactions:
                    self.transactions_text.insert(tk.END, f"- {txn}\n")
            else:
                self.transactions_text.insert(tk.END, "No transactions yet")
            self.transactions_text.config(state=tk.DISABLED)
    
    def enable_account_buttons(self):
        #Enable buttons that require an account to be selected
        for button in [self.deposit_button, self.withdraw_button, 
                      self.transfer_button, self.topup_button, 
                      self.delete_button]:
            button.config(state=tk.NORMAL)
    
    def deposit(self):
        #Deposit money into the selected account
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:", minvalue=0.01)
        if amount:
            try:
                self.current_account.deposit(amount)
                self.update_display()
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
            except BankingError as e:
                messagebox.showerror("Error", str(e))
    
    def withdraw(self):
        #Withdraw money from the selected account
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:", minvalue=0.01)
        if amount:
            try:
                self.current_account.withdraw(amount)
                self.update_display()
                messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
            except BankingError as e:
                messagebox.showerror("Error", str(e))
    
    def transfer(self):
        #Transfer money to another account
        if len(self.accounts) < 2:
            messagebox.showerror("Error", "Need at least 2 accounts to transfer")
            return
        
        target_name = simpledialog.askstring("Transfer", "Enter recipient account name:")
        if target_name:
            if target_name == self.current_account.name:
                messagebox.showerror("Error", "Cannot transfer to same account")
                return
                
            if target_name in self.accounts:
                amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:", minvalue=0.01)
                if amount:
                    try:
                        self.current_account.transfer(amount, self.accounts[target_name])
                        self.update_display()
                        messagebox.showinfo("Success", f"Transferred ${amount:.2f} to {target_name}")
                    except BankingError as e:
                        messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Recipient account not found")
    
    def mobile_topup(self):
        #Top up mobile phone balance
        phone_number = simpledialog.askstring("Mobile Top-up", "Enter phone number:")
        if phone_number:
            amount = simpledialog.askfloat("Mobile Top-up", "Enter amount to top up:", minvalue=0.01)
            if amount:
                try:
                    self.current_account.mobile_topup(amount, phone_number)
                    self.update_display()
                    messagebox.showinfo("Success", f"Topped up ${amount:.2f} to {phone_number}")
                except BankingError as e:
                    messagebox.showerror("Error", str(e))
    
    def delete_account(self):
        #Delete the selected account
        confirm = messagebox.askyesno("Confirm", f"Delete account for {self.current_account.name}?")
        if confirm:
            del self.accounts[self.current_account.name]
            self.current_account = None
            self.balance_label.config(text="No account selected")
            self.transactions_text.config(state=tk.NORMAL)
            self.transactions_text.delete(1.0, tk.END)
            self.transactions_text.config(state=tk.DISABLED)
            
            for button in [self.deposit_button, self.withdraw_button, 
                         self.transfer_button, self.topup_button, 
                         self.delete_button]:
                button.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", "Account deleted")

def processUserInput(choice, accounts, current_account):
    """
    Process user input for the banking application (console version)
    
    Args:
        choice (str): User's menu choice
        accounts (dict): Dictionary of bank accounts
        current_account (BankAccount): Currently selected account
        
    Returns:
        tuple: Updated (accounts, current_account)
    """
    try:
        if choice == '1':
            name = input("Enter account holder name: ")
            if name in accounts:
                print("Error: Account with this name already exists")
            else:
                initial_balance = float(input("Enter initial balance: "))
                accounts[name] = BankAccount(name, initial_balance)
                print(f"Account created for {name}")
        
        elif choice == '2':
            name = input("Enter account holder name: ")
            if name in accounts:
                current_account = accounts[name]
                print(f"Selected account: {name}")
            else:
                print("Error: Account not found")
        
        elif choice == '3':
            if current_account:
                amount = float(input("Enter amount to deposit: "))
                current_account.deposit(amount)
                print(f"Deposited {amount}")
            else:
                print("Error: No account selected")
        
        elif choice == '4':
            if current_account:
                amount = float(input("Enter amount to withdraw: "))
                current_account.withdraw(amount)
                print(f"Withdrew {amount}")
            else:
                print("Error: No account selected")
        
        elif choice == '5':
            if current_account:
                if len(accounts) < 2:
                    print("Error: Need at least 2 accounts to transfer")
                else:
                    target_name = input("Enter recipient account name: ")
                    if target_name == current_account.name:
                        print("Error: Cannot transfer to same account")
                    elif target_name in accounts:
                        amount = float(input("Enter amount to transfer: "))
                        current_account.transfer(amount, accounts[target_name])
                        print(f"Transferred {amount} to {target_name}")
                    else:
                        print("Error: Recipient account not found")
            else:
                print("Error: No account selected")
        
        elif choice == '6':
            if current_account:
                phone_number = input("Enter phone number: ")
                amount = float(input("Enter amount to top up: "))
                current_account.mobile_topup(amount, phone_number)
                print(f"Topped up {amount} to {phone_number}")
            else:
                print("Error: No account selected")
        
        elif choice == '7':
            if current_account:
                confirm = input(f"Delete account for {current_account.name}? (y/n): ")
                if confirm.lower() == 'y':
                    del accounts[current_account.name]
                    current_account = None
                    print("Account deleted")
            else:
                print("Error: No account selected")
        
        elif choice == '8':
            if current_account:
                print(f"Balance for {current_account.name}: {current_account.balance}")
                print("Transactions:")
                for txn in current_account.get_transactions():
                    print(f"- {txn}")
            else:
                print("Error: No account selected")
        
        elif choice == '9':
            print("Exiting...")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")
    
    except ValueError:
        print("Error: Invalid amount entered")
    except BankingError as e:
        print(f"Error: {e}")
    
    return accounts, current_account

def console_main():
    #Main function for console version of banking app
    accounts = {}
    current_account = None
    
    while True:
        print("\nBanking Application Menu:")
        print("1. Create Account")
        print("2. Select Account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Mobile Top-up")
        print("7. Delete Account")
        print("8. View Balance & Transactions")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        accounts, current_account = processUserInput(choice, accounts, current_account)

def gui_main():
    #Main function for GUI version of banking app
    root = tk.Tk()
    app = BankingAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("Banking Application")
    print("1. Console version")
    print("2. GUI version")
    mode = input("Select version (1 or 2): ")
    
    if mode == '1':
        console_main()
    elif mode == '2':
        gui_main()
    else:
        print("Invalid selection")

        