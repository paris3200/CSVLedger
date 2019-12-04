import csv
import re
import datetime
import json

import click


class CSVledger:
    def filter_description(self, row):
        """ Removes extra data from the transaction description"""
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

        # Strip whitespace
        result = result.strip()
        return result

    def categorize_transaction(self, description):

        # TODO Read accounts from config
        accounts = {}

        accounts["Assets:Savings"] = ["0060387673"]

        accounts["Expenses:Auto:Gas"] = [
            "EXXONMOBIL",
            "FOUR BRO",
            "SHEETZ",
            "SHELL OIL",
        ]

        accounts["Expenses:Food:Grocery"] = [
            "LOWE'S FOODS",
            "ALDI",
            "LIDL",
            "SAMSCLUB",
            "WAL-MART",
            "WM SUPERCENTER",
            "WM SUPERC",
            "MEAT CENTE",
            "TRIAD MUNICIPAL AB",
        ]

        accounts["Expenses:Food:Dining"] = [
            "BOJANGLES",
            "CHICK-FIL-A",
            "DAIRI-O",
            "EARLS",
            "EL SARAPE MEXICAN",
            "MCDONALD's",
            "PIZZA PERFECT",
            "PLAZA DEL SOL",
            "RIO GRANDE",
            "STARBUCKS",
            "WENDYS",
            "THE MASON JAR",
            "WISEMAN BREWING",
            "THIRSTY SOULS BREW",
        ]

        accounts["Expenses:Food:School Lunches"] = ["K12*STOKESCOUNTY"]

        accounts["Expenses:Homestead:Chickens"] = ["LTD"]

        accounts["Expenses:Household"] = [
            "DOLLAR GENERAL",
            "AMAZON com",
            "AMZN",
        ]

        accounts["Expenses:Household:Home Improvements"] = [
            "THE HOME DEPOT",
            "LOWES HOME",
        ]

        accounts["Expenses:Insurance:Life"] = ["CINTI LIF INS"]
        accounts["Expenses:Insurance:Auto"] = ["PENN NATIONAL IN AUTO"]
        accounts["Expenses:Entertainment"] = [
            "Prime Video",
            "AMZN Digital",
        ]

        accounts["Expenses:Utilites:Power"] = ["DUKEENERGY"]
        accounts["Expenses:Utilites:Internet"] = ["SPECTRUM", "TIMEWARNER"]
        accounts["Expenses:Personal Care:Doctor"] = [
            "STEPHEN W",
            "HUGH CHATHAM WOMENELKIN",
        ]
        accounts["Expenses:Personal Care:Medicine"] = ["CVS/PHARM"]

        accounts["Liabilites:Wells Fargo"] = ["WELLSFARGO"]
        accounts["Liabilites:SECU:Mortgage"] = ["6038767390"]
        accounts["Liabilites:SECU:Van"] = ["6038767305"]
        accounts["Liabilites:SECU:Visa"] = ["4046571218010930"]

        accounts["Income:Dakota:Salary"] = ["STATE OF NC", "Deposit USDA"]
        accounts["Income:Dakota:Dispatch"] = ["Deposit CAS5 TREAS"]
        accounts["Income:Misc"] = ["SECU Foundation", "Member Deposit"]
        accounts["Income:Interest"] = ["Dividend Earned"]

        accounts["Expenses:Checks"] = ["INCLEARING CHECK"]
        accounts["Assets:Cash"] = ["ATM Cash Withdrawal"]
        accounts["Expenses:Misc"] = ["VENMO"]
        accounts["Expenses:FEES"] = ["Overdraft Trnsfr Fee", "Safe Deposit Box Fee"]
        accounts["Expenses:Homestead"] = ["JACKS SMALL ENGINE"]
        accounts["Expenses:Auto:Maintenance"] = ["OREILLY"]
        accounts["Expenses:Personal Care:Clothes"] = ["TARGET"]
        accounts["Expenses:Personal Care:Hair Cut"] = ["DON'S BARB"]
        accounts["Expenses:Paris Leatherworks"] = ["019246000083916"]
        accounts["Expenses:Auto"] = ["STRICKLAND BROTHER"]

        for account, vendors in accounts.items():
            for vendor in vendors:
                if vendor in description:
                    return account

    def print_transaction(self, date, description, debit, credit):
        """ Prints the transaction in ledger format. """
        if debit:
            print(f"{date} *  {description}")
            print(
                f"\t \t {categorize_transaction(description)} \t ${format(debit, '.2f')}"
            )
            print("\t \t Assets:Checking \n")
        elif credit:
            print(f"{date} *  {description}")
            print(f"\t \t Assets:Checking \t ${format(credit, '.2f')}")
            print(f"\t \t {categorize_transaction(description)} \n")

    def print_total(self, total_credit, total_debit):
        """ Prints the combined total of all credit and debit transactions. """
        print(f"Credit: +{format(total_credit, '.2f')}")
        print(f"Debit: -{format(total_debit, '.2f')}")

    # TODO allow for initial date format to be specified
    def format_date(self, date):
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
def cli(csvfile, check):
    """ This script coverts CSV files downloaded from a financial instution to
    ledger entries.  Each entry is categorized using the business name to
    determine the spending category. """

    convertor = CSVledger()

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
            description = convertor.filter_description(row[2])

            date = convertor.format_date(row[0])

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
                if convertor.categorize_transaction(description) is None:
                    # No assocated Income/Expense category found
                    convertor.print_transaction(date, description, debit, credit)
            else:
                convertor.print_transaction(date, description, debit, credit)
