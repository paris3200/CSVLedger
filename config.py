""" Provides the configuration for the CSVledger module. """
from configparser import ConfigParser
import os
import sys
import errno
import json


class Config:
    """
    Reads the default configuration from config file.  If file doesn't exist
    then it is created.

    :param config_file: Location of config file
    """

    def __init__(self, config_file=None):

        xdg_config = os.environ.get("XDG_CONFIG_HOME")

        if not config_file:
            if not xdg_config:
                config_file = "~/.config/csvledger/config"
            else:
                config_file = xdg_config + "/csvledger/config"

        # Get the absolute file path
        self.config_file = os.path.expanduser(config_file)
        if not os.path.isfile(self.config_file):
            raise Exception("Config file not found")

        self.parse_config()

    def parse_config(self):
        """ Reads the config file and imports settings. """
        with open(self.config_file) as config:
            self.accounts = json.load(config)

    def create_dir(self):
        """ Creates defaults directory if it doesn't exist. """
        directory = os.path.expanduser(os.path.dirname(self.config_file))
        try:
            os.makedirs(directory)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(directory):
                pass
            else:
                raise
