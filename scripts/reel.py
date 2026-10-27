"""Checkerboard reel: a 3x5 grid of moonlit tiles where the pieces change square by square, like a chessboard.

    python3 scripts/reel.py R                  # all rings
    python3 scripts/reel.py E --out reels/earrings.mp4
    python3 scripts/reel.py R012 R020 C072 ... # your own pick, in this order
    python3 scripts/reel.py R --hero R041      # opens on one ring, full screen (the default)
    python3 scripts/reel.py R --hero none      # straight to the board

1080x1920, 30 fps, with an original score timed to the board (scripts/score.py; --silent for none). The reel opens on the hero piece full
screen with a slow push-in, then it shrinks into the middle square and the board around it shows.
On every beat one colour of the board
changes: the "black" squares slide up to the next piece, then the "white" squares slide down.
At the end the board turns green square by square and the seal comes up with the brand line.
Pieces come from assets/products/ (codes in products.html). Fonts: Italiana and Jost, from
Google Fonts, in --fonts.
"""
import argparse, csv, random, re, subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "assets" / "products"
W, H, COLS, ROWS, GAP = 1080, 1920, 3, 5, 6
FPS, BEAT, SLIDE, HOLD, OUTRO = 30, 0.6, 0.26, 0.9, 3.0
HERO, PUSH, ZOOM, HERO_HOLD = 1.5, 1.12, 0.8, 0.35  # hero on screen, push-in, shrink into the board, pause after
PAD = 1200                                          # backdrop added around the hero for the zoom
HERO_CELL = 7                                       # the middle square, (column 1, row 2)
HERO_SRC = ROOT / "assets" / "photos" / "site"      # full-size originals for hero pieces: <code>.jpg
IVORY, GREEN, GOLD, CREAM = (247, 245, 241), (28, 58, 46), (201, 169, 106), (237, 232, 223)

CW = (W - GAP * (COLS + 1)) // COLS
CH = (H - GAP * (ROWS + 1)) // ROWS
X0 = (W - (CW * COLS + GAP * (COLS - 1))) // 2
Y0 = (H - (CH * ROWS + GAP * (ROWS - 1))) // 2
CELLS = [(c, r) for r in range(ROWS) for c in range(COLS)]
FILL_TILE = 0.74  # piece size in a tile, as in site_products.py


def pick(args):
    rows = [r for r in csv.DictReader(open(PRODUCTS / "index.csv")) if r["code"]]
    by_code = {r["code"]: r for r in rows}
    if len(args) == 1 and args[0].isalpha():  # a whole type: R, E, N, C ...
        chosen = [r for r in rows if r["code"].rstrip("0123456789") == args[0].upper()]
        if args[0].upper() == "R":  # a few earrings are filed as rings on the site
            chosen = [r for r in chosen if not re.search(r"huggie|climber|studs\b|earring|hoops", r["title"], re.I)]
        random.Random(7).shuffle(chosen)  # mix stones and metals so neighbours differ
        return chosen
    return [by_code[c.upper()] for c in args]


def tile(row, cache={}):
    if row["code"] not in cache:
        im = Image.open(PRODUCTS / row["file"]).convert("RGB")
        side = max(CW, CH)
        im = im.resize((side, side), Image.LANCZOS)
        cache[row["code"]] = im.crop(((side - CW) // 2, (side - CH) // 2, (side - CW) // 2 + CW, (side - CH) // 2 + CH))
    return cache[row["code"]]


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * t * (t * (6 * t - 15) + 10)


def hero_frame(row):
    """The hero piece on a full-screen moonlit backdrop, made from the full-size original."""
    from site_products import moonlit_tile
    src = HERO_SRC / f"{row['code']}.jpg"
    if src.exists():
        return moonlit_tile(Image.open(src), W, H)
    print(f"no {src}: hero made from the 600px tile, it will be soft")
    im = Image.open(PRODUCTS / row["file"]).convert("RGB").resize((W, W), Image.LANCZOS)
    out = Image.new("RGB", (W, H)); out.paste(im.resize((W, H)), (0, 0)); out.paste(im, (0, round(H * 0.46 - W * 0.46)))
    return out


def plan(pieces):
    """Which piece each cell shows on each beat: black squares change on even beats, white on odd."""
    n = len(CELLS)
    queue = list(pieces)
    now = [queue.pop(0) if queue else pieces[i % len(pieces)] for i in range(n)]
    history = [list(now)]
    beat = 0
    while queue:
        colour = beat % 2
        for i, (c, r) in enumerate(CELLS):
            if (c + r) % 2 == colour and queue:
                now[i] = queue.pop(0)
        history.append(list(now))
        beat += 1
    return history


def timeline(pieces, hero=None):
    """When things happen, in seconds from the start: for the music."""
    n = len(pieces) - (1 if hero and any(p["code"] == hero["code"] for p in pieces) else 0) + (1 if hero else 0)
    swaps = len(plan([None] * n)) - 1 if n else 0
    lead, hold = (HERO + ZOOM, HERO_HOLD) if hero else (0.0, HOLD)
    t_end = lead + hold + swaps * BEAT
    return {"opening": HERO if hero else 0.0, "landing": lead if hero else 0.0,
            "cues": [lead + hold + k * BEAT for k in range(swaps)], "outro": t_end,
            "duration": int((t_end + OUTRO) * FPS) / FPS}


def frames(pieces, fonts, hero=None):
    if hero:  # the hero opens the board in the middle square
        pieces = [p for p in pieces if p["code"] != hero["code"]]
        pieces.insert(HERO_CELL, hero)
        import numpy as np
        big = Image.fromarray(np.pad(np.asarray(hero_frame(hero)), ((PAD, PAD), (PAD, PAD), (0, 0)), mode="edge"))
        lead, hold = HERO + ZOOM, HERO_HOLD
    else:
        lead, hold = 0.0, HOLD
    history = plan(pieces)
    seal = Image.open(ROOT / "assets" / "images" / "seal.png").convert("RGBA").resize((300, 300), Image.LANCZOS)
    serif = ImageFont.truetype(str(fonts / "Italiana-Regular.ttf"), 62)
    sans = ImageFont.truetype(str(fonts / "Jost[wght].ttf"), 30)
    try:
        sans.set_variation_by_axes([420])
    except Exception:
        pass
    swaps = len(history) - 1
    t_end = hold + swaps * BEAT
    total = int((lead + t_end + OUTRO) * FPS)
    for f in range(total):
        if hero and f / FPS < HERO:  # the hero alone, slow push-in towards the piece
            z = 1 + (PUSH - 1) * smooth(f / FPS / HERO)
            cx, cy = W / 2, H * 0.46
            yield big.resize((W, H), Image.LANCZOS, box=(PAD + cx - cx / z, PAD + cy - cy / z, PAD + cx + (W - cx) / z, PAD + cy + (H - cy) / z))
            continue
        t = f / FPS - lead
        frame = Image.new("RGB", (W, H), IVORY)
        k = 0 if t < hold else min(swaps, int((t - hold) / BEAT) + 1)  # beats already started
        for i, (c, r) in enumerate(CELLS):
            x, y = X0 + c * (CW + GAP), Y0 + r * (CH + GAP)
            colour = (c + r) % 2
            cur = tile(history[k][i])
            p = 1.0
            if k > 0 and history[k][i] is not history[k - 1][i]:
                p = ease((t - hold - (k - 1) * BEAT) / SLIDE)
            if p < 1.0:
                old = tile(history[k - 1][i])
                cell = Image.new("RGB", (CW, CH))
                d = round(CH * p)
                if colour == 0:  # black squares: new piece rises from below
                    cell.paste(old, (0, -d)); cell.paste(cur, (0, CH - d))
                else:            # white squares: new piece drops from above
                    cell.paste(old, (0, d)); cell.paste(cur, (0, d - CH))
                frame.paste(cell, (x, y))
            else:
                frame.paste(cur, (x, y))
            # outro: the board turns green, black squares first
            g = ease((t - t_end - colour * 0.35) / 0.45)
            if g > 0:
                cover = Image.new("RGB", (CW, CH), GREEN)
                frame.paste(Image.blend(frame.crop((x, y, x + CW, y + CH)), cover, g), (x, y))
        if hero and t < 0:  # the hero shrinks into the middle square, the board shows around it
            frame = shrink(frame, big, tile(hero), smooth((t + ZOOM) / ZOOM))
        # once every square is green, close the gaps and bring up the seal and the line
        a = ease((t - t_end - 0.8) / 0.6)
        if a > 0:
            frame = Image.blend(frame, Image.new("RGB", (W, H), GREEN), a)
            card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            card.alpha_composite(seal, ((W - 300) // 2, H // 2 - 330))
            d = ImageDraw.Draw(card)
            for text, font, colour, y in (("Modern Heirlooms.", serif, CREAM, H // 2 + 40),
                                          ("Timeless Classics.", serif, CREAM, H // 2 + 120),
                                          ("7THANDHILLJEWELRY.CA", sans, GOLD, H // 2 + 250)):
                tw = d.textlength(text, font=font)
                d.text(((W - tw) / 2, y), text, font=font, fill=colour)
            alpha = card.getchannel("A").point(lambda v: int(v * a))
            card.putalpha(alpha)
            frame = frame.convert("RGBA"); frame.alpha_composite(card); frame = frame.convert("RGB")
        yield frame


def shrink(board, big, small, p):
    """Hero at progress p: 0 = full screen (after the push-in), 1 = exactly its tile in the middle square."""
    c, r = CELLS[HERO_CELL]
    x, y = X0 + c * (CW + GAP), Y0 + r * (CH + GAP)
    side = max(CW, CH)                               # how tile() cuts the 600px tile into the cell
    s_end = side / min(W, H)                         # piece size in the cell / piece size full screen
    z = PUSH * (s_end / PUSH) ** p                   # scale, eased geometrically so the zoom feels even
    c0 = (W / 2, H * 0.46)                           # where the piece sits full screen ...
    c1 = (x + side / 2 - (side - CW) / 2, y + side * 0.46 - (side - CH) / 2)  # ... and in its square
    cx, cy = c0[0] + (c1[0] - c0[0]) * p, c0[1] + (c1[1] - c0[1]) * p
    d = [0 + x * p, 0 + y * p, W + (x + CW - W) * p, H + (y + CH - H) * p]  # visible window
    d = [round(v) for v in d]
    box = ((d[0] - cx) / z + c0[0], (d[1] - cy) / z + c0[1], (d[2] - cx) / z + c0[0], (d[3] - cy) / z + c0[1])
    box = tuple(v + PAD for v in box)  # the window can reach past the photo: the backdrop carries on
    part = big.resize((d[2] - d[0], d[3] - d[1]), Image.LANCZOS, box=box)
    if p > 0.75:  # land on the tile itself, so the cut to the board is invisible
        part = Image.blend(part, small.resize(part.size, Image.LANCZOS), (p - 0.75) / 0.25)
    board.paste(part, (d[0], d[1]))
    return board


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pieces", nargs="+", help="a type letter (R, E, N, C, CH, B) or a list of codes")
    ap.add_argument("--out", default=None)
    ap.add_argument("--fonts", default=str(ROOT / "assets" / "fonts"))
    ap.add_argument("--max", type=int, default=0, help="use only the first N pieces")
    ap.add_argument("--hero", default="R041", help="code of the piece that opens the reel full screen, or none")
    ap.add_argument("--silent", action="store_true", help="no music")
    a = ap.parse_args()
    pieces = pick(a.pieces)
    if a.max:
        pieces = pieces[:a.max]
    out = Path(a.out or ROOT / "reels" / f"reel-{a.pieces[0].lower() if len(a.pieces) == 1 else 'pick'}.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    codes = {r["code"]: r for r in csv.DictReader(open(PRODUCTS / "index.csv")) if r["code"]}
    hero = None if a.hero.lower() == "none" else codes[a.hero.upper()]
    audio = []
    if not a.silent:  # original score, timed to the board (scripts/score.py)
        import score
        wav = out.with_suffix(".wav")
        score.write(wav, score.score(**timeline(pieces, hero), beat=BEAT))
        audio = ["-i", str(wav), "-c:a", "aac", "-b:a", "192k", "-shortest"]
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", *audio[:2], "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                           "-pix_fmt", "yuv420p", *audio[2:], "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = 0
    for fr in frames(pieces, Path(a.fonts), hero):
        ff.stdin.write(fr.tobytes()); n += 1
    ff.stdin.close(); ff.wait()
    if audio:
        out.with_suffix(".wav").unlink()
    print(f"{out}  {len(pieces)} pieces, {n / FPS:.1f} s{'' if audio else ', no sound'}")


if __name__ == "__main__":
    main()
