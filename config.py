import logging
import os
import sys

from dotenv import load_dotenv


ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

if ENVIRONMENT == "production":
    dotenv_file = ".env.prod"
else:
    dotenv_file = ".env.dev"


logging.basicConfig(
    filename="C:/RecordDraw/window_recorder.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу, учитывая, что приложение может быть скомпилировано PyInstaller --onefile."""
    try:
        # PyInstaller создаёт временную папку и сохраняет путь в sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Для обычного запуска (не из PyInstaller) возвращаем текущую директорию
        base_path = os.path.abspath(".")

    ans = str(os.path.join(base_path, relative_path))
    logging.info(f"ANS={ans}")
    return ans


env_file_path = resource_path(dotenv_file)
load_dotenv(dotenv_path=env_file_path)


class Config:
    OBS_PATH = os.getenv("OBS_PATH")
    PHOTOSHOP_PATH = os.getenv("PHOTOSHOP_PATH")
    WORKING_DIR = os.getenv("WORKING_DIR")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
