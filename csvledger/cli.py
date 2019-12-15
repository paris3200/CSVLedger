from .csvledger import CSVledger
import csv
import click


@click.command()
@click.option(
    "--config", type=click.Path(exists=True, readable=True), help="path to config file",
)
@click.option("--profile", default="default", help="profile settings to use")
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
def cli(csvfile, check, config, total, convert, profile):
    """
    CSVledger taks the input of a CSV file of financial transactions, strips excessive
    data from the transactions and then converts the transactions to ledger-cli
    format.
    """

    convertor = CSVledger(config, profile)

    if total:
        convertor.convert_file(csvfile)
        print(convertor.get_totals())
    else:
        print(convertor.convert_file(csvfile))
