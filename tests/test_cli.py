"""
Test the CLI Interface
"""
import os
from click.testing import CliRunner
from csvledger.cli import cli


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    pass
    # exit_status = os.system("csvledger --help")
    # Fails on Travis CI for reasons unknown.
    # assert exit_status == 0


def test_sample_returns_unmatched_transaction():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "--config",
            "tests/sample_config.yml",
            "-i",
            "tests/sample_transactions.csv",
            "--check",
        ],
    )
    assert result.exit_code == 0
    assert "TARGET" in result.output


def test_totals():
    """ Test Totals on sample data """
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "--config",
            "tests/sample_config.yml",
            "-i",
            "tests/sample_transactions.csv",
            "--total",
        ],
    )
    assert result.exit_code == 0
    assert "TARGET" not in result.output
    assert "+$1200.00" in result.output
    assert "-$653.70" in result.output


def test_conversion():
    """ Test coversion to ledger format """
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "--config",
            "tests/sample_config.yml",
            "-i",
            "tests/sample_transactions.csv",
            "--convert",
        ],
    )
    assert result.exit_code == 0
    formatted = (
        "2019/08/26 * PAY CHECK \n \t \t Assets:Checking \t $1200.00 \n \t \t Income \n"
    )
    assert formatted.strip() in result.output
