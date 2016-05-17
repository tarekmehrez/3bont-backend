"""
Contains the ArgParser class as part of the config package.
"""
import argparse


class ArgParser(object):

    """
    CLI for the entire package.
    """

    def __init__(self):
        """
        Init argparser.
        """
        self._parser = argparse.ArgumentParser()

    def crawler_args(self):
        """
        Main Crawler args.
        """
        self._parser.add_argument('--config',
                                  action='store',
                                  dest='config',
                                  help='Path to .ini config file',
                                  required=True)

        args = self._parser.parse_args()
        return args
