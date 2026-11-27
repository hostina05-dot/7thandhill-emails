"""Square reel: one square in the middle of a 9:16 frame, the same picture blurred behind it.

    python3 scripts/reel_square.py                 # the default sequence below
    python3 scripts/reel_square.py --out reels/square.mp4

Opens on a ring, then our photos on people and pieces take turns in the square, and it ends on
Sally with the seal on the edge of the square (as in the letters) and the brand line above it.
Everything sits in the middle of the frame, clear of the Instagram buttons and caption, and the
square stays whole in the 3:4 profile grid. No sound: add the track in Instagram.
Pieces: codes from products.html (a full-size original in assets/photos/site/<code>.jpg is used
when there is one); photos: originals in assets/photos/, graded as in the letters.
"""
import argparse, csv, subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
from photos import grade  # noqa: E402
from site_products import moonlit_tile  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
W, H, S = 1080, 1920, 1080
Y0 = (H - S) // 2
FPS, FADE, PUSH = 30, 0.22, 1.06
GOLD, CREAM = (201, 169, 106), (237, 232, 223)

# (kind, source, seconds, crop centre x, y[, square side as a share of the photo's short side])
SEQUENCE = [
    ("piece", "R041", 1.8, .5, .5),
    ("photo", "model-green-sweater.jpg", 1.3, .42, .5),
    ("piece", "R045", 1.2, .5, .5),
    ("photo", "hand-rings.jpg", 1.3, .5, .5),
    ("piece", "R064", 1.2, .5, .5),
    ("photo", "necklaces-green-book.jpg", 1.3, .5, .5),
    ("piece", "R019", 1.2, .5, .5),
    ("photo", "model-armchair-compass.jpg", 1.3, .5, .32),
    ("sally", "sally-fireplace.jpg", 3.2, .53, .34, .62),
]


def square(kind, src, cx, cy, zoom=1.0):
    if kind == "piece":
        rows = {r["code"]: r for r in csv.DictReader(open(ROOT / "assets" / "products" / "index.csv")) if r["code"]}
        orig = ROOT / "assets" / "photos" / "site" / f"{src}.jpg"
        if orig.exists():
            return moonlit_tile(Image.open(orig), S, S)
        return Image.open(ROOT / "assets" / "products" / rows[src]["file"]).convert("RGB").resize((S, S), Image.LANCZOS)
    im = grade(Image.open(ROOT / "assets" / "photos" / src).convert("RGB"))
    w, h = im.size
    side = min(w, h) * zoom
    x = min(max(cx * w - side / 2, 0), w - side); y = min(max(cy * h - side / 2, 0), h - side)
    return im.resize((S, S), Image.LANCZOS, box=(x, y, x + side, y + side))


def backdrop(sq):
    """The square blown up to fill the frame, softly blurred and dimmed."""
    bg = ImageOps.fit(sq, (W // 4, H // 4), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
    bg = bg.resize((W, H), Image.BICUBIC)
    return Image.blend(bg, Image.new("RGB", (W, H), (14, 20, 17)), 0.45)


def shot(sq, bg, p):
    """One frame of a shot at progress p: slow push-in on the square."""
    z = 1 + (PUSH - 1) * p
    m = S * (1 - 1 / z) / 2
    frame = bg.copy()
    frame.paste(sq.resize((S, S), Image.LANCZOS, box=(m, m, S - m, S - m)), (0, Y0))
    return frame


def frames(fonts):
    seal = Image.open(ROOT / "assets" / "images" / "seal.png").convert("RGBA").resize((156, 156), Image.LANCZOS)
    serif = ImageFont.truetype(str(fonts / "Italiana-Regular.ttf"), 56)
    sans = ImageFont.truetype(str(fonts / "Jost[wght].ttf"), 28)
    shots = [(square(k, s, *rest), k, d) for k, s, d, *rest in SEQUENCE]
    shots = [(sq, backdrop(sq), k, d) for sq, k, d in shots]
    starts, t = [], 0.0
    for _, _, _, d in shots:
        starts.append(t); t += d
    total = int(t * FPS)
    for f in range(total):
        t = f / FPS
        i = max(j for j, s in enumerate(starts) if s <= t)
        sq, bg, kind, d = shots[i]
        frame = shot(sq, bg, (t - starts[i]) / (d + FADE))
        if i > 0 and t - starts[i] < FADE:  # cross-fade from the shot before
            psq, pbg, _, pd = shots[i - 1]
            prev = shot(psq, pbg, (t - starts[i - 1]) / (pd + FADE))
            a = (t - starts[i]) / FADE
            frame = Image.blend(prev, frame, a * a * (3 - 2 * a))
        if kind == "sally":  # the seal on the edge of the square, the line above it
            a = min(1.0, max(0.0, (t - starts[i] - 0.5) / 0.7))
            if a > 0:
                card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                card.alpha_composite(seal, ((W - 156) // 2, Y0 + S - 78))
                dr = ImageDraw.Draw(card)
                for text, font, colour, y in (("Modern Heirlooms. Timeless Classics.", serif, CREAM, Y0 - 150),
                                              ("7THANDHILLJEWELRY.CA", sans, GOLD, Y0 - 70)):
                    dr.text(((W - dr.textlength(text, font=font)) / 2, y), text, font=font, fill=colour)
                card.putalpha(card.getchannel("A").point(lambda v: int(v * a)))
                frame = frame.convert("RGBA"); frame.alpha_composite(card); frame = frame.convert("RGB")
        yield frame


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "reels" / "reel-square.mp4"))
    ap.add_argument("--fonts", default=str(ROOT / "assets" / "fonts"))
    a = ap.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = 0
    for fr in frames(Path(a.fonts)):
        ff.stdin.write(fr.tobytes()); n += 1
    ff.stdin.close(); ff.wait()
    print(f"{out}  {len(SEQUENCE)} shots, {n / FPS:.1f} s, no sound")


if __name__ == "__main__":
    main()
