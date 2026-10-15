[English](./README.md) · **Русский**

# ⚡ System Deploy Hub

### Пакетный автоустановщик программ для Windows на базе Winget и CustomTkinter.

Выбирай нужные программы или готовый пресет, чтобы развернуть рабочее или игровое окружение в пару кликов.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![Winget](https://img.shields.io/badge/Winget-Package_Manager-0078D4?style=flat-square&logo=windows&logoColor=white) ![UI](https://img.shields.io/badge/UI-CustomTkinter-3B8ED0?style=flat-square) ![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-E0A800?style=flat-square)

**Быстрый старт** · **Возможности** · **Сборка EXE** · **Структура проекта**

---

## Возможности

* **🎨 Иконки и живые статусы**: у каждой программы отображается фирменный значок и индикатор статуса установки в реальном времени (`📥` в очереди, `⏳` установка, `✅` установлено, `⚠️` требует внимания, `❌` ошибка).  
* **🌐 Два языка интерфейса (RU / EN)**: мгновенное переключение между русским и английским языками через переключатель `RU | EN` в шапке или окно **⚙️ Настройки** с сохранением в `hub_settings.json`.  
* **⚡ Готовые пресеты и быстрый поиск**: применяй готовые наборы (**Базовый ПК**, **Гейминг**, **Разработчик**) одним кликом или фильтруй каталог по названию и `Winget ID`.  
* **💾 Экспорт и импорт профилей**: сохраняй свой список программ в `.json` и загружай его на любом другом ПК.  
* **🛡️ Потокобезопасность и UAC**: установка выполняется в фоновом потоке без зависания окна, с проверкой прав Администратора и корректной обработкой кодов возврата `winget`.

---

## Быстрый старт

1. Установи зависимости:  
     
   pip install \-r requirements.txt  
     
2. Запусти приложение (рекомендуется от имени Администратора, чтобы избежать лишних запросов UAC):  
     
   python system\_deploy\_hub.py

---

## Сборка EXE

### Вариант 1: Локальная сборка на Windows в 1 клик

Запусти файл `build_exe.bat` или выполни команду:

python build\_exe.py

Скрипт автоматически сгенерирует иконку `app_icon.ico`, упакует тему `CustomTkinter` и соберёт автономный файл **`dist/SystemDeployHub.exe`** со встроенным манифестом прав Администратора (`--uac-admin`).

### Вариант 2: Автоматическая сборка через GitHub Actions

В репозиторий включён workflow `.github/workflows/build_exe.yml`. При каждом `push` в ветку `main` или `master` сервер GitHub автоматически компилирует `SystemDeployHub.exe` и прикрепляет готовый файл в разделе **Actions → Artifacts**.

---

## Структура проекта

* `system_deploy_hub.py` — основной код приложения с генерацией иконок, живыми статусами и настройками RU/EN  
* `build_exe.py` — скрипт генерации `.ico` и упаковки `SystemDeployHub.exe` через `PyInstaller`  
* `build_exe.bat` — пакетный файл для сборки `.exe` на Windows в один клик  
* `requirements.txt` — зависимости проекта (`customtkinter`, `Pillow`, `pyinstaller`)  
* `README.md` / `README.ru.md` — документация на английском и русском языках с переключателем в шапке  
* `.github/workflows/build_exe.yml` — конфигурация автосборки Windows `.exe` на GitHub Actions