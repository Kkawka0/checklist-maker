# === main.py ===
"""
SuperApp — Omnipack IT-Support Screenshot→OCR→LLM Checklist
===========================================================

· Insert  → screenshot, OCR, Qwen-14B prompt, new checklist tasks
· Ctrl+Shift+D → toggle dock visibility

"""

import os
import subprocess
import datetime
import json
import threading
from pathlib import Path

import keyboard
import pyautogui
from PIL import Image
import pytesseract
from PySide6 import QtWidgets, QtCore, QtGui

# CONFIG
BASE_DIR = Path(__file__).parent
SCREENSHOT_DIR = BASE_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)
TASKS_FILE = BASE_DIR / "tasks.json"
OLLAMA_MODEL = "qwen:14b"
OLLAMA_TIMEOUT = 120
GUI_HOTKEY = "ctrl+shift+d"

def call_ollama(prompt: str) -> str:
    try:
        proc = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode(), capture_output=True, timeout=OLLAMA_TIMEOUT, check=True
        )
        return proc.stdout.decode()
    except subprocess.TimeoutExpired:
        return "[LLM TIMEOUT]"
    except subprocess.CalledProcessError as err:
        return f"[LLM ERROR] {err.stderr.decode()}"

def parse_tasks(text: str):
    tasks = []
    for line in text.splitlines():
        stripped = line.lstrip(" •-\t")
        if stripped and stripped[0].isalpha():
            tasks.append(stripped.strip())
    return tasks

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

class DockWindow(QtWidgets.QWidget):
    WIDTH = 340

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IT-Support Checklist")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setFixedWidth(self.WIDTH)
        geo = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(geo.width() - self.WIDTH, 0, self.WIDTH, geo.height())

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout(self.container)
        self.vbox.setAlignment(QtCore.Qt.AlignTop)
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

        self.tasks = load_tasks()
        self.refresh()

    def refresh(self):
        while self.vbox.count():
            child = self.vbox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for t in self.tasks:
            self._add_task_widget(t)

    def _add_task_widget(self, task):
        cb = QtWidgets.QCheckBox(task["text"])
        cb.setChecked(task.get("done", False))
        cb.stateChanged.connect(self.persist)
        note = QtWidgets.QTextEdit(task.get("note", ""))
        note.setPlaceholderText("Notes …")
        note.setFixedHeight(56)
        note.textChanged.connect(self.persist)
        wrapper = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(wrapper)
        v.setContentsMargins(0, 0, 0, 0)
        v.addWidget(cb)
        v.addWidget(note)
        task["_cb"], task["_note"] = cb, note
        self.vbox.addWidget(wrapper)

    def persist(self):
        for t in self.tasks:
            t["done"] = t["_cb"].isChecked()
            t["note"] = t["_note"].toPlainText()
        save_tasks(self.tasks)

    def add_new_tasks(self, texts):
        existing = {t["text"] for t in self.tasks}
        for txt in texts:
            if txt not in existing:
                self.tasks.append({"text": txt, "done": False, "note": ""})
        self.refresh()
        save_tasks(self.tasks)

def pipeline(dock: DockWindow):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = SCREENSHOT_DIR / f"ss_{ts}.png"
    img = pyautogui.screenshot()
    img.save(fn)

    ui_text = pytesseract.image_to_string(Image.open(fn))
    prompt = (
        "You are an Omnipack IT-Support assistant. Based on the UI text below, "
        "produce 3-6 concise checklist items describing next actions.\n\nUI_TEXT:\n"
        + ui_text
        + "\n\nChecklist:"
    )
    llm_out = call_ollama(prompt)
    tasks = parse_tasks(llm_out)

    QtCore.QMetaObject.invokeMethod(
        dock, lambda t=tasks: dock.add_new_tasks(t), QtCore.Qt.QueuedConnection
    )

def main():
    app = QtWidgets.QApplication([])
    dock = DockWindow()
    dock.hide()

    keyboard.add_hotkey(GUI_HOTKEY, lambda: dock.setVisible(not dock.isVisible()))
    keyboard.add_hotkey("insert", lambda: threading.Thread(target=pipeline, args=(dock,), daemon=True).start())

    app.exec()

if __name__ == "__main__":
    main()
