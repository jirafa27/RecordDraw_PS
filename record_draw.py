import logging
import sys
import time
import pywinauto
from pywinauto import Application
from screeninfo import get_monitors
from obswebsocket import obsws, requests
import subprocess
import os

from config import Config


class OBSHandler:
    def __init__(self):
        self.host = Config.HOST
        self.port = Config.PORT
        self.password = Config.PASSWORD
        self.obs_path = Config.OBS_PATH
        self.working_dir = Config.WORKING_DIR
        self.ws = None
        self.current_scene = None
        self.obs_title = "OBS Studio"
        logging.info(f"{self.host},  {self.port}, {self.password}, {self.working_dir}")

    def obs_running(self):
        """
        Проверяет, запущен ли OBS Studio как активное приложение, а не фоновый процесс.
        """
        try:
            result = subprocess.run(["tasklist", "/v"], capture_output=True, text=True)
            lines = result.stdout.split("\n")
            for line in lines:
                if "obs64.exe" in line and "N/A" not in line:
                    logging.info("OBS запущен и активно работает.")
                    return True
            logging.warning("OBS либо не запущен, либо работает в фоновом режиме.")
            return False
        except Exception as e:
            logging.error(f"Ошибка при проверке OBS: {e}")
            return False

    def start_obs(self):
        try:
            if not self.obs_running():
                DETACHED_PROCESS = 0x00000008
                subprocess.Popen(
                    [self.obs_path, "--startuptype=Normal"],
                    cwd=self.working_dir,
                    creationflags=DETACHED_PROCESS,
                )
                logging.info("Запустили OBS Studio.")
            else:
                logging.info("OBS Studio уже запущен")
        except FileNotFoundError as e:
            logging.error(f"Не удалось найти OBS Studio: {e}")
        except Exception as e:
            logging.error(f"Ошибка при запуске OBS Studio: {e}")

    def close_obs_connection(self):
        try:
            self.ws.disconnect()
        except Exception as e:
            logging.error(f"Ошибка при закрытии подключения OBS: {e}")

    def connect_to_obs_scene(self):
        self.ws = obsws(self.host, self.port, self.password)
        self.ws.connect()
        self.current_scene = self.ws.call(requests.GetCurrentProgramScene())
        logging.info(f"Текущая сцена: {self.current_scene}")

    def start_recording(self):
        response = self.ws.call(requests.GetInputList())
        sources = [source["inputName"] for source in response.datain["inputs"]]
        if not "Photoshop Capture" in sources:
            self.ws.call(
                requests.CreateInput(
                    sceneName=self.current_scene.datain["currentProgramSceneName"],
                    inputName="Photoshop Capture",
                    inputKind="window_capture",
                    inputSettings={
                        "method": 2,
                        "priority": 2,
                        "window": "Без имени-1 @ 50% (RGB/8):Photoshop:Photoshop.exe",
                    },
                    sceneItemEnabled=True,
                )
            )

        self.ws.call(requests.StartRecord())
        logging.debug("Запись началась.")

    def stop_recording(self):
        self.ws.call(requests.StopRecord())
        logging.info("Запись остановлена.")


class WindowRecorder:
    def __init__(self):
        self.app = None
        self.process = Config.PHOTOSHOP_PATH
        self.is_recording = False
        self.monitor = get_monitors()[0]
        self.logger = logging.getLogger()
        logging.basicConfig(
            filename="C:\RecordDraw\window_recorder.log",
            level=logging.DEBUG,
            format=f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        )
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        self.obs_handler = OBSHandler()

    def connect_to_obs(self):
        self.obs_handler.connect_to_obs_scene()

    def finding_window(self):
        logging.info("Запуск программы")
        while True:
            try:
                if not self.is_recording:
                    self.app = Application().connect(
                        path=self.process, timeout=1200, retry_interval=5
                    )
                    self.obs_handler.start_obs()
                    self.connect_to_obs()
                    self.start_recording()
                else:
                    self.app = Application().connect(path=self.process, timeout=1)
            except pywinauto.application.ProcessNotFoundError:
                if self.is_recording:
                    self.stop_recording()
                    self.obs_handler.close_obs_connection()
                logging.info("Photoshop закрылся")
                time.sleep(10)
            except Exception as e:
                logging.info(e)
                time.sleep(10)

    def start_recording(self):
        if not self.is_recording:
            logging.info("Начинаем запись экрана...")
            self.obs_handler.start_recording()
            self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            logging.info("Остановка записи экрана...")
            self.obs_handler.stop_recording()
            self.is_recording = False


if __name__ == "__main__":
    log_path = os.path.join("C:", os.sep, "RecordDraw", "window_recorder.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    window_recorder = WindowRecorder()
    window_recorder.finding_window()
