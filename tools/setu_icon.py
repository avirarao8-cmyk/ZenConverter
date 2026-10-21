"""Generate the Setu Neo-Vedic emblem (golden lotus + yantra on deep indigo).

Writes the launcher icon and the Android 12 splash icons straight into the
app resource folders, overwriting the upstream ZenConverter artwork.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

INDIGO_TOP = (26, 26, 61)
INDIGO_BOT = (10, 10, 30)
GOLD = (232, 163, 61)
GOLD_LIGHT = (246, 205, 116)
TEAL = (58, 168, 168)

RES = "app/src/main/res"


def radial_bg(size):
    img = Image.new("RGB", (size, size), INDIGO_BOT)
    px = img.load()
    cx = cy = size / 2
    maxd = math.hypot(cx, cy)
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - cx, y - cy) / maxd
            t = min(1.0, d * 1.15)
            px[x, y] = (
                int(INDIGO_TOP[0] * (1 - t) + INDIGO_BOT[0] * t),
                int(INDIGO_TOP[1] * (1 - t) + INDIGO_BOT[1] * t),
                int(INDIGO_TOP[2] * (1 - t) + INDIGO_BOT[2] * t),
            )
    return img


def petal_layer(size, ring_r, petal_len, petal_w, color):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = size / 2
    pcy = cy - ring_r
    d.ellipse(
        [cx - petal_w / 2, pcy - petal_len, cx + petal_w / 2, pcy + petal_len],
        fill=color,
    )
    return layer


def make_emblem(size, petals=8, with_ring=True):
    S = 2048 if size <= 2048 else size
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    R = S * 0.285
    petal_len = S * 0.140
    petal_w = S * 0.112

    base = petal_layer(S, R, petal_len, petal_w, GOLD + (255,))
    for i in range(petals):
        img = Image.alpha_composite(
            img, base.rotate(-i * (360 / petals), resample=Image.BICUBIC, center=(S / 2, S / 2))
        )

    base2 = petal_layer(S, R * 0.55, petal_len * 0.72, petal_w * 0.82, GOLD_LIGHT + (255,))
    for i in range(petals):
        img = Image.alpha_composite(
            img,
            base2.rotate(
                -i * (360 / petals) - (180 / petals), resample=Image.BICUBIC, center=(S / 2, S / 2)
            ),
        )

    d = ImageDraw.Draw(img)
    if with_ring:
        rr = S * 0.478
        d.ellipse([S / 2 - rr, S / 2 - rr, S / 2 + rr, S / 2 + rr], outline=GOLD + (255,), width=int(S * 0.012))
        rr2 = S * 0.438
        d.ellipse([S / 2 - rr2, S / 2 - rr2, S / 2 + rr2, S / 2 + rr2], outline=TEAL + (150,), width=int(S * 0.006))

    cd = S * 0.135
    d.ellipse([S / 2 - cd, S / 2 - cd, S / 2 + cd, S / 2 + cd], fill=INDIGO_BOT + (255,), outline=GOLD + (255,), width=int(S * 0.012))
    bd = S * 0.045
    d.ellipse([S / 2 - bd, S / 2 - bd, S / 2 + bd, S / 2 + bd], fill=GOLD_LIGHT + (255,))

    glow = img.filter(ImageFilter.GaussianBlur(S * 0.02))
    img = Image.alpha_composite(glow, img)
    return img.resize((size, size), Image.LANCZOS)


def make_app_icon(size, emblem):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(radial_bg(size), (0, 0))
    scaled = emblem.resize((int(size * 0.94),) * 2, Image.LANCZOS)
    off = (size - scaled.size[0]) // 2
    canvas.alpha_composite(scaled, (off, off))
    return canvas.convert("RGB")


def main():
    emblem = make_emblem(2048)
    icon_path = os.path.join(RES, "drawable-nodpi", "zenconverter.webp")
    make_app_icon(2048, emblem).save(icon_path, "WEBP", quality=92, method=6)
    print("wrote", icon_path)

    for density, size in [("mdpi", 288), ("hdpi", 432), ("xhdpi", 576), ("xxhdpi", 864), ("xxxhdpi", 1152)]:
        path = os.path.join(RES, f"drawable-{density}", "zenconverter_launch.png")
        emblem.resize((size, size), Image.LANCZOS).save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
