""" Provides the configuration for the CSVledger module. """
import errno
import json
import os

import yaml


class Config:
    """
    Reads the configuration from config file.

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
            data = yaml.load(config, Loader=yaml.FullLoader)
            self.accounts = data["accounts"]
            self.filter = data["filter"]
