from loguru import logger

logger.add('log/SeaBot_EWX_{time}.log', rotation='00:00')


def success(Text: str) -> None:
    logger.success(Text)


def error(Text: str) -> None:
    logger.error(Text)


def info(Text: str) -> None:
    logger.info(Text)


def warning(Text: str) -> None:
    logger.warning(Text)
