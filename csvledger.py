import csv
import datetime
import re

import click

from config import Config


class CSVledger:
    def __init__(self, config_file=None):
        self.config = Config(config_file)

    def filter_description(self, row):
        """ Removes extra data from the transaction description"""
        result = row
        for text in self.config.filter:
            result = result.replace(text, "")

        # TODO Move this to the config
        # Remove the Transaction Date
        result = re.sub(r"\d\d[-]\d\d", "", result)

        # Strip whitespace
        result = result.strip()
        return result

    def categorize_transaction(self, description):
        """
        Matches the transaction description from the accounts and vendors
        listed in the config file.

        :param description: transaction descrption
        """
        accounts = self.config.accounts
        for group in accounts:
            for account, vendors in group.items():
                for vendor in vendors:
                    if vendor in description:
                        return account

    def print_transaction(self, date, description, debit, credit):
        """ Prints the transaction in ledger format. """
        if debit:
            print(f"{date} * {description}")
            print(
                f"\t \t {self.categorize_transaction(description)} \t \
                ${format(debit, '.2f')}"
            )
            print("\t \t Assets:Checking \n")
        elif credit:
            print(f"{date} * {description}")
            print(f"\t \t Assets:Checking \t ${format(credit, '.2f')}")
            print(f"\t \t {self.categorize_transaction(description)} \n")

    def print_total(self, total_credit, total_debit):
        """
        Prints the combined total of all credit and debit transactions

        :param total_credit: sum total of credit transactions
        :param total_debit: sum total of debit transactions
        """
        print(f"Credit: +${format(total_credit, '.2f')}")
        print(f"Debit: -${format(total_debit, '.2f')}")

    # TODO allow for initial date format to be specified
    def format_date(self, date):
        """ Converts date to ledgers default format of '%Y/%m/%d' """
        return datetime.datetime.strptime(date, "%m/%d/%Y").strftime(
            "%Y/%m/%d"
        )


@click.command()
@click.option(
    "--config",
    type=click.Path(exists=True, readable=True),
    help="path to config file",
)
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
@click.option(
    "--total",
    is_flag=True,
    help="prints sum of all credit and debit transactions",
)
@click.option(
    "--convert", is_flag=True, help="prints transactions in ledger format",
)
def cli(csvfile, check, config, total, convert):
    """ This script coverts CSV files downloaded from a financial instution to
    ledger entries.  Each entry is categorized using the business name to
    determine the spending category. """

    convertor = CSVledger(config)

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
                    convertor.print_transaction(
                        date, description, debit, credit
                    )
            elif convert:
                convertor.print_transaction(date, description, debit, credit)
        if total:
            convertor.print_total(total_credit, total_debit)
