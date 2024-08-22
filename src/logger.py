import logging
from src.config import load_config


class Logger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


_loggers = {}


def get_logger(name=None):
    config = load_config()
    if name is None:
        name = __name__

    if name not in _loggers:
        level = logging.getLevelName(config.get('log_level', 'INFO'))
        _loggers[name] = Logger(name, level=level)

    return _loggers[name]