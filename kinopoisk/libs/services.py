from loguru import logger


def get_popular_actor_from_file(actor_file):
    with open(actor_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

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