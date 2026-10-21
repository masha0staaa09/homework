import json
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json_file(file_path: str) -> list[dict]:
    """Читает JSON-файл и возвращает список словарей."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            logger.info("JSON-файл успешно прочитан")
            return data

        logger.warning("Содержимое JSON-файла не является списком")
        return []

    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("Не удалось прочитать JSON: некорректный формат")
        return []
