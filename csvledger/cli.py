from .csvledger import CSVledger
import csv
import click


@click.command()
@click.option(
    "--config", type=click.Path(exists=True, readable=True), help="path to config file",
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
    "--total", is_flag=True, help="prints sum of all credit and debit transactions",
)
@click.option(
    "--convert", is_flag=True, help="prints transactions in ledger format",
)
def cli(csvfile, check, config, total, convert):
    """
    CSVledger taks the input of a CSV file of financial transactions, strips excessive
    data from the transactions and then converts the transactions to ledger-cli
    format.
    """

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
                    convertor.print_transaction(date, description, debit, credit)
            elif convert:
                convertor.print_transaction(date, description, debit, credit)
        if total:
            convertor.print_total(total_credit, total_debit)
