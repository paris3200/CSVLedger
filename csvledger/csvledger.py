import csv
import datetime
import re

from .config import Config


class CSVledger:
    """
    CSVledger taks the input of a CSV file of financial transactions, strips excessive
    data from the transactions and then converts the transactions to ledger-cli
    format.

    Parameters
    ----------
    config_file: str
        File path of config file.
    """

    def __init__(self, config_file=None, profile="default"):
        self.config = Config(config_file, profile)
        self.credit = 0
        self.debit = 0

    def convert_file(self, csvfile=None, check=False):
        """
        Parameters
        ----------
        csvfile: str
            File path of csv file to processed.
        check: Boolean
            Check for unmatched transactions.

        Returns
        -------
        str
            converted transactions
        """
        result = ""
        with open(csvfile, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

            if self.config.profile["header"]:
                next(csv_reader)

            for row in csv_reader:
                credit = None
                debit = None
                description = self.filter_description(
                    row[self.config.profile["description"]]
                )

                date = self.format_date(row[self.config.profile["date"]])

                try:
                    credit = float(row[self.config.profile["credit"]])
                except ValueError:
                    pass
                else:
                    self.credit += credit

                try:
                    debit = float(row[self.config.profile["debit"]])
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

        Parameters
        ----------
        description: str
            The description to be filtered

        Returns
        -------
        str
            The filtered description.
        """
        result = description
        if self.config.filter:
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

        Parameters
        -----------
        description: str
                Transaction description

        Returns
        --------
        str or None
            Account Category associated with description if found.
        """
        accounts = self.config.accounts
        for group in accounts:
            for account, vendors in group.items():
                for vendor in vendors:
                    if vendor in description:
                        return account

    def format_transaction(self, date, payee, debit=0, credit=0):
        """
        Formats transaction into the ledger format.


        Parameters
        -----------
        date: str
            date of transactions
        description: str
            payee of transaction
        debit: float
            debit amount of transaction
        credit: float
            credit amount of transaction


        Returns
        --------
        str
            Formatted transaction
        """
        result = f"{date} * {payee}\n"
        if debit:
            result += (
                f"\t\t{self.categorize_transaction(payee)}\t${format(debit, '.2f')}\n"
            )
            result += f"\t\t{self.config.profile['account']}\n\n"
        elif credit:
            result += (
                f"\t\t{self.config.profile['account']}\t${format(credit, '.2f')}\n"
            )
            result += f"\t\t{self.categorize_transaction(payee)}\n\n"
        return result

    def get_totals(self):
        """
        Returns the combined total of all credit and debit transactions.

        Returns
        -----------
        str
            formatted with summed total of all transactions
        """
        result = f"Credit: +${format(self.credit, '.2f')} \n"
        result += f"Debit: -${format(self.debit, '.2f')} \n"
        return result

    # TODO allow for initial date format to be specified
    @staticmethod
    def format_date(date):
        """
        Converts date from %m/%d/%Y to ledgers default format of '%Y/%m/%d'

        Parameters
        --------
        date: str
            Date in %m/%d/%Y (12/15/2019)

        Returns
        -------
        str
            Date formated to '%Y/%m/%d' (2019/12/15)
        """

        return datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y/%m/%d")
