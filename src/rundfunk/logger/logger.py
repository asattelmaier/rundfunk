import logging


class Logger:
    def __init__(self, context: str):
        self._context = context

    @staticmethod
    def setup(log_level: str = None) -> None:
        if log_level is None:
            return

        if log_level.upper() == logging.getLevelName(logging.DEBUG):
            logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)

    def debug(self, message: str) -> None:
        logging.debug('%s::%s', self._context, message)
