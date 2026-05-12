import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Create logger per file/module name.
    Example:
        logger = get_logger(__name__)
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    file_name = name.split(".")[-1]
    print(file_name)
    log_file_path = os.path.join(LOG_DIR, f"{file_name}.log")
    file_handler = RotatingFileHandler(log_file_path,maxBytes=5 * 1024 * 1024,  backupCount=5)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(filename)s | %(levelname)s | %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger