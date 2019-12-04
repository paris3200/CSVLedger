import csv
import re
import datetime

import click


def filter_description(row):
    result = row
    remove_text = [
        "Point of Sale",
        "L340",
        "DATE",
        "Debit",
        "WINSTON-SALE",
        "WINSTON SALE",
        "WINSTON-SALNC",
        "MOUNT AIRY",
        "MT AIRY",
        "KING",
        "PINNACLE",
        "SECU BILLPAY TO",
        "ACH",
        "HILLSVILLE",
        "DOBSON",
        "MOCKSVILLE",
        "LEXINGTON",
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
        "SAMS CLUB": "Expenses:Food:Grocery",
        "WAL-MART": "Expenses:Food:Grocery",
        "WM SUPERCENTER": "Expenses:Food:Grocery",
        "WM SUPERC": "Expenses:Food:Grocery",
        "MEAT CENTE": "Expenses:Food:Grocery",
        "TRIAD MUNICIPAL AB": "Expenses:Food:Grocery",
        "FOUR BRO": "Expenses:Auto:Gas",
        "SHEETZ": "Expenses:Auto:Gas",
        "SHELL OIL": "Expenses:Auto:Gas",
        "EXXONMOBIL": "Expenses:Auto:Gas",
        "BOJANGLES": "Expenses:Food:Dining",
        "CHICK-FIL-A": "Expenses:Food:Dining",
        "DAIRI-O": "Expenses:Food:Dining",
        "EARLS": "Expenses:Food:Dining",
        "EL SARAPE MEXICAN ": "Expenses:Food:Dining",
        "MCDONALD'S": "Expenses:Food:Dining",
        "PIZZA PERFECT": "Expenses:Food:Dining",
        "PLAZA DEL SOL": "Expenses:Food:Dining",
        "RIO GRANDE": "Expenses:Food:Dining",
        "STARBUCKS": "Expenses:Food:Dining",
        "WENDYS": "Expenses:Food:Dining",
        "THE MASON JAR": "Expenses:Food:Dining",
        "THIRSTY SOULS BREW": "Expenses:Food:Dining",
        "WISEMAN BREWING": "Expenses:Food:Dining",
        "LTD FARM": "Expenses:Homestead:Chickens",
        "LTD FARM": "Expenses:Homestead:Chickens",
        "DOLLAR GENERAL": "Expenses:Household",
        "THE HOME DEPOT": "Expenses:Household:Home Improvements",
        "CINTI LIF INS": "Expenses:Insurance:Life",
        "PENN NATIONAL IN AUTO": "Expenses:Insurance:Auto",
        "DUKEENERGY": "Expenses:Utilites:Power",
        "TIMEWARNER": "Expenses:Utilites:Internet",
        "SPECTRUM": "Expenses:Utilites:Internet",
        "WELLSFARGO": "Liabilites:Wellsfargo",
        "6038767390": "Liabilites:SECU:Mortgage",
        "6038767305": "Liabilites:SECU:Van",
        "4046571218010930": "Liabilites:SECU:Visa",
        "0060387673": "Assets:Savings",
        "019246000083916": "Expenses:Paris Leatherworks",
        "STATE OF NC": "Income:Dakota:Salary",
        "Deposit USDA": "Income:Dakota:Salary",
        "Dividend Earned": "Income:Interest",
        "VENMO": "Expenses:Misc",
        "SECU Foundation": "Expenses:Misc",
        "Overdraft Trnsfr Fee": "Expenses:Fees",
        "Safe Deposit Box Fee": "Expenses:Fees",
        "TARGET": "Expenses:Personal Care:Clothes",
        "DON'S BARB": "Expenses:Personal Care:Haircut",
        "OREILLY": "Expenses:Auto:Maintenance",
        "Prime Video": "Expenses:Entertainment",
        "AMZN Digital": "Expenses:Entertainment",
        "Member Deposit": "Income:Misc",
        "CVS/PHARM": "Expenses:Personal Care:Medicine",
        "STEPHEN W": "Expenses:Personal Care:Doctor",
        "HUGH CHATHAM WOMENELKIN": "Expenses:Personal Care:Doctor",
        "Amazon com": "Expenses:Household",
        "AMZN": "Expenses:Household",
        "JACKS SMALL ENGINE": "Expenses:Household",
        "Deposit CAS5 TREAS ": "Income:Dakota:Dispatch",
        "STRICKLAND BROTHER": "Expenses:Auto:Inspection",
        "INCLEARING CHECK": "Expenses:Checks",
        "ATM Cash Withdrawal": "Expenses:Misc",
        "K12*STOKESCOUNTY": "Expenses:Food:School Lunch",
    }
    for store, category in categories.items():
        if store in description:
            return category


def print_transaction(date, description, debit, credit):
    """ Prints the transaction in ledger format. """
    if debit:
        print(f"{date} *  {description}")
        print(f"\t \t {categorize_transaction(description)} \t ${format(debit, '.2f')}")
        print("\t \t Assets:Checking \n")
    elif credit:
        print(f"{date} *  {description}")
        print(f"\t \t Assets:Checking \t ${format(credit, '.2f')}")
        print(f"\t \t {categorize_transaction(description)} \n")


def print_total(total_credit, total_debit):
    """ Prints the combined total of all credit and debit transactions. """
    print(f"Credit: +{format(total_credit, '.2f')}")
    print(f"Debit: -{format(total_debit, '.2f')}")


def format_date(date):
    """ Converts date to ledgers default format of '%Y/%m/%d' """
    return datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y/%m/%d")


@click.command()
@click.option(
    "--csvfile",
    "-i",
    type=click.Path(exists=True, readable=True),
    help="csv file to be converted",
)
@click.option(
    "--check",
    is_flag=True,
    help="prints all transaction without an expense/income category.",
)
def csvledger(csvfile, check):
    """ This script coverts CSV files downloaded from a financial instution to
    ledger entires.  Each entry is categorized using the business name to
    determine the spending category. """
    # Open file
    with open(csvfile, "r", newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        total_credit = 0
        total_debit = 0

        # Skip Header Row
        next(csv_reader)

        for row in csv_reader:
            credit = None
            debit = None
            description = filter_description(row[2])

            date = format_date(row[0])

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

            if check:
                if categorize_transaction(description) is None:
                    print_transaction(date, description, debit, credit)
            else:
                print_transaction(date, description, debit, credit)
