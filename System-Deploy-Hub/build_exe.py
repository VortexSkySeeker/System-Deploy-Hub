import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont


def generate_ico(ico_path: str = "app_icon.ico"):
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        (12, 12, size - 12, size - 12),
        radius=56,
        fill="#1F6AA5",
        outline="#3B8ED0",
        width=8,
    )
    try:
        font = ImageFont.truetype("arialbd.ttf", 120)
    except Exception:
        font = ImageFont.load_default()

    text = "SD"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(
        ((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]),
        text,
        fill="#FFFFFF",
        font=font,
    )
    img.save(
        ico_path,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)],
    )


def build():
    ico_file = "app_icon.ico"
    generate_ico(ico_file)
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--clean",
        "--uac-admin",
        "--name",
        "SystemDeployHub",
        "--icon",
        ico_file,
        "--collect-all",
        "customtkinter",
        "system_deploy_hub.py",
    ]
    subprocess.run(cmd, check=True)
    print("EXE successfully built at:", os.path.abspath(os.path.join("dist", "SystemDeployHub.exe")))


if __name__ == "__main__":
    build()
