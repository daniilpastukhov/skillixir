import logging


def get_logger(name: str) -> logging.Logger:
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	logger.propagate = False
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch = logging.StreamHandler()
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	return logger
