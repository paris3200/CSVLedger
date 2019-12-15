"""
Test the Config Class
"""
from csvledger.config import Config


def test_profile_set():
    config = Config("tests/sample_config.yml", profile="default")
    assert config.profile["header"] is True
