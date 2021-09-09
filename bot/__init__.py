import logging
from logging import handlers
from pathlib import Path


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging_file = Path("logs", f"bot.log")
logging_file.parent.mkdir(exist_ok=True)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

file_handler = handlers.RotatingFileHandler(logging_file, maxBytes=5242880, backupCount=3, encoding="utf8")
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logging.getLogger("lightbulb").setLevel(logging.INFO)
logging.getLogger("hikari").setLevel(logging.INFO)
