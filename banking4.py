import random
import sqlite3
import os

def create_db():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card(" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "number TEXT, " +
                "pin TEXT, " +
                "balance INTEGER DEFAULT 0);")
    conn.commit()
    return conn

def write_db(conn, number, pin, balance):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO card (number, pin, balance) VALUES ({number}, {pin}, {balance});")
    conn.commit()

def read_db(conn, number, pin=None):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM card WHERE number = {number}')
    try:
        db_id, db_number, db_pin, db_balance = cur.fetchone()
    except TypeError:
        return None
    if pin != None and db_pin != pin:
        return None
    return db_balance

def update_db(conn, number, balance):
    cur = conn.cursor()
    cur.execute(f"UPDATE card SET balance = {balance} WHERE number = {number};")
    conn.commit()

def delete_db(conn, number):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM card WHERE number = {number};")
    conn.commit()

def get_menuno():
    print("1. Create an account") 
    print("2. Log into account")
    print("0. Exit")
    return(int(input()))

def calc_checkdg(card):
    total = 0
    for i in range(len(card)):
        digit = int(card[i])
        if i % 2 == 0:
            digit = digit * 2
            if digit >= 10:
                digit -= 9
        total += digit
    if total % 10 == 0:
        return "0"
    return str(10 - (total % 10))

def create_account(conn):
    while True:
        bin = "400000"
        account_number = "000000000" + str(random.randint(0, 999999999))
        account_number = account_number[len(account_number) - 9:]
        number = "400000" + account_number
        number += calc_checkdg(number)
        if read_db(conn, number) == None:
            break
        
    pin = str(random.randint(0, 9999))
    balance = 0
    write_db(conn, number, pin, balance)

    print("Your card has been created")
    print("Your card number:")
    print(number)
    print("Your card PIN:")
    print(pin)

def login(conn):
    print("Enter your card number:")
    number = input()
    print("Enter your PIN:")
    pin = input()
    print()
    balance = read_db(conn, number, pin)
    if balance is not None:
        print("You have successfully logged in!")
    else:
        print("Wrong card number or PIN!")
        return
    print()

    while True:
        menuno = get_account_menuno()
        print()
        if menuno == 1:
            show_balance(conn, number)
        elif menuno == 2:
            add_incom(conn, number)
        elif menuno == 3:
            transfer(conn, number)
        elif menuno == 4:
            close_account(conn, number)
            return False
        elif menuno == 5:
            logout()
            return False
        elif menuno == 0:
            return True
        print()

def get_account_menuno():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    return int(input())

def show_balance(conn, number):
    balance = read_db(conn, number)
    print(f"Balance: {balance}")

def add_incom(conn, number):
    print("Enter income:")
    incom = int(input())
    balance = read_db(conn, number)
    update_db(conn, number, balance + incom)
    print("Income was added!")

def transfer(conn, number):
    print("Transfer")
    print("Enter card number:")
    transfer_number = input()
    if len(transfer_number) != 16 or calc_checkdg(transfer_number[:len(transfer_number) - 1]) != transfer_number[-1]:
        print("Probably you made a mistake in the card number. Please try again!")
        return
    if transfer_number == number:
        print("You can't transfer money to the same account!")
        return
    transfer_balance = read_db(conn, transfer_number)
    if transfer_balance == None:
        print("Such a card does not exist.")
        return
    print("Enter how much money you want to transfer:")
    transfer_money = int(input())
    balance = read_db(conn, number)
    if transfer_money > balance:
        print("Not enough money!")
        return
    update_db(conn, number, balance - transfer_money)
    update_db(conn, transfer_number, transfer_balance + transfer_money)
    print("Success!")

def close_account(conn, number):
    delete_db(conn, number)
    print("The account has been closed!")

def logout():
    print("You have successfully logged out!")

def exit(conn):
    conn.close()
    print("Bye!")

if os.path.exists('card.s3db'):
    conn = sqlite3.connect('card.s3db')
else:
    conn = create_db()

random.seed(17)

while True:
    menuno = get_menuno()
    print()
    if menuno == 1:
        create_account(conn)
    elif menuno == 2:
        exit_flag = login(conn)
        if exit_flag:
            exit(conn)
            break
    elif menuno == 0:
        exit(conn)
        break
    print()