"""Run: python3 src/logo.py   (then python3 src/assets.py, then python3 src/build.py)
Rebuild the transparent logo from the original PNG.
- white background removed, letters fully opaque, soft drop shadow removed
- tagline removed, wordmark scaled to the icon's full height
- recoloured to the site's headline blue/green (light) and the dark-mode tints
"""
from PIL import Image

import os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'brand', 'logo-original.png')
PUB = os.path.join(HERE, '..', 'public')
os.chdir(PUB)  # writes logo.png / logo-dark.png into public/
LO, HI = 0.55, 0.85          # alpha remap: below LO -> gone (shadow), above HI -> solid


def build(blue, green, out_name):
    src = Image.open(SRC).convert('RGBA')
    W, H = src.size
    px = src.load()
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    po = out.load()
    for y in range(H):
        for x in range(W):
            r, g, b, a0 = px[x, y]
            a = max(255 - r, 255 - g, 255 - b) / 255.0
            if a0 < 255:
                a = min(a, a0 / 255)
            if a < 0.02:
                continue
            c = [min(255, max(0, round((v - 255 * (1 - a)) / a))) for v in (r, g, b)]
            grey = max(c) - min(c) < 30
            if grey and y > 100 and x > 100:      # tagline
                continue
            if grey:                               # (R) mark: thin strokes, keep them
                a2 = max(0.0, min(1.0, (a - 0.12) / 0.4))
            else:
                a2 = max(0.0, min(1.0, (a - LO) / (HI - LO)))
            if a2 <= 0:
                continue
            if grey:                               # the (R) mark -> green
                col = green
            else:
                col = blue if c[2] > c[1] else green
            po[x, y] = (*col, round(a2 * 255))
    out = out.crop(out.getbbox())
    # split icon / wordmark at the first empty column gap
    W, H = out.size
    al = out.split()[3].load()
    cols = [any(al[x, y] > 20 for y in range(H)) for x in range(W)]
    x = cols.index(True)
    while cols[x]:
        x += 1
    gs = x
    while not cols[x]:
        x += 1
    icon = out.crop((0, 0, gs, H))
    icon = icon.crop(icon.getbbox())
    text = out.crop((x, 0, W, H))
    text = text.crop(text.getbbox())
    h = icon.height
    text = text.resize((round(text.width * h / text.height), h), Image.LANCZOS)
    gap = round(h * 0.12)
    final = Image.new('RGBA', (icon.width + gap + text.width, h), (0, 0, 0, 0))
    final.paste(icon, (0, 0), icon)
    final.paste(text, (icon.width + gap, 0), text)
    final.quantize(colors=48, method=Image.FASTOCTREE, dither=Image.Dither.NONE).save(out_name, optimize=True)
    return final.size


print(build((11, 106, 168), (20, 121, 42), 'logo.png'))
print(build((111, 200, 255), (95, 214, 119), 'logo-dark.png'))
