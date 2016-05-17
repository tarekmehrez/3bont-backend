"""
Contains the ConfigReader class as part of the config package.
"""
import configparser


class ConfigReader(object):

    """
    Ini config file parser.
    """

    def parse_config(self, config_file):
        """
        Parse ini config file.

        Args:
            config_file (str)

        Returns:
            dict: parsed arguments
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        return config
