import datetime
import os
import logging
from app.common.variables import variables

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    log_level = variables.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    log_dir = variables.LOG_PATH
    os.makedirs(log_dir, exist_ok=True)

    current_ts = datetime.datetime.now().strftime("%Y-%m-%d")

    log_path = os.path.join(variables.LOG_PATH, f"LOG_{current_ts}.log")

    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_path)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        )
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    return logger