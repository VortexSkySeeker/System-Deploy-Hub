import ctypes
import json
import os
import shutil
import subprocess
import sys
import threading
from datetime import datetime
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SETTINGS_FILE = "hub_settings.json"

APP_META = {
    "Google.Chrome": {"badge": "Ch", "color": "#4285F4", "ru": "Google Chrome", "en": "Google Chrome"},
    "Mozilla.Firefox": {"badge": "Fx", "color": "#FF7139", "ru": "Mozilla Firefox", "en": "Mozilla Firefox"},
    "Brave.Brave": {"badge": "Br", "color": "#FB542B", "ru": "Brave Browser", "en": "Brave Browser"},
    "Yandex.Browser": {"badge": "Ya", "color": "#FC3F1D", "ru": "Yandex Browser", "en": "Yandex Browser"},
    "Telegram.TelegramDesktop": {"badge": "Tg", "color": "#26A5E4", "ru": "Telegram", "en": "Telegram"},
    "Discord.Discord": {"badge": "Ds", "color": "#5865F2", "ru": "Discord", "en": "Discord"},
    "qBittorrent.qBittorrent": {"badge": "qB", "color": "#2F67BA", "ru": "qBittorrent", "en": "qBittorrent"},
    "Microsoft.VisualStudioCode": {"badge": "VS", "color": "#007ACC", "ru": "VS Code", "en": "VS Code"},
    "Git.Git": {"badge": "Gt", "color": "#F05032", "ru": "Git", "en": "Git"},
    "Python.Python.3.12": {"badge": "Py", "color": "#3776AB", "ru": "Python 3.12", "en": "Python 3.12"},
    "OpenJS.NodeJS.LTS": {"badge": "JS", "color": "#339933", "ru": "Node.js (LTS)", "en": "Node.js (LTS)"},
    "Unity.UnityHub": {"badge": "Un", "color": "#4A5568", "ru": "Unity Hub", "en": "Unity Hub"},
    "BlenderFoundation.Blender": {"badge": "Bl", "color": "#E87D0D", "ru": "Blender", "en": "Blender"},
    "JetBrains.IntelliJIDEA.Community": {"badge": "IJ", "color": "#FE315D", "ru": "IntelliJ IDEA Community", "en": "IntelliJ IDEA Community"},
    "Valve.Steam": {"badge": "St", "color": "#1B2838", "ru": "Steam", "en": "Steam"},
    "EpicGames.EpicGamesLauncher": {"badge": "Ep", "color": "#3A3A3A", "ru": "Epic Games Launcher", "en": "Epic Games Launcher"},
    "PrismLauncher.PrismLauncher": {"badge": "Pr", "color": "#4CAF50", "ru": "Prism Launcher (Minecraft)", "en": "Prism Launcher (Minecraft)"},
    "OBSProject.OBSStudio": {"badge": "OB", "color": "#302E31", "ru": "OBS Studio", "en": "OBS Studio"},
    "Bytedance.CapCut": {"badge": "CC", "color": "#00A8E8", "ru": "CapCut", "en": "CapCut"},
    "VideoLAN.VLC": {"badge": "VL", "color": "#FF8800", "ru": "VLC Media Player", "en": "VLC Media Player"},
    "Spotify.Spotify": {"badge": "Sp", "color": "#1DB954", "ru": "Spotify", "en": "Spotify"},
    "Nvidia.NvidiaApp": {"badge": "NV", "color": "#76B900", "ru": "NVIDIA App (Драйверы GPU)", "en": "NVIDIA App (GPU Drivers)"},
    "Microsoft.DirectX": {"badge": "DX", "color": "#107C10", "ru": "DirectX End-User Runtime", "en": "DirectX End-User Runtime"},
    "Microsoft.VCRedist.2015+.x64": {"badge": "C+", "color": "#68217A", "ru": "VC++ Redistributable (x64)", "en": "VC++ Redistributable (x64)"},
    "Microsoft.VCRedist.2015+.x86": {"badge": "C+", "color": "#8E44AD", "ru": "VC++ Redistributable (x86)", "en": "VC++ Redistributable (x86)"},
    "Microsoft.DotNet.DesktopRuntime.8": {"badge": ".N", "color": "#512BD4", "ru": ".NET Desktop Runtime 8", "en": ".NET Desktop Runtime 8"},
    "7zip.7zip": {"badge": "7z", "color": "#005499", "ru": "7-Zip", "en": "7-Zip"},
    "Microsoft.PowerToys": {"badge": "PT", "color": "#0078D4", "ru": "PowerToys", "en": "PowerToys"},
    "voidtools.Everything": {"badge": "Ev", "color": "#F7941D", "ru": "Everything (Быстрый поиск)", "en": "Everything (Fast Search)"},
}

CATEGORIES = {
    "browsers": {
        "ru": "🌐 Браузеры и Сеть",
        "en": "🌐 Browsers & Network",
        "apps": [
            "Google.Chrome",
            "Mozilla.Firefox",
            "Brave.Brave",
            "Yandex.Browser",
            "Telegram.TelegramDesktop",
            "Discord.Discord",
            "qBittorrent.qBittorrent",
        ],
    },
    "dev": {
        "ru": "💻 Разработка и 3D",
        "en": "💻 Dev & 3D",
        "apps": [
            "Microsoft.VisualStudioCode",
            "Git.Git",
            "Python.Python.3.12",
            "OpenJS.NodeJS.LTS",
            "Unity.UnityHub",
            "BlenderFoundation.Blender",
            "JetBrains.IntelliJIDEA.Community",
        ],
    },
    "gaming": {
        "ru": "🎮 Гейминг и Медиа",
        "en": "🎮 Gaming & Media",
        "apps": [
            "Valve.Steam",
            "EpicGames.EpicGamesLauncher",
            "PrismLauncher.PrismLauncher",
            "OBSProject.OBSStudio",
            "Bytedance.CapCut",
            "VideoLAN.VLC",
            "Spotify.Spotify",
        ],
    },
    "system": {
        "ru": "⚙️ Драйверы и Система",
        "en": "⚙️ Drivers & System",
        "apps": [
            "Nvidia.NvidiaApp",
            "Microsoft.DirectX",
            "Microsoft.VCRedist.2015+.x64",
            "Microsoft.VCRedist.2015+.x86",
            "Microsoft.DotNet.DesktopRuntime.8",
            "7zip.7zip",
            "Microsoft.PowerToys",
            "voidtools.Everything",
        ],
    },
}

PRESETS = {
    "basic": {
        "ru": "📦 Базовый ПК",
        "en": "📦 Basic PC",
        "apps": [
            "Google.Chrome",
            "Telegram.TelegramDesktop",
            "7zip.7zip",
            "VideoLAN.VLC",
            "voidtools.Everything",
            "Microsoft.VCRedist.2015+.x64",
        ],
    },
    "gaming": {
        "ru": "🎮 Гейминг",
        "en": "🎮 Gaming",
        "apps": [
            "Valve.Steam",
            "EpicGames.EpicGamesLauncher",
            "Discord.Discord",
            "OBSProject.OBSStudio",
            "Nvidia.NvidiaApp",
            "Microsoft.DirectX",
            "Microsoft.VCRedist.2015+.x64",
            "Microsoft.VCRedist.2015+.x86",
        ],
    },
    "dev": {
        "ru": "🛠️ Разработчик",
        "en": "🛠️ Developer",
        "apps": [
            "Microsoft.VisualStudioCode",
            "Git.Git",
            "Python.Python.3.12",
            "OpenJS.NodeJS.LTS",
            "Microsoft.PowerToys",
            "7zip.7zip",
            "voidtools.Everything",
        ],
    },
}

TRANSLATIONS = {
    "ru": {
        "window_title": "System Deploy Hub // Автоустановщик",
        "subtitle": "Выбери нужные компоненты или готовый пресет для пакетной установки через Winget",
        "admin_ok": "🛡️ Администратор",
        "admin_warn": "⚠️ Обычный режим (возможны запросы UAC)",
        "presets_label": "Пресеты:",
        "search_placeholder": "🔍 Поиск по названию или Winget ID...",
        "status_ready": "Готово к работе",
        "btn_select_tab": "☑️ Выбрать вкладку",
        "btn_clear": "🧹 Сбросить",
        "btn_export": "💾 Профиль",
        "btn_import": "📂 Загрузить",
        "btn_settings": "⚙️ Настройки",
        "btn_stop": "⏹ Стоп",
        "btn_install": "🚀 УСТАНОВИТЬ ВЫБРАННОЕ ({count})",
        "btn_installing": "⏳ Идет установка...",
        "log_ready": "[Система готова] Отметь галочками нужный софт и нажми кнопку установки.",
        "log_winget_missing": "[ВНИМАНИЕ] Утилита 'winget' не найдена в PATH. Установи 'App Installer' из Microsoft Store.",
        "log_admin_tip": "[Совет] Для установки без лишних окон UAC запускай программу от имени Администратора.",
        "log_preset_applied": "[Пресет] Применён набор: {name}",
        "log_nothing_selected": "[!] Ничего не выбрано для установки.",
        "log_winget_err": "[ОШИБКА] Winget не найден в системе. Установка невозможна.",
        "log_cancel_req": "[!] Запрошена остановка. Ожидание завершения текущего пакета...",
        "log_cancelled": "⏹ Установка прервана пользователем.",
        "log_start_batch": "=== Начинаю установку ({total} шт.) ===",
        "log_installing_item": "---> [{idx}/{total}] Скачивание и установка: {name} ({app_id})...",
        "log_ok": "[OK] {name} успешно установлен!",
        "log_already": "[ИНФО] {name} уже установлен (обновление не требуется).",
        "log_status_code": "[Статус {code}] {name}: возможно, уже установлен или требует перезагрузки.",
        "log_error": "[ОШИБКА] {name}: {err}",
        "log_done": "=== 🎉 ЗАВЕРШЕНО! Успешно обработано: {ok} из {total} ===",
        "progress_installing": "Установка [{idx}/{total}]: {name}",
        "export_empty": "[!] Не выбрано ни одной программы для сохранения профиля.",
        "export_title": "Сохранить профиль установки",
        "export_ok": "[Профиль] Сохранено пакетов: {count} -> {file}",
        "export_err": "[ОШИБКА] Не удалось сохранить профиль: {err}",
        "import_title": "Загрузить профиль установки",
        "import_ok": "[Профиль] Загружено пакетов: {count} из {file}",
        "import_err": "[ОШИБКА] Не удалось загрузить профиль: {err}",
        "settings_title": "Настройки // Settings",
        "settings_header": "⚙️ Настройки приложения",
        "settings_lang": "Язык интерфейса (Language):",
        "settings_theme": "Тема оформления:",
        "settings_silent": "Тихая установка (--silent)",
        "settings_clear_log": "🗑️ Очистить консоль логов",
        "settings_close": "Готово",
        "theme_dark": "Тёмная (Dark)",
        "theme_light": "Светлая (Light)",
        "theme_system": "Системная (System)",
        "log_cleared": "[Консоль очищена]",
    },
    "en": {
        "window_title": "System Deploy Hub // Batch Installer",
        "subtitle": "Select software components or choose a preset for batch installation via Winget",
        "admin_ok": "🛡️ Administrator",
        "admin_warn": "⚠️ Standard Mode (UAC prompts may appear)",
        "presets_label": "Presets:",
        "search_placeholder": "🔍 Search by name or Winget ID...",
        "status_ready": "Ready",
        "btn_select_tab": "☑️ Select Tab",
        "btn_clear": "🧹 Clear",
        "btn_export": "💾 Save Profile",
        "btn_import": "📂 Load Profile",
        "btn_settings": "⚙️ Settings",
        "btn_stop": "⏹ Stop",
        "btn_install": "🚀 INSTALL SELECTED ({count})",
        "btn_installing": "⏳ Installing...",
        "log_ready": "[System Ready] Check the desired software and click the install button.",
        "log_winget_missing": "[WARNING] 'winget' utility not found in PATH. Please install 'App Installer' from Microsoft Store.",
        "log_admin_tip": "[Tip] Run as Administrator to avoid multiple UAC prompts during installation.",
        "log_preset_applied": "[Preset] Applied preset: {name}",
        "log_nothing_selected": "[!] No packages selected for installation.",
        "log_winget_err": "[ERROR] Winget was not found on this system. Installation aborted.",
        "log_cancel_req": "[!] Stop requested. Waiting for the current package to finish...",
        "log_cancelled": "⏹ Installation cancelled by user.",
        "log_start_batch": "=== Starting batch installation ({total} packages) ===",
        "log_installing_item": "---> [{idx}/{total}] Downloading & installing: {name} ({app_id})...",
        "log_ok": "[OK] {name} installed successfully!",
        "log_already": "[INFO] {name} is already installed (no update required).",
        "log_status_code": "[Status {code}] {name}: may already be installed or requires a reboot.",
        "log_error": "[ERROR] {name}: {err}",
        "log_done": "=== 🎉 COMPLETED! Successfully processed: {ok} of {total} ===",
        "progress_installing": "Installing [{idx}/{total}]: {name}",
        "export_empty": "[!] Select at least one package to save a profile.",
        "export_title": "Save Installation Profile",
        "export_ok": "[Profile] Saved {count} packages -> {file}",
        "export_err": "[ERROR] Failed to save profile: {err}",
        "import_title": "Load Installation Profile",
        "import_ok": "[Profile] Loaded {count} packages from {file}",
        "import_err": "[ERROR] Failed to load profile: {err}",
        "settings_title": "Settings // Настройки",
        "settings_header": "⚙️ Application Settings",
        "settings_lang": "Interface Language (Язык):",
        "settings_theme": "Appearance Mode:",
        "settings_silent": "Silent installation (--silent)",
        "settings_clear_log": "🗑️ Clear Log Console",
        "settings_close": "Done",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "theme_system": "System",
        "log_cleared": "[Console cleared]",
    },
}

WINGET_ALREADY_INSTALLED_CODES = {
    -1978335189,
    2316632107,
    -1978335135,
    2316632161,
}


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def create_badge_icon(text: str, bg_color: str, size: int = 28) -> ctk.CTkImage:
    scale = 2
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (2, 2, canvas_size - 3, canvas_size - 3),
        radius=12,
        fill=bg_color,
        outline="#FFFFFF33",
        width=2,
    )
    try:
        font = ImageFont.truetype("arialbd.ttf", int(canvas_size * 0.42))
    except Exception:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", int(canvas_size * 0.42))
        except Exception:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (canvas_size - w) / 2 - bbox[0]
    y = (canvas_size - h) / 2 - bbox[1]
    draw.text((x, y), text, fill="#FFFFFF", font=font)
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=final_img, dark_image=final_img, size=(size, size))


class InstallerHub(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.lang = "ru"
        self.theme_mode = "dark"
        self.silent_mode = True
        self._load_settings()

        ctk.set_appearance_mode(self.theme_mode)
        self.geometry("880x720")
        self.minsize(780, 640)

        self.checkboxes: dict[str, dict] = {}
        self.preset_buttons: dict[str, ctk.CTkButton] = {}
        self.icon_cache: dict[str, ctk.CTkImage] = {}
        self.active_category_key = "browsers"
        self.is_installing = False
        self.cancel_requested = False
        self.settings_window = None

        self._build_ui()
        self.apply_language()
        self._check_environment()

    def _load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("lang") in ("ru", "en"):
                    self.lang = data["lang"]
                if data.get("theme") in ("dark", "light", "system"):
                    self.theme_mode = data["theme"]
                if isinstance(data.get("silent"), bool):
                    self.silent_mode = data["silent"]
            except Exception:
                pass

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "lang": self.lang,
                        "theme": self.theme_mode,
                        "silent": self.silent_mode,
                    },
                    f,
                    indent=2,
                )
        except Exception:
            pass

    def tr(self, key: str, **kwargs) -> str:
        template = TRANSLATIONS[self.lang].get(key, key)
        return template.format(**kwargs) if kwargs else template

    def _build_ui(self):
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 4))

        self.header = ctk.CTkLabel(
            top_frame,
            text="⚡ SYSTEM DEPLOY HUB",
            font=("Consolas", 24, "bold"),
            text_color="#3b8ed0",
        )
        self.header.pack(side="left")

        right_top = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_top.pack(side="right")

        self.lang_switch = ctk.CTkSegmentedButton(
            right_top,
            values=["RU", "EN"],
            width=84,
            height=28,
            command=self._on_quick_lang_switch,
        )
        self.lang_switch.set(self.lang.upper())
        self.lang_switch.pack(side="right", padx=(10, 0))

        self.settings_btn = ctk.CTkButton(
            right_top,
            text="⚙️ Настройки",
            width=120,
            height=28,
            fg_color="#333333",
            hover_color="#444444",
            command=self.open_settings,
        )
        self.settings_btn.pack(side="right", padx=(10, 0))

        self.admin_badge = ctk.CTkLabel(
            right_top,
            text="",
            font=("Arial", 12, "bold"),
        )
        self.admin_badge.pack(side="right", pady=4)

        self.sub = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 12),
            text_color="gray",
        )
        self.sub.pack(anchor="w", padx=20, pady=(0, 8))

        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=(0, 6))

        self.presets_label = ctk.CTkLabel(
            filter_frame, text="", font=("Arial", 12, "bold")
        )
        self.presets_label.pack(side="left", padx=(0, 6))

        for preset_key in PRESETS:
            btn = ctk.CTkButton(
                filter_frame,
                text="",
                width=125,
                height=28,
                fg_color="#2b5797",
                hover_color="#1e3f6f",
                command=lambda k=preset_key: self.apply_preset(k),
            )
            btn.pack(side="left", padx=4)
            self.preset_buttons[preset_key] = btn

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        self.search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            width=260,
            height=28,
        )
        self.search_entry.pack(side="right")

        self.cat_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.cat_bar.pack(fill="x", padx=20, pady=(4, 2))
        self.cat_buttons: dict[str, ctk.CTkButton] = {}
        for cat_key in CATEGORIES:
            cbtn = ctk.CTkButton(
                self.cat_bar,
                text="",
                height=34,
                corner_radius=8,
                font=("Arial", 13, "bold"),
                command=lambda k=cat_key: self.switch_category(k),
            )
            cbtn.pack(side="left", fill="x", expand=True, padx=4)
            self.cat_buttons[cat_key] = cbtn

        self.cards_container = ctk.CTkFrame(self, corner_radius=10)
        self.cards_container.pack(padx=20, pady=6, fill="both", expand=True)

        self.category_frames: dict[str, ctk.CTkScrollableFrame] = {}
        for cat_key, cat_data in CATEGORIES.items():
            sframe = ctk.CTkScrollableFrame(
                self.cards_container, fg_color="transparent"
            )
            sframe.grid_columnconfigure(0, weight=1)
            sframe.grid_columnconfigure(1, weight=1)
            self.category_frames[cat_key] = sframe

            for i, app_id in enumerate(cat_data["apps"]):
                meta = APP_META[app_id]
                var = ctk.BooleanVar(value=False)
                var.trace_add("write", lambda *_: self._update_selection_counter())

                row_card = ctk.CTkFrame(
                    sframe,
                    corner_radius=8,
                    fg_color=("#EBEBEB", "#1F242D"),
                )
                row_card.grid(
                    row=i // 2,
                    column=i % 2,
                    padx=8,
                    pady=6,
                    sticky="ew",
                )

                icon_img = create_badge_icon(meta["badge"], meta["color"], size=28)
                self.icon_cache[app_id] = icon_img

                icon_lbl = ctk.CTkLabel(
                    row_card,
                    text="",
                    image=icon_img,
                    width=32,
                )
                icon_lbl.pack(side="left", padx=(10, 6), pady=8)

                cb = ctk.CTkCheckBox(
                    row_card,
                    text="",
                    variable=var,
                    font=("Arial", 13),
                    checkbox_width=20,
                    checkbox_height=20,
                )
                cb.pack(side="left", padx=4, pady=8, fill="x", expand=True)

                status_lbl = ctk.CTkLabel(
                    row_card,
                    text="📥",
                    font=("Segoe UI Emoji", 14),
                    width=28,
                )
                status_lbl.pack(side="right", padx=(4, 10))

                self.checkboxes[app_id] = {
                    "var": var,
                    "cb": cb,
                    "status": status_lbl,
                    "card": row_card,
                    "category": cat_key,
                }

        self.switch_category("browsers")

        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=(4, 0))

        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="",
            font=("Arial", 12),
            text_color="gray",
        )
        self.progress_label.pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=320)
        self.progress_bar.pack(side="right", pady=4)
        self.progress_bar.set(0)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=8)

        self.select_all_btn = ctk.CTkButton(
            self.btn_frame,
            text="",
            command=self.select_current_tab,
            width=145,
            fg_color="#444",
            hover_color="#555",
        )
        self.select_all_btn.pack(side="left", padx=(0, 5))

        self.clear_btn = ctk.CTkButton(
            self.btn_frame,
            text="",
            command=self.clear_selection,
            width=105,
            fg_color="#444",
            hover_color="#555",
        )
        self.clear_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(
            self.btn_frame,
            text="",
            command=self.export_profile,
            width=110,
            fg_color="#444",
            hover_color="#555",
        )
        self.export_btn.pack(side="left", padx=5)

        self.import_btn = ctk.CTkButton(
            self.btn_frame,
            text="",
            command=self.import_profile,
            width=115,
            fg_color="#444",
            hover_color="#555",
        )
        self.import_btn.pack(side="left", padx=5)

        self.cancel_btn = ctk.CTkButton(
            self.btn_frame,
            text="",
            command=self.request_cancel,
            width=85,
            fg_color="#dc3545",
            hover_color="#b02a37",
            state="disabled",
        )
        self.cancel_btn.pack(side="right", padx=(5, 0))

        self.install_btn = ctk.CTkButton(
            self.btn_frame,
            text="",
            font=("Arial", 14, "bold"),
            fg_color="#28a745",
            hover_color="#218838",
            command=self.start_installation,
        )
        self.install_btn.pack(side="right", padx=5, fill="x", expand=True)

        self.log_box = ctk.CTkTextbox(
            self,
            height=135,
            font=("Consolas", 12),
            fg_color="#111111",
            text_color="#00ff00",
            state="disabled",
        )
        self.log_box.pack(padx=20, pady=(0, 15), fill="x")

    def switch_category(self, cat_key: str):
        self.active_category_key = cat_key
        for k, frame in self.category_frames.items():
            frame.pack_forget()
        self.category_frames[cat_key].pack(fill="both", expand=True, padx=6, pady=6)
        for k, btn in self.cat_buttons.items():
            if k == cat_key:
                btn.configure(fg_color="#1f6aa5", hover_color="#144870")
            else:
                btn.configure(fg_color=("#D0D5DD", "#2B2B2B"), hover_color=("#B8C0CC", "#3A3A3A"))

    def _on_quick_lang_switch(self, value: str):
        new_lang = value.lower()
        if new_lang in ("ru", "en") and new_lang != self.lang:
            self.lang = new_lang
            self._save_settings()
            self.apply_language()

    def apply_language(self):
        self.title(self.tr("window_title"))
        self.sub.configure(text=self.tr("subtitle"))
        self.admin_badge.configure(
            text=self.tr("admin_ok") if is_admin() else self.tr("admin_warn"),
            text_color="#28a745" if is_admin() else "#e0a800",
        )
        self.settings_btn.configure(text=self.tr("btn_settings"))
        self.presets_label.configure(text=self.tr("presets_label"))
        self.search_entry.configure(placeholder_text=self.tr("search_placeholder"))

        for preset_key, btn in self.preset_buttons.items():
            btn.configure(text=PRESETS[preset_key][self.lang])

        for cat_key, btn in self.cat_buttons.items():
            btn.configure(text=CATEGORIES[cat_key][self.lang])

        for app_id, item in self.checkboxes.items():
            app_name = APP_META[app_id][self.lang]
            item["cb"].configure(text=f"{app_name}  [{app_id}]")

        if not self.is_installing:
            self.progress_label.configure(text=self.tr("status_ready"))

        self.select_all_btn.configure(text=self.tr("btn_select_tab"))
        self.clear_btn.configure(text=self.tr("btn_clear"))
        self.export_btn.configure(text=self.tr("btn_export"))
        self.import_btn.configure(text=self.tr("btn_import"))
        self.cancel_btn.configure(text=self.tr("btn_stop"))
        self._update_selection_counter()

    def open_settings(self):
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.focus()
            return

        win = ctk.CTkToplevel(self)
        win.title(self.tr("settings_title"))
        win.geometry("420x340")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        self.settings_window = win

        title_lbl = ctk.CTkLabel(
            win,
            text=self.tr("settings_header"),
            font=("Arial", 18, "bold"),
        )
        title_lbl.pack(pady=(18, 12))

        lang_frame = ctk.CTkFrame(win, fg_color="transparent")
        lang_frame.pack(fill="x", padx=24, pady=6)
        lang_lbl = ctk.CTkLabel(lang_frame, text=self.tr("settings_lang"), font=("Arial", 13))
        lang_lbl.pack(side="left")

        lang_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=["Русский (RU)", "English (EN)"],
            width=150,
        )
        lang_menu.set("Русский (RU)" if self.lang == "ru" else "English (EN)")
        lang_menu.pack(side="right")

        theme_frame = ctk.CTkFrame(win, fg_color="transparent")
        theme_frame.pack(fill="x", padx=24, pady=6)
        theme_lbl = ctk.CTkLabel(theme_frame, text=self.tr("settings_theme"), font=("Arial", 13))
        theme_lbl.pack(side="left")

        theme_map_forward = {
            "dark": self.tr("theme_dark"),
            "light": self.tr("theme_light"),
            "system": self.tr("theme_system"),
        }
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=[
                self.tr("theme_dark"),
                self.tr("theme_light"),
                self.tr("theme_system"),
            ],
            width=150,
        )
        theme_menu.set(theme_map_forward.get(self.theme_mode, self.tr("theme_dark")))
        theme_menu.pack(side="right")

        silent_var = ctk.BooleanVar(value=self.silent_mode)
        silent_switch = ctk.CTkSwitch(
            win,
            text=self.tr("settings_silent"),
            variable=silent_var,
            font=("Arial", 13),
        )
        silent_switch.pack(anchor="w", padx=24, pady=(12, 8))

        clear_log_btn = ctk.CTkButton(
            win,
            text=self.tr("settings_clear_log"),
            fg_color="#444",
            hover_color="#555",
            command=self.clear_log,
        )
        clear_log_btn.pack(fill="x", padx=24, pady=(6, 12))

        def apply_and_close():
            chosen_lang = "ru" if "RU" in lang_menu.get() else "en"
            chosen_theme_label = theme_menu.get()
            if "Light" in chosen_theme_label or "Светлая" in chosen_theme_label:
                self.theme_mode = "light"
            elif "System" in chosen_theme_label or "Системная" in chosen_theme_label:
                self.theme_mode = "system"
            else:
                self.theme_mode = "dark"

            self.lang = chosen_lang
            self.silent_mode = bool(silent_var.get())
            self.lang_switch.set(self.lang.upper())
            ctk.set_appearance_mode(self.theme_mode)
            self._save_settings()
            self.apply_language()
            win.destroy()

        close_btn = ctk.CTkButton(
            win,
            text=self.tr("settings_close"),
            fg_color="#28a745",
            hover_color="#218838",
            font=("Arial", 13, "bold"),
            command=apply_and_close,
        )
        close_btn.pack(fill="x", padx=24, pady=(4, 15))

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.log(self.tr("log_cleared"))

    def _check_environment(self):
        self.log(self.tr("log_ready"))
        if shutil.which("winget") is None:
            self.log(self.tr("log_winget_missing"))
        if not is_admin() and sys.platform == "win32":
            self.log(self.tr("log_admin_tip"))

    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}\n"
        self.after(0, self._append_log, formatted)

    def _append_log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _update_selection_counter(self):
        if self.is_installing:
            return
        count = sum(1 for item in self.checkboxes.values() if item["var"].get())
        self.install_btn.configure(text=self.tr("btn_install", count=count))

    def _on_search_change(self, *_):
        query = self.search_var.get().strip().lower()
        for app_id, item in self.checkboxes.items():
            name_ru = APP_META[app_id]["ru"].lower()
            name_en = APP_META[app_id]["en"].lower()
            if not query or query in name_ru or query in name_en or query in app_id.lower():
                item["cb"].configure(text_color=("#111111", "#DCE4EE"))
            else:
                item["cb"].configure(text_color="gray40")

    def apply_preset(self, preset_key: str):
        if self.is_installing:
            return
        self.clear_selection()
        preset_data = PRESETS.get(preset_key, {})
        for app_id in preset_data.get("apps", []):
            if app_id in self.checkboxes:
                self.checkboxes[app_id]["var"].set(True)
        self.log(self.tr("log_preset_applied", name=preset_data.get(self.lang, preset_key)))

    def select_current_tab(self):
        if self.is_installing:
            return
        for app_id in CATEGORIES[self.active_category_key]["apps"]:
            self.checkboxes[app_id]["var"].set(True)

    def clear_selection(self):
        if self.is_installing:
            return
        for item in self.checkboxes.values():
            item["var"].set(False)
            item["status"].configure(text="📥")

    def export_profile(self):
        selected_ids = [
            app_id for app_id, item in self.checkboxes.items() if item["var"].get()
        ]
        if not selected_ids:
            self.log(self.tr("export_empty"))
            return
        file_path = filedialog.asksaveasfilename(
            title=self.tr("export_title"),
            defaultextension=".json",
            filetypes=[("JSON Profile", "*.json")],
            initialfile="deploy_profile.json",
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({"packages": selected_ids}, f, ensure_ascii=False, indent=2)
                self.log(
                    self.tr(
                        "export_ok",
                        count=len(selected_ids),
                        file=os.path.basename(file_path),
                    )
                )
            except Exception as e:
                self.log(self.tr("export_err", err=e))

    def import_profile(self):
        if self.is_installing:
            return
        file_path = filedialog.askopenfilename(
            title=self.tr("import_title"),
            filetypes=[("JSON Profile", "*.json")],
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                target_ids = set(data.get("packages", []))
                self.clear_selection()
                matched = 0
                for app_id, item in self.checkboxes.items():
                    if app_id in target_ids:
                        item["var"].set(True)
                        matched += 1
                self.log(
                    self.tr(
                        "import_ok",
                        count=matched,
                        file=os.path.basename(file_path),
                    )
                )
            except Exception as e:
                self.log(self.tr("import_err", err=e))

    def request_cancel(self):
        if self.is_installing:
            self.cancel_requested = True
            self.cancel_btn.configure(state="disabled")
            self.log(self.tr("log_cancel_req"))

    def start_installation(self):
        if self.is_installing:
            return

        selected = [
            (APP_META[app_id][self.lang], app_id)
            for app_id, item in self.checkboxes.items()
            if item["var"].get()
        ]
        if not selected:
            self.log(self.tr("log_nothing_selected"))
            return

        if shutil.which("winget") is None:
            self.log(self.tr("log_winget_err"))
            return

        self.is_installing = True
        self.cancel_requested = False
        self.install_btn.configure(state="disabled", text=self.tr("btn_installing"))
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)

        threading.Thread(
            target=self.install_worker, args=(selected,), daemon=True
        ).start()

    def _set_item_status(self, app_id: str, icon: str):
        if app_id in self.checkboxes:
            self.after(0, lambda: self.checkboxes[app_id]["status"].configure(text=icon))

    def install_worker(self, selected: list[tuple[str, str]]):
        total = len(selected)
        self.log(self.tr("log_start_batch", total=total))
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        success_count = 0
        for idx, (name, app_id) in enumerate(selected, start=1):
            if self.cancel_requested:
                self.log(self.tr("log_cancelled"))
                break

            self._set_item_status(app_id, "⏳")
            self.after(
                0,
                lambda i=idx, t=total, n=name: self.progress_label.configure(
                    text=self.tr("progress_installing", idx=i, total=t, name=n)
                ),
            )
            self.log(self.tr("log_installing_item", idx=idx, total=total, name=name, app_id=app_id))

            cmd = [
                "winget",
                "install",
                "--id",
                app_id,
                "-e",
                "--accept-package-agreements",
                "--accept-source-agreements",
            ]
            if self.silent_mode:
                cmd.append("--silent")

            try:
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    creationflags=creation_flags,
                )
                if process.returncode == 0:
                    self.log(self.tr("log_ok", name=name))
                    self._set_item_status(app_id, "✅")
                    success_count += 1
                elif process.returncode in WINGET_ALREADY_INSTALLED_CODES:
                    self.log(self.tr("log_already", name=name))
                    self._set_item_status(app_id, "✅")
                    success_count += 1
                else:
                    self.log(
                        self.tr("log_status_code", code=process.returncode, name=name)
                    )
                    self._set_item_status(app_id, "⚠️")
            except Exception as e:
                self.log(self.tr("log_error", name=name, err=e))
                self._set_item_status(app_id, "❌")

            progress = idx / total
            self.after(0, lambda p=progress: self.progress_bar.set(p))

        self.log(self.tr("log_done", ok=success_count, total=total))
        self.after(0, self._finish_installation)

    def _finish_installation(self):
        self.is_installing = False
        self.cancel_requested = False
        self.cancel_btn.configure(state="disabled")
        self.progress_label.configure(text=self.tr("status_ready"))
        self._update_selection_counter()
        self.install_btn.configure(state="normal")


if __name__ == "__main__":
    app = InstallerHub()
    app.mainloop()