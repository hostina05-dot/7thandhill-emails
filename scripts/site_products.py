"""Every product from www.7thandhilljewelry.ca on the moonlit backdrop of the letters.

    python3 scripts/site_products.py <folder with products.json pages and downloaded images>

Picks the first photo of each product shot on white, evens out the white, centres the piece
with the same air around it, and multiplies it onto the moonlit gradient (as the packshots in
photos.py). Writes assets/products/<code>-<handle>.jpg, assets/products/index.csv and products.html.

Every piece gets a short code by type: R012 = ring no. 12 (C charm, R ring, E earrings, N necklace,
CH chain, B bracelet, CN connector, L lock, O other). Codes never change on a re-run; new products
get the next free number of their type. In scripts/compose.py a code works like a catalog number.
"""
import csv, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).parent))
from photos import moonlit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "products"
SITE = "https://www.7thandhilljewelry.ca/products/"
TYPES = {"Earrings": "Earring", "Necklaces": "Necklace", "Charms & Pendants": "Charm", "": "Other"}
CODES = {"Charm": "C", "Ring": "R", "Earring": "E", "Necklace": "N", "Chain": "CH", "Bracelet": "B",
         "Connector": "CN", "Lock": "L"}
SIZE, FILL = 600, 0.74  # the piece's longer side takes 74% of the square


def flatten(im):
    """Cut-out PNGs keep their transparency; put them on white paper first."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        paper = Image.new("RGBA", im.size, (255, 255, 255, 255))
        paper.alpha_composite(im)
        im = paper
    return im.convert("RGB")


def on_white(im):
    a = np.asarray(flatten(im).resize((200, 200))).astype(float)
    ring = np.concatenate([a[:10].reshape(-1, 3), a[-10:].reshape(-1, 3), a[:, :10].reshape(-1, 3), a[:, -10:].reshape(-1, 3)])
    lum = ring.mean(1)
    if np.median(a.mean(2)) < 215:  # mostly dark inside a white frame
        return False
    return lum.mean() > 228 and np.percentile(lum, 5) > 205 and (ring.max(1) - ring.min(1)).mean() < 14


def moonlit_tile(im):
    a = np.asarray(flatten(im)).astype(np.float32)
    h, w, _ = a.shape
    b = max(2, int(min(h, w) * 0.04))
    border = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    a = np.clip(a * (255.0 / np.median(border, 0)), 0, 255)  # off-white paper -> pure white
    lum = a.mean(2, keepdims=True)
    a = a + (255 - a) * np.clip((lum - 228) / 18, 0, 1)        # faint grey boxes around the piece fade out
    ink = (255 - a.min(2)) > 18                               # where the piece (and its shadow) is
    ys, xs = np.nonzero(ink)
    if len(xs) < 50:
        y0, y1, x0, x1 = 0, h - 1, 0, w - 1
    else:
        y0, y1 = np.percentile(ys, [0.2, 99.8]).astype(int); x0, x1 = np.percentile(xs, [0.2, 99.8]).astype(int)
    m = 0.01  # a piece the photographer cut off at the frame keeps that edge on the tile edge
    left, right, top, bottom = x0 <= w * m, x1 >= w * (1 - m), y0 <= h * m, y1 >= h * (1 - m)
    x0, x1 = (0 if left else x0), (w - 1 if right else x1)
    y0, y1 = (0 if top else y0), (h - 1 if bottom else y1)
    piece = Image.fromarray(a.astype(np.uint8)).crop((x0, y0, x1 + 1, y1 + 1))
    pw, ph = piece.size
    k = SIZE * FILL / max(pw, ph)
    if left and right: k = max(k, SIZE / pw)
    if top and bottom: k = max(k, SIZE / ph)
    piece = piece.resize((max(1, round(pw * k)), max(1, round(ph * k))), Image.LANCZOS)
    pw, ph = piece.size
    px = 0 if left and not right else SIZE - pw if right and not left else (SIZE - pw) // 2
    py = 0 if top and not bottom else SIZE - ph if bottom and not top else (SIZE - ph) // 2 if top else round(SIZE * 0.46 - ph / 2)
    canvas = Image.new("RGB", (SIZE, SIZE), "white")
    canvas.paste(piece, (px, py))
    return ImageChops.multiply(canvas, moonlit(SIZE, SIZE))


def gallery(rows):
    """products.html: every tile with its code, name and link, grouped by type, with a search box.
    Small copies of the tiles sit inside the page, so it shows the pictures wherever it is opened."""
    import base64, html, io

    def thumb(file):
        b = io.BytesIO()
        Image.open(OUT / file).resize((240, 240), Image.LANCZOS).save(b, "JPEG", quality=72, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    groups = {}
    for r in rows:
        if r["file"]:
            groups.setdefault(r["group"], []).append(r)
    parts = []
    for t in sorted(groups, key=lambda t: -len(groups[t])):
        cards = "".join(
            f'<a class="c" href="{r["url"]}" target="_blank" data-k="{r["code"].lower()} {html.escape(r["title"].lower())}">'
            f'<img loading="lazy" src="{thumb(r["file"])}" alt=""><b>{r["code"]}</b><span>{html.escape(r["title"])}</span></a>'
            for r in groups[t])
        parts.append(f'<section><h2>{html.escape(t)} <small>{groups[t][0]["code"].rstrip("0123456789")} · {len(groups[t])}</small></h2>'
                     f'<div class="g">{cards}</div></section>')
    n = sum(len(v) for v in groups.values())
    (ROOT / "products.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>7th & Hill pieces</title>
<style>body{{margin:0;padding:24px 16px;background:#f7f5f1;color:#1d2b24;font:14px/1.4 Arial,sans-serif}}
h1{{font:400 30px Georgia,serif;margin:0 0 4px}}p{{margin:0 0 14px;color:#5b6660}}h2{{font:400 22px Georgia,serif;margin:28px 0 12px}}
small{{font:12px Arial;color:#8a938e}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
input{{width:100%;max-width:360px;box-sizing:border-box;padding:10px 12px;border:1px solid #cfd3cf;font:14px Arial;background:#fff}}
.c{{display:block;color:inherit;text-decoration:none;background:#fff;padding:6px 6px 8px}}.c img{{width:100%;display:block}}
.c b{{display:block;font:700 15px Arial;margin-top:6px;letter-spacing:.04em}}.c span{{display:block;font-size:12px;color:#5b6660}}</style></head>
<body><h1>7th &amp; Hill pieces</h1>
<p>{n} pieces from the site on the moonlit backdrop. To put a piece in a letter, name its code, for example R012.
C charm · R ring · E earrings · N necklace · CH chain · B bracelet · CN connector · L lock · O other. Click a tile for the product page. Full-size tiles: assets/products/&lt;code&gt;-….jpg.</p>
<input id="q" type="search" placeholder="Search by code or name: R012, scarab, heart">
{"".join(parts)}
<script>document.getElementById('q').addEventListener('input',function(){{var q=this.value.trim().toLowerCase();
document.querySelectorAll('.c').forEach(function(c){{c.style.display=!q||c.dataset.k.indexOf(q)>-1?'':'none'}});
document.querySelectorAll('section').forEach(function(s){{s.style.display=s.querySelector('.c:not([style*="none"])')?'':'none'}})}});</script>
</body></html>
""")


def main(src):
    src = Path(src)
    products = []
    for page in sorted(src.glob("p*.json")):
        products += json.load(open(page))["products"]
    OUT.mkdir(parents=True, exist_ok=True)
    index = OUT / "index.csv"
    known = {r["url"]: r.get("code", "") for r in csv.DictReader(open(index))} if index.exists() else {}
    known = {u: c for u, c in known.items() if c}
    count = {}
    for c in known.values():
        pre = c.rstrip("0123456789"); count[pre] = max(count.get(pre, 0), int(c[len(pre):]))
    rows = []
    for p in products:
        if p["handle"].startswith("gift-card"):
            continue
        group = TYPES.get(p["product_type"], p["product_type"])
        shots = [src / "img" / f"{p['id']}_{k}.jpg" for k in range(len(p["images"]))]
        pick = next((f for f in shots if f.exists() and on_white(Image.open(f))), None)
        url = SITE + p["handle"]
        code = known.get(url, "")
        if pick and not code:
            pre = CODES.get(group, "O"); count[pre] = count.get(pre, 0) + 1
            code = f"{pre}{count[pre]:03d}"
        name = f"{code}-{p['handle']}.jpg" if pick else ""
        if pick:
            moonlit_tile(Image.open(pick)).save(OUT / name, quality=82, optimize=True, progressive=True)
        rows.append({"code": code, "title": p["title"].title().replace("14K", "14k").replace("10K", "10k").replace("18K", "18k"), "type": p["product_type"], "group": group,
                     "url": url, "file": name, "note": "" if pick else "no photo on white, left out",
                     "available": "yes" if any(v["available"] for v in p["variants"]) else "no"})
    rows.sort(key=lambda r: (not r["code"], r["code"].rstrip("0123456789"), int(r["code"].lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ") or 0)))
    for old in OUT.glob("*.jpg"):  # tiles of products that left the site, or from before the codes
        if old.name not in {r["file"] for r in rows}:
            old.unlink()
    with open(index, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    gallery(rows)
    with open(ROOT / "blocks" / "site-products.md", "w") as f:
        f.write("# 7th & Hill · all pieces from the site\n\nCode = what to name in a letter (R012 = ring no. 12). "
                "Pictures: products.html. Tiles: assets/products/.\n\n| Code | Piece | Link |\n|---|---|---|\n")
        for r in rows:
            if r["code"]:
                f.write(f"| {r['code']} | {r['title']} | {r['url']} |\n")
    print(f"{sum(bool(r['file']) for r in rows)} of {len(rows)} products on the moonlit backdrop -> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1])
