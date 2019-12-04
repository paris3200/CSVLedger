"""
Test the CLI Interface
"""
import os
import pytest
from click.testing import CliRunner
from csvledger import cli


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    exit_status = os.system("csvledger --help")
    assert exit_status == 0
