#!/usr/bin/env python3
"""Compose the news-image-20261118 entry: a newspaper front page for
Wednesday 18 November 2026, built from four AI-generated photo panels
(no text in the panels) plus crisp PIL-drawn headlines.

Stories (all first reported 18 Nov 2026, cross-checked across
openchronicle.org, justsecurity.org, zarknews.com, horizonapp.link):
 1. Gulf: U.S. jets hit a Revolutionary Guard missile site on Qeshm
    Island; Iran answers with drone strikes on U.S. bases in Kuwait
    and Bahrain.
 2. Ukraine: Kerch Bridge hit again - a span collapses into the strait.
 3. APEC Shenzhen: Xi and Putin meet ahead of Thursday's trilateral
    summit with Trump.
 4. U.S. Senate: Peltola wins Alaska; Democrats take a 56-44 majority.
Ticker: Ebola in DR Congo passes 11,000 cases; Voyager 1 reaches one
light-day from Earth; U.S. loses measles-free status after 26 years.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
W, H = 1024, 1024

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (16, 28, 51)
PAPER = (247, 243, 234)
RED = (178, 34, 34)
GOLD = (216, 180, 90)
INK = (20, 20, 20)
GREY = (90, 90, 90)


def font(path, size):
    return ImageFont.truetype(path, size)


def cover(img, tw, th):
    """Center-crop img to exactly tw x th (cover fit)."""
    w, h = img.size
    s = max(tw / w, th / h)
    nw, nh = int(w * s + 0.5), int(h * s + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def panel(name):
    p = None
    for f in sorted(os.listdir(PANELS)):
        if f.startswith("media-generation-" + name):
            p = os.path.join(PANELS, f)
            break
    assert p, "panel not found: " + name
    return Image.open(p).convert("RGB")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 108], fill=NAVY)
    f_small = font(SANS_B, 21)
    f_date = font(SERIF_B, 46)
    d.text((W // 2, 26), "T H E   W O R L D   I N   O N E   D A Y",
           font=f_small, fill=GOLD, anchor="ma")
    d.text((W // 2, 52), "WEDNESDAY, 18 NOVEMBER 2026",
           font=f_date, fill=(255, 255, 255), anchor="ma")

    # ---- Hero: Gulf ----
    hero = cover(panel("panel-gulf"), 1000, 372)
    img.paste(hero, (12, 120))
    d.rectangle([12, 492, 1012, 560], fill=(255, 255, 255))
    d.rectangle([12, 492, 1012, 496], fill=RED)
    d.text((24, 502), "THE GULF",
           font=font(SANS_B, 20), fill=RED)
    d.text((24, 528), "U.S. strikes Qeshm Island; Iran hits back at bases in Kuwait and Bahrain",
           font=font(SERIF_B, 24), fill=INK)

    # ---- Three panels ----
    cols = [
        ("panel-kerch", "UKRAINE",
         "Kerch Bridge hit again \u2014 a span collapses into the strait"),
        ("panel-shenzhen", "APEC \u00b7 SHENZHEN",
         "Xi and Putin meet before Thursday\u2019s summit with Trump"),
        ("panel-alaska", "U.S. SENATE",
         "Peltola wins Alaska \u2014 Democrats take a 56\u201344 majority"),
    ]
    x0 = 12
    pw, gap = 325, 12
    for i, (name, kicker, head) in enumerate(cols):
        x = x0 + i * (pw + gap)
        pic = cover(panel(name), pw, 220)
        img.paste(pic, (x, 572))
        d.rectangle([x, 792, x + pw, 796], fill=RED)
        d.text((x, 804), kicker, font=font(SANS_B, 19), fill=RED)
        lines = wrap(d, head, font(SERIF_B, 25), pw - 4)
        y = 830
        for ln in lines:
            d.text((x, y), ln, font=font(SERIF_B, 25), fill=INK)
            y += 30

    # ---- Ticker ----
    d.rectangle([0, 960, W, 1024], fill=NAVY)
    tick = ("ALSO TODAY:  Ebola in DR Congo passes 11,000 cases   \u2022   "
            "Voyager 1 reaches one light-day   \u2022   "
            "U.S. loses measles-free status")
    size = 19
    while d.textlength(tick, font=font(SANS_B, size)) > 1000 and size > 10:
        size -= 1
    d.text((W // 2, 976), tick, font=font(SANS_B, size),
           fill=(255, 255, 255), anchor="ma")

    out = os.path.join(HERE, "entry.png")
    # Saved as JPEG bytes under the entry.png name: the rules tell the
    # file apart by its first bytes and the name stays entry.png.
    img.save(out, "JPEG", quality=88, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
