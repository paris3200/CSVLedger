import csv
import re


def filter_description(row):
    result = row
    remove_text = [
        "Point of Sale",
        "L340",
        "DATE",
        "Debit",
        "WINSTON-SALE",
        "WINSTON SALE",
        "MOUNT AIRY",
        "MT AIRY",
        "KING",
        "PINNACLE",
        "SECU BILLPAY TO",
        "ACH",
    ]
    for text in remove_text:
        result = result.replace(text, "")

    # Remove the Transaction Date
    result = re.sub(r"\d\d[-]\d\d", "", result)

    result = result.strip()
    return result


def categorize_transaction(description):
    categories = {
        "LOWE'S FOODS": "Expenses:Food:Grocery",
        "ALDI": "Expenses:Food:Grocery",
        "LIDL": "Expenses:Food:Grocery",
        "SAMSCLUB": "Expenses:Food:Grocery",
        "MEAT CENTE": "Expenses:Food:Grocery",
        "FOUR BRO": "Expenses:Auto:Gas",
        "SHEETZ": "Expenses:Auto:Gas",
        "DAIRI-O": "Expenses:Food:Dining",
        "MCDONALD'S": "Expenses:Food:Dining",
        "STARBUCKS": "Expenses:Food:Dining",
        "BOJANGLES": "Expenses:Food:Dining",
        "PLAZA DEL SOL": "Expenses:Food:Dining",
        "THIRSTY SOULS BREW": "Expenses:Food:Dining",
        "WISEMAN BREWING": "Expenses:Food:Dining",
        "LTD FARM": "Expenses:Homestead:Chickens",
        "DOLLAR GENERAL": "Expenses:Household",
        "CINTI LIF INS": "Expenses:Insurance:Life",
        "DUKEENERGY": "Expenses:Utilites:Power",
        "WELLSFARGO": "Liabilites:Wellsfargo",
        "6038767390": "Liabilites:SECU:Mortgage",
        "6038767305": "Liabilites:SECU:Van",
        "4046571218010930": "Liabilites:SECU:Visa",
        "0060387673": "Assets:Savings",
        "STATE OF NC": "Income:Dakota:Salary",
        "Dividend Earned": "Income:Interest",
        "VENMO": "Expenses:Misc",
        "SECU Foundation": "Expenses:Misc",
    }
    for store, category in categories.items():
        if store in description:
            return category


def print_transaction(date, description, debit, credit):
    if debit:
        print(f"{date} *  {description}")
        print(f"\t \t {categorize_transaction(description)} \t ${format(debit, '.2f')}")
        print("\t \t Assets:Checking \n")
    elif credit:
        print(f"{date} *  {description}")
        print(f"\t \t Assets:Checking \t ${format(credit, '.2f')}")
        print(f"\t \t {categorize_transaction(description)} \n")


def print_total(total_credit, total_debit):
    print(f"Credit: +{format(total_credit, '.2f')}")
    print(f"Debit: -{format(total_debit, '.2f')}")
    print(f"Change: {format(total_credit-total_debit, '.2f')}")


# Open file
with open("transaction.csv", "r", newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    total_credit = 0
    total_debit = 0

    # Skip Header Row
    next(csv_reader)

    for row in csv_reader:
        credit = None
        debit = None
        description = filter_description(row[2])
        date = row[0]

        try:
            credit = float(row[3])
        except ValueError:
            pass
        else:
            total_credit += credit

        try:
            debit = float(row[4])
        except ValueError:
            pass
        else:
            total_debit += debit

        # if categorize_transaction(description) == None:
        #    print_transaction(date, description, debit, credit)

        print_transaction(date, description, debit, credit)
