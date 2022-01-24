from logging import error
from loguru import logger

logger.add('log/SeaBot_WX_{time}.log', rotation='00:00')


def info(Text):
    logger.info(Text)


def success(Text):
    logger.success(Text)


def error(Text):
    logger.error(Text)
