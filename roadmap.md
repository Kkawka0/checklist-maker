# 🚀 Omnipack IT-Support SuperApp — Full Dev Roadmap

**Projekt:** Interaktywna, autonomiczna checklista IT-Supportowa w środowisku Omnipack, wykorzystująca OCR + lokalne LLM + interaktywny dock GUI.

---

## 🔧 AKTUALNY STAN (MVP - v0.1)

- Nasłuch na klawisz `Insert` → wykonywany screenshot.
- OCR przez `pytesseract` na wykonanym zrzucie.
- Lokalna analiza OCR przez model `qwen:14b` przez `ollama run`.
- Generowanie checklisty z sugestiami IT-Supportowymi (w kontekście pracy w Omnipack).
- Interaktywny dock (PySide6):
  - Przesuwany dock po prawej krawędzi.
  - Lista tasków jako checkboxy.
  - Każdy task posiada mini-notatkę (QTextEdit pod spodem).
  - Checklisty trwale zapisane w `tasks.json`.
- Obsługa `Ctrl+Shift+D` do otwierania/zamykania docka.
- Obsługa pełnego flow przez 1 plik `main.py`.

---

## 🧠 KONTEKST SYSTEMU

> Narzędzie ma wspomagać IT-Supportowca Omnipack w czasie przetwarzania błędów fulfillmentowych, synchronizacji API, analiz logów systemowych, obsługi zleceń w OMS/WMS oraz debugowania zamówień z kanałów takich jak Shopify/Magento.

> System powinien autonomicznie identyfikować możliwe kroki w procesie naprawy, zarządzania SKU, weryfikacji stocków, synchronizacji statusów, obsługi `missingItems`, walidacji mappingów external_number, shipment_number itd.

> Docelowo ma to być **pół-autonomiczny task-manager asystujący operatora IT w codziennej obsłudze systemów Omnipack.**

---

## 🔭 GŁÓWNY CEL DEV

- Cały kod utrzymywany modularnie w `main.py` dopóki projekt nie przekroczy MVP v1.0.
- GUI w pełni interaktywne, odporne na zawieszki LLM/OCR.
- Każdy nowy feature idzie w pełni produkcyjnie stabilny (nie demo-code).
- AI-pomocnik Codex będzie rozwijał funkcje per task.

---

## 🚩 NAJBLIŻSZE FEATURE TASKI (Backlog Devowy)

### 1️⃣ Edycja tasków (Editable Tasks)
- Klikalny przycisk edycji tekstu zadania.
- Zmiany zapisują się w `tasks.json`.

### 2️⃣ Usuwanie tasków (Delete Tasks)
- Dodanie przycisku kasowania taska.
- Natychmiastowy update GUI + `tasks.json`.

### 3️⃣ Diagnostyka OCR (Raw OCR Viewer)
- Podgląd surowego tekstu wyciągniętego z OCR.
- Zakładka `Raw OCR` w GUI docka.

### 4️⃣ Profilowanie projektowe (Multi Profiles)
- Obsługa wielu projektów / klientów.
- Każdy profil ma osobny JSON checklisty + osobny screenshot folder.
- Możliwość przełączania profili w GUI.

### 5️⃣ Historia Screenshotów (Screenshots Manager)
- Lista wykonanych screenshotów.
- Podgląd starego OCR z archiwum.
- Przeglądarka screenshotów w GUI.

### 6️⃣ Zaawansowane logowanie (Error Logging)
- Tworzenie `logs/superapp.log` dla błędów OCR/LLM/systemowych.
- Każda awaria subprocessów logowana wraz z timestampem.

### 7️⃣ Diagnostyka LLM
- Wyświetlanie pełnej odpowiedzi LLM w osobnym oknie "LLM Raw Output".

### 8️⃣ API WebHook Mode (Future)
- Możliwość nasłuchiwania webhooków z systemu fulfillmentowego.
- Screenshot triggerowany przez eventy systemowe, nie tylko Insert.

---

## 🗂️ ARCHITEKTURA SYSTEMU (v1)

- 📂 `main.py` — cały kod GUI + OCR + LLM pipeline.
- 📂 `screenshots/` — automatycznie zapisywane screenshoty.
- 📂 `tasks.json` — trwalsza lista tasków dla GUI.
- 📂 `logs/` — logi błędów i awarii.
- 📂 `profiles/` — katalog dla multi-profile JSON.
- 📂 `README.md` — pełna dokumentacja devowa.
- 📂 `requirements.txt` — pełna specyfikacja pip.

---

## ⚙️ TECHSTACK:

- Python 3.12+
- PySide6 (GUI)
- pyautogui (screenshots)
- Pillow (obrazki)
- pytesseract (OCR)
- keyboard (global hotkeys)
- subprocess (Ollama CLI bridge)
- Ollama (`qwen:14b` model lokalnie)
- Optional: tesseract-OCR native + Ollama preinstalled

---

## 🤖 INSTRUKCJE DLA AI DEVELOPER (Codex Prompt Context)

> You are participating in the development of an internal IT-support assistant for Omnipack. The system processes screenshots via OCR and AI LLM to generate actionable checklists for IT operators. The assistant must be fully interactive, stable, modular, extendable. GUI is dock-style via PySide6. All new code must follow strict coding clarity and stability. Always write production-grade Python, keep modularity, clear variable names, full error-handling, and complete comments.

---

# 🔥 PRZYKŁADOWA SESJA AI DEV

**TASK:** Implement task deletion button for each checklist item.

**CONTEXT:** All code lives inside main.py. Use PySide6 QPushButton inside task wrapper layout. On delete → remove task from self.tasks → refresh GUI → save_tasks(). Clean error handling, update persistence.

---

# 🏁 MASTER PLAN

- ✅ MVP
- 🔄 MVP+
- 🔄 Modular AI Dev Workflow
- 🔄 Codex Co-Pilot full integration
- 🔄 GUI refinement
- 🔄 Deployment-ready package (.exe builder)

