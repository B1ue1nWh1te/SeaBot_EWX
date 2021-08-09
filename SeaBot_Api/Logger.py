from loguru import logger
import sys


# 日志
def Log(Text):
    logger.info(Text)


# 初始化
try:
    Log("[日志初始化]正在加载配置")
    logger.add('log/SeaBot_Api_{time}.log', rotation='00:00')
    Log("[日志初始化]配置加载完成")

except Exception:
    ExceptionInformation = sys.exc_info()
    Text = "[日志初始化异常]异常信息为:{}".format(ExceptionInformation)
    Log(Text)
    sys.exit(0)
