"""
Test the CLI Interface
"""
import os
from click.testing import CliRunner
from csvledger.csvledger import cli


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system("csvledger --help")
    assert exit_status == 0


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
    assert "2019/08/26 * PAY CHECK\n" in result.output
    assert "\t \t Assets:Checking \t $1200.00" in result.output
    assert "\t \t Income \n\n" in result.output
