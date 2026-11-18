#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Programmatic newspaper front page: masthead + date, one lead story with a
drawn bridge illustration, and four more stories as full-width rows, each
with a small drawn icon on the right. All text is set with DejaVu fonts;
all artwork is drawn with PIL shapes. No external images, no AI generation.

Layout keeps text and icons in separate columns so nothing overlaps:
text column on the left, icon column on the right of each row.

Run:  python3 draw.py            (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (26, 26, 26)
PAPER = (247, 243, 232)
RED = (178, 34, 34)
STEEL = (70, 90, 110)
GOLD = (176, 141, 44)
SKY = (214, 228, 238)
SEA = (58, 110, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_rule(d, x0, y, x1, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_bridge_icon(d, x, y, w, h):
    """Broken road bridge over water: deck, two towers, gap, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sea
    d.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=SEA)
    for i in range(3):
        yy = y + int(h * 0.78) + i * 12
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(255, 255, 255), width=2)
    # towers rise above the deck only
    tw = 14
    deck_y = y + int(h * 0.42)
    for tx in (x + int(w * 0.22), x + int(w * 0.72)):
        d.rectangle([tx, y + 18, tx + tw, deck_y + 10], fill=INK)
        d.rectangle([tx - 6, y + 12, tx + tw + 6, y + 22], fill=INK)
    # piers under the deck ends, down to the water
    for px in (x + int(w * 0.06), x + int(w * 0.88)):
        d.rectangle([px, deck_y + 10, px + 12, y + int(h * 0.72)], fill=INK)
    # deck: left span and right span, gap in the middle (collapsed span)
    d.rectangle([x, deck_y, x + int(w * 0.44), deck_y + 10], fill=INK)
    d.rectangle([x + int(w * 0.60), deck_y, x + w, deck_y + 10], fill=INK)
    # fallen span in the water, tilted and clearly visible
    d.polygon([(x + int(w * 0.43), y + int(h * 0.80)),
               (x + int(w * 0.62), y + int(h * 0.74)),
               (x + int(w * 0.60), y + int(h * 0.86)),
               (x + int(w * 0.42), y + int(h * 0.92))], fill=(40, 40, 40))
    # cables from tower tops to the deck ends
    d.line([(x + int(w * 0.22) + 7, y + 22), (x + int(w * 0.44), deck_y)],
           fill=INK, width=2)
    d.line([(x + int(w * 0.72) + 7, y + 22), (x + int(w * 0.60), deck_y)],
           fill=INK, width=2)
    # smoke puffs and fire over the gap
    cx, cy = x + int(w * 0.52), deck_y - 30
    d.ellipse([cx - 26, cy - 18, cx + 2, cy + 10], fill=(170, 170, 170))
    d.ellipse([cx - 6, cy - 28, cx + 26, cy + 2], fill=(140, 140, 140))
    d.ellipse([cx - 10, cy - 6, cx + 12, cy + 14], fill=(240, 170, 60))
    d.ellipse([cx - 4, cy - 2, cx + 6, cy + 8], fill=(230, 110, 40))


def draw_radar_icon(d, x, y, w, h):
    """Radar dish with sweeping beam and a small drone."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 226))
    cx, cy = x + int(w * 0.40), y + int(h * 0.58)
    for r in (40, 28, 16):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=STEEL, width=4)
    d.line([(cx - 44, cy), (cx + 44, cy)], fill=STEEL, width=4)
    d.polygon([(cx, cy), (cx + 40, cy - 28), (cx + 40, cy - 4)],
              fill=(200, 60, 40))
    d.line([(cx, cy), (cx, cy + 20)], fill=INK, width=5)
    d.line([(cx - 14, cy + 20), (cx + 14, cy + 20)], fill=INK, width=5)
    # drone top right
    dx, dy = x + int(w * 0.76), y + int(h * 0.24)
    d.rectangle([dx - 13, dy - 5, dx + 13, dy + 5], fill=INK)
    d.ellipse([dx - 20, dy - 10, dx - 6, dy + 2], outline=INK, width=3)
    d.ellipse([dx + 6, dy - 10, dx + 20, dy + 2], outline=INK, width=3)
    d.line([(dx, dy + 5), (dx, dy + 12)], fill=INK, width=3)


def draw_quad_icon(d, x, y, w, h):
    """Four coloured blocks (four nations) over a ship on waves."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cols = [(178, 34, 34), (30, 80, 160), (220, 130, 30), (40, 120, 70)]
    bw, bh, gap = 20, 26, 6
    total = 4 * bw + 3 * gap
    x0 = x + (w - total) // 2
    y0 = y + 8
    for i, c in enumerate(cols):
        d.rectangle([x0 + i * (bw + gap), y0,
                     x0 + i * (bw + gap) + bw, y0 + bh], fill=c)
        d.rectangle([x0 + i * (bw + gap), y0 + bh,
                     x0 + i * (bw + gap) + 5, y0 + bh + 12], fill=INK)
    # ship hull
    hy = y + h - 30
    d.polygon([(x + 16, hy), (x + w - 16, hy), (x + w - 34, hy + 20),
               (x + 34, hy + 20)], fill=INK)
    d.rectangle([x + w // 2 - 3, hy - 24, x + w // 2 + 3, hy], fill=INK)
    d.polygon([(x + w // 2 + 3, hy - 24), (x + w // 2 + 3, hy - 4),
               (x + w // 2 + 28, hy - 4)], fill=RED)
    for i in range(2):
        yy = y + h - 8 + i * 5
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(255, 255, 255), width=2)


def draw_chip_icon(d, x, y, w, h):
    """Microchip with pins and circuit traces."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 228))
    cx, cy = x + w // 2, y + h // 2
    s = 56
    for k in range(4):
        px = x + 20 + k * 24
        d.line([(px, y + 10), (px, cy - s // 2)], fill=INK, width=4)
        d.line([(px, cy + s // 2), (px, y + h - 10)], fill=INK, width=4)
        py = y + 20 + k * 24
        d.line([(x + 10, py), (cx - s // 2, py)], fill=INK, width=4)
        d.line([(cx + s // 2, py), (x + w - 10, py)], fill=INK, width=4)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=INK)
    d.rectangle([cx - s // 2 + 10, cy - s // 2 + 10,
                 cx + s // 2 - 10, cy + s // 2 - 10],
                outline=GOLD, width=3)
    d.text((cx, cy), "AI", font=font(SANS_B, 22), fill=(255, 255, 255),
           anchor="mm")


def draw_cricket_icon(d, x, y, w, h):
    """Cricket bat, ball and stumps on a green strip."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 226))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 150, 80))
    # stumps on the left
    sx = x + 16
    for i in range(3):
        d.rectangle([sx + i * 11, y + h - 62, sx + i * 11 + 6, y + h - 26],
                    fill=(220, 190, 120))
    d.rectangle([sx, y + h - 67, sx + 28, y + h - 62], fill=(220, 190, 120))
    # red ball with seam, mid-left, clear of the bat
    bx, by = x + 58, y + h - 46
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=RED)
    d.arc([bx - 13, by - 13, bx + 13, by + 13], 40, 220,
          fill=(255, 255, 255), width=3)
    # bat upright on the right
    d.rounded_rectangle([x + w - 56, y + 16, x + w - 30, y + 88],
                        radius=7, fill=(205, 164, 110), outline=INK, width=3)
    d.rectangle([x + w - 47, y + 88, x + w - 39, y + 106], fill=INK)


def story_row(d, x, y, w, h, kicker, headline, deck, icon_fn, accent):
    """One full-width story row: left accent bar, text left, icon right."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=(200, 196, 184), width=2)
    d.rectangle([x, y, x + 8, y + h], fill=accent)
    tx = x + 24
    text_w = w - 24 - 150
    ty = y + 12
    d.text((tx, ty), kicker, font=font(SANS_B, 18), fill=accent)
    ty += 28
    hl = font(SERIF_B, 30)
    for line in wrap(d, headline, hl, text_w):
        d.text((tx, ty), line, font=hl, fill=INK)
        ty += 36
    ty += 2
    dk = font(SANS, 20)
    for line in wrap(d, deck, dk, text_w):
        d.text((tx, ty), line, font=dk, fill=(60, 60, 60))
        ty += 26
    icon_fn(d, x + w - 132, y + 8, 116, h - 16)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- masthead ----
    d.text((W // 2, 28), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    draw_rule(d, x0, 106, x1, 3)
    d.text((W // 2, 118), "WEDNESDAY  18  NOVEMBER  2026",
           font=font(SANS_B, 33), fill=RED, anchor="ma")
    d.text((W // 2, 158), "Five stories that defined the day",
           font=font(SERIF, 23), fill=(90, 90, 90), anchor="ma")
    draw_rule(d, x0, 192, x1, 2)

    # ---- lead story: Crimea bridge ----
    ly = 210
    d.text((x0, ly), "WAR IN UKRAINE", font=font(SANS_B, 20), fill=RED)
    ly += 32
    hl = font(SERIF_B, 46)
    for line in wrap(d, "Ukraine smashes the Crimea bridge", hl, 600):
        d.text((x0, ly), line, font=hl, fill=INK)
        ly += 55
    ly += 6
    dk = font(SANS, 22)
    for line in wrap(d, "Road span falls into the sea after a second "
                     "day of strikes; Moscow hits two Kyiv bridges "
                     "in reply.", dk, 600):
        d.text((x0, ly), line, font=dk, fill=(60, 60, 60))
        ly += 30
    draw_bridge_icon(d, x1 - 300, 210, 300, 222)
    draw_rule(d, x0, 452, x1, 2)

    # ---- four story rows ----
    ry, rh, gap = 470, 116, 10
    rw = x1 - x0
    story_row(d, x0, ry, rw, rh,
              "GULF TENSIONS",
              "Iran drones target US radar in Bahrain",
              "Tehran claims a hit; the US says the drones were "
              "stopped. US jets strike a missile site on Qeshm Island.",
              draw_radar_icon, STEEL)
    story_row(d, x0, ry + (rh + gap), rw, rh,
              "INDO-PACIFIC",
              "Quad leaders meet in Manila",
              "Trump, Modi, Albanese and Takaichi launch an AI "
              "accelerator and plan a first joint patrol-aircraft "
              "exercise for 2027.",
              draw_quad_icon, GOLD)
    story_row(d, x0, ry + 2 * (rh + gap), rw, rh,
              "TECH & MARKETS",
              "Nvidia rules out Huang's return",
              "Record revenue of $115.8bn, up 103%, as the board "
              "backs interim chief Colette Kress and hunts for a "
              "new CEO.",
              draw_chip_icon, (40, 120, 70))
    story_row(d, x0, ry + 3 * (rh + gap), rw, rh,
              "SPORT",
              "Dhoni retires from the IPL",
              "India great ends his playing career and will mentor "
              "Chennai Super Kings.",
              draw_cricket_icon, RED)

    # ---- footer ----
    fy = ry + 4 * rh + 3 * gap + 14
    draw_rule(d, x0, fy, x1, 2)
    d.text((W // 2, fy + 12),
           "Reported 18 November 2026  |  Sources: Reuters, CNN, "
           "Nikkei Asia, Al Jazeera, NHK, Indian Express",
           font=font(SANS, 18), fill=(90, 90, 90), anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
