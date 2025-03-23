import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Global dictionary to store transactions
transactions = {}

# File handling functions
def load_transactions():
    # Load transactions from the JSON file 
    global transactions
    try:
        with open('transactions.json', 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        # If file is not available, transactions dictionary will be empty
        pass
    except json.decoder.JSONDecodeError:
        # Handle invalid JSON format
        print("Error: Invalid JSON format in transactions file.")

def save_transactions():
    # Save transactions from the 'transactions' dictionary into the JSON file
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file, indent=2)  # Use indent parameter for pretty printing

def read_bulk_transactions_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except json.decoder.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filename}.")
        return {}

# Feature implementations
def add_transaction():
    # Add a new transaction
    global transactions
    while True:
        try:
            amount = float(input("Enter transaction amount: "))
            break  # break the loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    description = input("Enter transaction description: ")
    while True:
        transaction_type = input("Enter transaction type (Income/Expense): ").capitalize()
        if transaction_type in ['Income', 'Expense']:
            break  # break the loop if input is valid
        else:
            print("Invalid input. Please enter 'Income' or 'Expense'.")

    while True:
        try:
            date = input("Enter transaction date (YYYY-MM-DD): ")
            datetime.strptime(date, "%Y-%m-%d")  # validate date format 
            break  # break the loop if input is valid
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")

    # Check if the type already exists, if not, create a new key with an empty list
    if transaction_type not in transactions:
        transactions[transaction_type] = []

    # Append the new transaction to the corresponding type list
    transactions[transaction_type].append({"amount": amount, "description": description, "date": date})
    print("Your transaction is successfully added!")

def view_transactions():
    # Initialize Tkinter window
    root = tk.Tk()
    root.title("View Transactions")

    # Function to filter transactions based on search query
    def filter_transactions():
        search_query = search_entry.get().strip().lower()
        income_tree.delete(*income_tree.get_children())
        expense_tree.delete(*expense_tree.get_children())
        if transactions:
            income_index = 1
            expense_index = 1
            for transaction_type, transactions_list in transactions.items():
                for transaction in transactions_list:
                    if search_query in transaction["description"].lower():
                        if transaction_type == "Income":
                            income_tree.insert("", "end", values=(income_index, transaction["amount"], transaction["description"], transaction["date"]))
                            income_index += 1
                        elif transaction_type == "Expense":
                            expense_tree.insert("", "end", values=(expense_index, transaction["amount"], transaction["description"], transaction["date"]))
                            expense_index += 1

    # Function to sort transactions based on column
    def sort_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)

    # Create a Frame for the search bar
    search_frame = ttk.Frame(root)
    search_frame.pack(fill="x", padx=10, pady=5)
    search_label = ttk.Label(search_frame, text="Search:")
    search_label.pack(side="left")
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", expand=True, fill="x")
    search_button = ttk.Button(search_frame, text="Search", command=filter_transactions)
    search_button.pack(side="left")

    # Create a Treeview widget for Income transactions
    income_frame = ttk.LabelFrame(root, text="Income Transactions")
    income_frame.pack(fill="both", expand=True, padx=10, pady=5)
    income_tree = ttk.Treeview(income_frame, columns=("Index", "Amount", "Description", "Date"), show="headings")
    income_tree.heading("Index", text="Index", command=lambda: sort_column(income_tree, "Index", False))
    income_tree.heading("Amount", text="Amount", command=lambda: sort_column(income_tree, "Amount", False))
    income_tree.heading("Description", text="Description", command=lambda: sort_column(income_tree, "Description", False))
    income_tree.heading("Date", text="Date", command=lambda: sort_column(income_tree, "Date", False))
    income_tree.pack(expand=True, fill="both")

    # Create a Treeview widget for Expense transactions
    expense_frame = ttk.LabelFrame(root, text="Expense Transactions")
    expense_frame.pack(fill="both", expand=True, padx=10, pady=5)
    expense_tree = ttk.Treeview(expense_frame, columns=("Index", "Amount", "Description", "Date"), show="headings")
    expense_tree.heading("Index", text="Index", command=lambda: sort_column(expense_tree, "Index", False))
    expense_tree.heading("Amount", text="Amount", command=lambda: sort_column(expense_tree, "Amount", False))
    expense_tree.heading("Description", text="Description", command=lambda: sort_column(expense_tree, "Description", False))
    expense_tree.heading("Date", text="Date", command=lambda: sort_column(expense_tree, "Date", False))
    expense_tree.pack(expand=True, fill="both")

    # Insert all transactions initially
    if transactions:
        income_index = 1
        expense_index = 1
        for transaction_type, transactions_list in transactions.items():
            for transaction in transactions_list:
                if transaction_type == "Income":
                    income_tree.insert("", "end", values=(income_index, transaction["amount"], transaction["description"], transaction["date"]))
                    income_index += 1
                elif transaction_type == "Expense":
                    expense_tree.insert("", "end", values=(expense_index, transaction["amount"], transaction["description"], transaction["date"]))
                    expense_index += 1

    # Run the Tkinter event loop
    root.mainloop()


def update_transaction():
    #update transactions
    global transactions
    view_transactions()
    if transactions:
        try:
            transaction_type = input("Enter transaction type to update(income/expense):").capitalize()
            if transaction_type in transactions:
                index = int(input("Enter the index of the transaction to update: ")) - 1
                if 0 <= index < len(transactions[transaction_type]):
                    amount = float(input("Enter new transaction amount: "))
                    description = input("Enter new transaction description: ")
                    date = input("Enter new transaction date (YYYY-MM-DD): ")
                    transactions[transaction_type][index] = {"amount": amount, "description": description, "date": date}
                    print("Successfully updated...")
                else:
                    print("Invalid index.")
            else:
                print("Invalid transaction type.")
        except ValueError:
            print("Invalid input.")
    else:
        print("No transactions available.")

def delete_transaction():
    #delete transactions
    global transactions
    view_transactions()
    if transactions:
        try:
            transaction_type = input("Enter transaction type to delete(income/expense):").capitalize()
            if transaction_type in transactions:
                index = int(input("Enter the index of the transaction to delete: ")) - 1
                if 0 <= index < len(transactions[transaction_type]):
                    del transactions[transaction_type][index]
                    print("Transaction deleted successfully.")
                else:
                    print("Invalid index.")
            else:
                print("Invalid transaction type.")
        except ValueError:
            print("Invalid input.")
    else:
        print("No transactions available.")

def display_summary():
    #display a summary
    global transactions
    if transactions:
        for transaction_type, transactions_list in transactions.items():
            total_amount = sum(transaction['amount'] for transaction in transactions_list)
            print(f"Total {transaction_type}: {total_amount}")
    else:
        print("No transactions available.")

def main_menu():
    #main menu for the finance tracker application
    load_transactions()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            save_transactions()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

#recall the function
main_menu()
