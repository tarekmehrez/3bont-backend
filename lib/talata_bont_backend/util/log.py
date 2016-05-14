import logging

def init_logger():
	logging.basicConfig(level=logging.DEBUG,format='%(asctime)s : %(levelname)s : %(message)s')

def get_logger():
	logger = logging.getLogger(__name__)
	return logger
