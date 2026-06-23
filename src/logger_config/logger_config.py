import logging
import time
from pathlib import Path

START_TIME = time.time()

# paths
BASE_DIR=Path(__file__).resolve().parent.parent.parent
LOG_DIR=BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE=LOG_DIR / "astraRAG.log"

class ElapsedFormatter(logging.Formatter):
    def format(self,record):
        record.elapsed_sec = round(time.time() - START_TIME , 2)
        return super().format(record)                   # super().format(record) calls the original logging.Formatter.format().

def setup_logger():
    root_logger=logging.getLogger()
    if root_logger.handlers:
        return root_logger

    root_logger.setLevel(logging.INFO)

    formatter=ElapsedFormatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(elapsed_sec)s | %(message)s"
    )

    # console logs
    console_handler= logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler=logging.FileHandler(filename=LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return root_logger