from loguru import logger

# loging loguru
logger.add(
    "logs/debug.log",
    format="{time} - [{level}] : {message}",
    level="DEBUG",
    rotation="100 KB",
    colorize=True,
)

# logger.debug("Это отладочное сообщение")
# logger.info("Это информационное сообщение")
# logger.success("Операция прошла успешно")
# logger.warning("Предупреждение!")
# logger.error("Произошла ошибка")
# logger.critical("Критическая ошибка!")