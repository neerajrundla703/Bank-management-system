import mysql.connector
import random
import string

class Bank:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  # Change
            database="bank_system"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def __accountgenerate(self):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        acc_id = alpha + num + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    def Createaccount(self):
        name = input("Tell your name: ")
        age = int(input("Tell your age: "))
        email = input("Tell your email: ")
        pin = int(input("Tell your 4-digit pin: "))
        account_no = self.__accountgenerate()

        if age < 18 or len(str(pin)) != 4:
            print("Sorry, you cannot create an account.")
            return

        sql = "INSERT INTO accounts (name, age, email, pin, account_no, balance) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (name, age, email, pin, account_no, 0))
        self.conn.commit()

        print("\n Account created successfully!")
        print(f"Account No: {account_no}")
        print("Please note it down.")

    def depositmoney(self):
        acc_no = input("Enter account number: ")
        pin = int(input("Enter your pin: "))

        self.cursor.execute("SELECT * FROM accounts WHERE account_no=%s AND pin=%s", (acc_no, pin))
        user = self.cursor.fetchone()

        if not user:
            print("No data found.")
            return

        amount = float(input("Enter deposit amount: "))
        if amount > 10000 or amount <= 0:
            print("Deposit must be between 0 and 10000.")
            return

        self.cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_no=%s", (amount, acc_no))
        self.conn.commit()
        print(" Amount deposited successfully.")

    def withdrawmoney(self):
        acc_no = input("Enter account number: ")
        pin = int(input("Enter your pin: "))

        self.cursor.execute("SELECT * FROM accounts WHERE account_no=%s AND pin=%s", (acc_no, pin))
        user = self.cursor.fetchone()

        if not user:
            print("No data found.")
            return

        amount = float(input("Enter withdrawal amount: "))
        if user['balance'] < amount:
            print("Insufficient balance.")
            return

        self.cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_no=%s", (amount, acc_no))
        self.conn.commit()
        print(" Amount withdrawn successfully.")

    def showdetails(self):
        acc_no = input("Enter account number: ")
        pin = int(input("Enter your pin: "))

        self.cursor.execute("SELECT * FROM accounts WHERE account_no=%s AND pin=%s", (acc_no, pin))
        user = self.cursor.fetchone()

        if not user:
            print("No data found.")
            return

        print("\n===== Account Details =====")
        for key, value in user.items():
            print(f"{key}: {value}")

    def updatedetails(self):
        acc_no = input("Enter account number: ")
        pin = int(input("Enter your pin: "))

        self.cursor.execute("SELECT * FROM accounts WHERE account_no=%s AND pin=%s", (acc_no, pin))
        user = self.cursor.fetchone()

        if not user:
            print(" No such user found.")
            return

        print("You cannot change age, account number, or balance.")
        new_name = input("Enter new name (leave blank to skip): ") or user['name']
        new_email = input("Enter new email (leave blank to skip): ") or user['email']
        new_pin = input("Enter new pin (leave blank to skip): ") or user['pin']

        self.cursor.execute(
            "UPDATE accounts SET name=%s, email=%s, pin=%s WHERE account_no=%s",
            (new_name, new_email, int(new_pin), acc_no)
        )
        self.conn.commit()
        print("Details updated successfully.")

    def Delete(self):
        acc_no = input("Enter account number: ")
        pin = int(input("Enter your pin: "))

        self.cursor.execute("SELECT * FROM accounts WHERE account_no=%s AND pin=%s", (acc_no, pin))
        user = self.cursor.fetchone()

        if not user:
            print("No such data exists.")
            return

        confirm = input("Press 'y' to confirm deletion: ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return

        self.cursor.execute("DELETE FROM accounts WHERE account_no=%s", (acc_no,))
        self.conn.commit()
        print(" Account deleted successfully.")

# ===== Main Menu =====
bank = Bank()
while True:
    print("\n===== Bank Menu =====")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Show Details")
    print("5. Update Details")
    print("6. Delete Account")
    print("7. Exit")

    choice = input("Enter choice: ")
    if choice == '1':
        bank.Createaccount()
    elif choice == '2':
        bank.depositmoney()
    elif choice == '3':
        bank.withdrawmoney()
    elif choice == '4':
        bank.showdetails()
    elif choice == '5':
        bank.updatedetails()
    elif choice == '6':
        bank.Delete()
    elif choice == '7':
        break
    else:
        print(" Invalid choice. Try again.")
