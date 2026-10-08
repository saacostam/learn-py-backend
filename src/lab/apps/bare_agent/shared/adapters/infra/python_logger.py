import logging


class PythonLogger:
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)
