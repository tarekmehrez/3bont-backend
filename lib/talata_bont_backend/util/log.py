"""
Containts free methods to init and use logger.
"""
import logging


def init_logger():
    """
    Initialize Logger.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s')


def get_logger():
    """
    Get logger.

    Returns:
        logger object
    """
    logger = logging.getLogger(__name__)
    return logger
