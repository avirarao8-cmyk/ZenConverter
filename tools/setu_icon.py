"""Build Setu's launcher and splash icons from the source artwork.

Usage: python3 tools/setu_icon.py <source-image>

The launcher icon replaces res/drawable-nodpi/zenconverter.webp and the Android 12
splash icons replace res/drawable-*/zenconverter_launch.png, so the upstream
resource names keep working.
"""
import os
import sys

from PIL import Image

RES = "app/src/main/res"
LAUNCHER_SIZE = 2048
SPLASH_SIZES = [
    ("mdpi", 288),
    ("hdpi", 432),
    ("xhdpi", 576),
    ("xxhdpi", 864),
    ("xxxhdpi", 1152),
]


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else "setu-icon-source.png"
    with Image.open(source) as opened:
        art = opened.convert("RGB")
    print("source:", source, art.size)

    launcher = art.resize((LAUNCHER_SIZE, LAUNCHER_SIZE), Image.LANCZOS)
    launcher_path = os.path.join(RES, "drawable-nodpi", "zenconverter.webp")
    launcher.save(launcher_path, "WEBP", quality=95, method=6)
    print("wrote", launcher_path)

    splash_source = art.convert("RGBA")
    for density, size in SPLASH_SIZES:
        path = os.path.join(RES, f"drawable-{density}", "zenconverter_launch.png")
        splash_source.resize((size, size), Image.LANCZOS).save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
