"""Article figures for 'Six Problems, One First Cut' (Analytics Decoded).
Every value is read from first_cut.py (seed 2026), so the images and the
printed numbers cannot disagree. Run: python figures.py
"""
import contextlib
import io
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

with contextlib.redirect_stdout(io.StringIO()):
    import first_cut as fc  # runs the simulations quietly

FONTS = "/usr/share/fonts/truetype/google-fonts/"
PAPER, INK, GREEN = "#F7F5F0", "#1F2421", "#1A6A58"
GREY, RULE, TINT = "#6B6F6C", "#D9D5CC", "#DCEAE5"
OUT = "figures"
os.makedirs(OUT, exist_ok=True)


def font(name, size):
    files = {"bold": "Poppins-Bold.ttf", "medium": "Poppins-Medium.ttf",
             "light": "Poppins-Light.ttf", "regular": "Poppins-Regular.ttf",
             "lora": "Lora-Variable.ttf", "lora_i": "Lora-Italic-Variable.ttf"}
    return ImageFont.truetype(FONTS + files[name], size)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, width):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def header(d, W, title, subtitle, m):
    d.text((m, m), title, font=font("bold", 64), fill=INK)
    d.text((m, m + 92), subtitle, font=font("lora_i", 38), fill=GREY)


def footer(d, W, H, m):
    d.line([(m, H - m - 40), (W - m, H - m - 40)], fill=RULE, width=2)
    d.text((m, H - m - 22), "Simulated data, NumPy seed 2026. Image by the author.",
           font=font("light", 26), fill=GREY)
    s = "Analytics Decoded"
    d.text((W - m - text_w(d, s, font("medium", 26)), H - m - 22), s,
           font=font("medium", 26), fill=GREEN)


# ------------------------------------------------ Figure 1: the six first cuts
def six_cuts():
    W, H, m = 2000, 1400, 90
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d, W, "Six problems, six first cuts",
           "One number per problem, computed before any model", m)

    cards = [
        ("Healthcare", f"{fc.share_by_90:.1%}",
         "of first-year stoppers stop by day 90",
         f"{len(fc.pts):,} patients"),
        ("Banking", f"{fc.recall:.1%}",
         "of fraud caught by one rule",
         f"{len(fc.tx):,} payments, {fc.base_rate:.3%} fraud"),
        ("Technology", f"+{fc.diff * 100:.2f} pts",
         "measured; the true lift was 0.6 pts",
         f"{fc.n_arm:,} users per group"),
        ("E-commerce", f"{fc.top20_share:.1%}",
         "of revenue from the top 20% of buyers",
         f"{len(fc.cust):,} customers, one year"),
        ("Consumer goods", f"{-fc.dip / fc.bump:.1%}",
         "of the promotion spike given back later",
         f"{len(fc.promo_weeks)} promotions in {fc.weeks} weeks"),
        ("Government", f"{fc.conc:.1%}",
         "of lost money sits in 10% of blocks",
         f"{len(fc.gov)} blocks, {fc.overall:.1%} leakage overall"),
    ]
    cols, gap = 3, 40
    top = m + 190
    cw = (W - 2 * m - (cols - 1) * gap) // cols
    ch = (H - top - m - 90 - gap) // 2
    for i, (sector, num, concept, scale) in enumerate(cards):
        x = m + (i % cols) * (cw + gap)
        y = top + (i // cols) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill="#FFFFFF",
                            outline=RULE, width=2)
        d.rectangle([x, y + 18, x + 8, y + ch - 18], fill=GREEN)
        p = x + 44
        d.text((p, y + 36), sector, font=font("medium", 34), fill=GREEN)
        d.text((p, y + 92), num, font=font("bold", 104), fill=INK)
        for k, line in enumerate(wrap(d, concept, font("lora", 34), cw - 88)):
            d.text((p, y + 244 + k * 46), line, font=font("lora", 34), fill=INK)
        d.line([(p, y + ch - 78), (x + cw - 44, y + ch - 78)], fill=RULE, width=2)
        d.text((p, y + ch - 62), scale, font=font("light", 27), fill=GREY)
    footer(d, W, H, m)
    img.save(f"{OUT}/fig1_six_first_cuts.png", optimize=True)


# ------------------------------------------------ Figure 2: persistence curve
def persistence():
    W, H, m = 2000, 1250, 90
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d, W, "Most stopping happens in the first 90 days",
           f"Share of {len(fc.pts):,} simulated patients still refilling, "
           "by days since starting", m)

    x0, x1 = m + 120, W - m - 40
    y0, y1 = m + 230, H - m - 170          # plot top and bottom
    X = lambda day: x0 + (x1 - x0) * day / 365
    Y = lambda share: y1 - (y1 - y0) * share

    # first-90-days band
    d.rectangle([X(0), y0, X(90), y1], fill=TINT)
    d.text((X(4) + 12, y1 - 56), "First 90 days", font=font("medium", 30),
           fill=GREEN)

    # grid and axes
    for s in (0, 0.25, 0.5, 0.75, 1.0):
        d.line([(x0, Y(s)), (x1, Y(s))], fill=RULE, width=2)
        lab = f"{s:.0%}"
        d.text((x0 - 24 - text_w(d, lab, font("light", 28)), Y(s) - 18), lab,
               font=font("light", 28), fill=GREY)
    for day in (0, 90, 180, 270, 365):
        lab = str(day)
        d.text((X(day) - text_w(d, lab, font("light", 28)) / 2, y1 + 16), lab,
               font=font("light", 28), fill=GREY)
    lab = "Days since starting the medicine"
    d.text(((x0 + x1) / 2 - text_w(d, lab, font("regular", 28)) / 2, y1 + 62),
           lab, font=font("regular", 28), fill=GREY)

    # the curve, read from the data one day at a time
    days = np.arange(0, 366)
    share = [(fc.pts.stop_day > t).mean() for t in days]
    d.line([(X(t), Y(s)) for t, s in zip(days, share)], fill=GREEN, width=7,
           joint="curve")

    # checkpoints printed in the article
    for day, s in fc.on_therapy.items():
        cx, cy = X(day), Y(s)
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=PAPER,
                  outline=GREEN, width=6)
        lab = f"{s:.1%}"
        f = font("bold", 36)
        tx = cx + 24 if day < 365 else cx - 24 - text_w(d, lab, f)
        d.text((tx, cy - 62), lab, font=f, fill=INK)

    # the finding
    f, fb = font("lora_i", 36), font("bold", 44)
    nx, ny = X(140), Y(0.30)
    d.line([(X(90) + 4, ny + 30), (nx - 20, ny + 30)], fill=GREEN, width=3)
    d.text((nx, ny), f"{fc.share_by_90:.1%}", font=fb, fill=GREEN)
    d.text((nx + text_w(d, f"{fc.share_by_90:.1%}", fb) + 18, ny + 8),
           "of everyone who stops in year one", font=f, fill=INK)
    d.text((nx, ny + 60), "has already stopped by day 90", font=f, fill=INK)

    footer(d, W, H, m)
    img.save(f"{OUT}/fig2_persistence.png", optimize=True)


if __name__ == "__main__":
    six_cuts()
    persistence()
    print("saved:", sorted(os.listdir(OUT)))
