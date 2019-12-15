import csv
import datetime
import re

import click

from .config import Config


class CSVledger:
    """
    CSVledger taks the input of a CSV file of financial transactions, strips excessive
    data from the transactions and then converts the transactions to ledger-cli
    format.
    """

    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.credit = 0
        self.debit = 0

    def convert_file(self, csvfile=None, header=True, check=False):
        """
        :param csvfile: file path of csv file to processed
        :param header: Boolean - true if file contains a header row
        :param check: Boolean - check for unmatched transactions
        :return converted transactions
        """
        result = ""
        with open(csvfile, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            if header:
                next(csv_reader)

            for row in csv_reader:
                credit = None
                debit = None
                description = self.filter_description(row[2])

                date = self.format_date(row[0])

                try:
                    credit = float(row[3])
                except ValueError:
                    pass
                else:
                    self.credit += credit

                try:
                    debit = float(row[4])
                except ValueError:
                    pass
                else:
                    self.debit += debit

                if check:
                    if self.categorize_transaction(description) is None:
                        # No assocated Income/Expense category found
                        result += self.format_transaction(
                            date, description, debit, credit
                        )
                else:
                    result += self.format_transaction(date, description, debit, credit)

            return result

    def filter_description(self, description):
        """
        Delete extra data from the transaction description which is listed
        in the config file under filter.

        :param description:  the description to be filtered
        :returns: the filtered string
        """
        result = description
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

        :param description: transaction description
        :returns: account associated with payee
        """
        accounts = self.config.accounts
        for group in accounts:
            for account, vendors in group.items():
                for vendor in vendors:
                    if vendor in description:
                        return account

    def format_transaction(self, date, payee, debit=0, credit=0):
        """
        Returns a formatted string of the financial transaction.

        :param date: data of transactions
        :Param description: payee of transaction
        :param debit: debit amount of transaction
        :param credit: credit amount of transaction
        :returns: string of the formated transaction
        """
        result = f"{date} * {payee} \n"
        if debit:
            result += f" \t \t {self.categorize_transaction(payee)} \t ${format(debit, '.2f')} \n "
            result += "\t \t Assets:Checking \n"
        elif credit:
            result += f" \t \t Assets:Checking \t ${format(credit, '.2f')} \n "
            result += f"\t \t {self.categorize_transaction(payee)} \n"
        return result.strip()

    def get_totals(self):
        """
        Returns the combined total of all credit and debit transactions
        :returns: string formatted with summed total of all transactions
        """
        result = f"Credit: +${format(self.credit, '.2f')} \n"
        result += f"Debit: -${format(self.debit, '.2f')} \n"
        return result

    # TODO allow for initial date format to be specified
    @staticmethod
    def format_date(date):
        """ Converts date to ledgers default format of '%Y/%m/%d' """
        return datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y/%m/%d")
