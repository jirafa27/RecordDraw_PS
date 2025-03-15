# RecordDraw_PS

Этот проект предназначен для автоматической записи экрана, когда запущен **Adobe Photoshop**.  
Приложение использует **OBS Studio** для захвата видео и управляет его работой через WebSocket API.

---

## Основные возможности

- **Автоматический запуск OBS Studio**, если он не запущен.
- **Проверка активного окна Photoshop**.
- **Автоматическое начало и остановка записи** при запуске и закрытии Photoshop.
- **Создание источника захвата окна Photoshop** в OBS Studio.

---

## Требования

Перед запуском убедитесь, что установлены следующие зависимости:

### Программы:

- [OBS Studio](https://obsproject.com/)
- **Adobe Photoshop**

### Python зависимости:

- **Python 3.8+**
- `pywinauto`
- `screeninfo`
- `obs-websocket-py`
- `pyinstaller` (для сборки в исполняемый файл)

Установите их с помощью:

```sh
pip install -r requirements.txt 
```
### Клонирование репозитория
```sh
git clone https://github.com/your-repo/window-recorder.git
cd window-recorder
```

### Настройка OBS-Studio и файл конфигурации
Требуется в проекте создать файл .dev.env и прописать там следующие параметры (задать свои)
Password, Host и PORT следует найти в настройках OBS Websocket
```sh
OBS_PATH=C:\Program Files\obs-studio\bin\64bit\obs64.exe
PHOTOSHOP_PATH=C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe
WORKING_DIR=C:\Program Files\obs-studio\data\obs-studio
PASSWORD=password
HOST=localhost
PORT=4455
```

### Для компиляции в exe следует выполнит команду

```sh
pyinstaller --onefile --noconsole window_recorder.py
```

По необходимости можно добавить exe в планировщик задач Windows с запуском каждый раз при запуске системы

