"""
Config helper module.
"""
from talata_bont_backend.config import ConfigReader, ArgParser


def get_config_dict():
    """
    Get config dict.
    """
    argparser = ArgParser()
    args = argparser.crawler_args()

    config_dict = ConfigReader().parse_config(args.config)
    return config_dict
