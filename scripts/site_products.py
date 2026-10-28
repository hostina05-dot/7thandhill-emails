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


def moonlit_tile(im, w_out=SIZE, h_out=SIZE):
    """The piece on the moonlit backdrop; the square tile by default, any frame (a reel cover) on request."""
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
    k = min(w_out, h_out) * FILL / max(pw, ph)
    if left and right: k = max(k, w_out / pw)
    if top and bottom: k = max(k, h_out / ph)
    piece = piece.resize((max(1, round(pw * k)), max(1, round(ph * k))), Image.LANCZOS)
    pw, ph = piece.size
    px = 0 if left and not right else w_out - pw if right and not left else (w_out - pw) // 2
    py = 0 if top and not bottom else h_out - ph if bottom and not top else (h_out - ph) // 2 if top else round(h_out * 0.46 - ph / 2)
    canvas = Image.new("RGB", (w_out, h_out), "white")
    canvas.paste(piece, (px, py))
    return ImageChops.multiply(canvas, moonlit(w_out, h_out))


# The gallery follows the site: one block per category, and inside Charms and Rings the site's own
# collections (assets/products/collections.json: collection handle -> product handles, from
# /collections/<handle>/products.json). A piece goes in the first collection of the list it belongs to.
BLOCKS = [("Ring", "Rings"), ("Earring", "Earrings"), ("Necklace", "Necklaces"), ("Chain", "Chains"),
          ("Bracelet", "Bracelets"), ("Charm", "Charms"), ("Connector", "Connectors"), ("Lock", "Locks"),
          ("Other", "Other")]
SUBS = {
    "Charm": [("Amulets &amp; Talismans", "talismans-medallions"), ("Large charms", "large-charms"),
              ("Medium charms", "medium-charms-1"), ("Small charms", "small-charms"), ("Mini charms", "mini-charms"),
              ("Rondelles", "rondelles"), ("Children&rsquo;s edit", "semi-fine-charms"), ("More charms", None)],
    "Ring": [("Bespoke bridal &amp; cocktail", "coming-soon"), ("The Grand Art Deco", "the-grand-art-deco-collection"),
             ("More rings", None)],
}


def gallery(rows):
    """products.html: one block per category (with the site's collections inside Charms and Rings),
    a code on every tile, a bar to jump between blocks and a search box.
    Small copies of the tiles sit inside the page, so it shows the pictures wherever it is opened."""
    import base64, html, io

    def thumb(file):
        b = io.BytesIO()
        Image.open(OUT / file).resize((240, 240), Image.LANCZOS).save(b, "JPEG", quality=72, optimize=True, progressive=True)
        return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

    def card(r):
        return (f'<a class="c" href="{r["url"]}" target="_blank" data-k="{r["code"].lower()} {html.escape(r["title"].lower())}">'
                f'<img loading="lazy" src="{thumb(r["file"])}" alt=""><b>{r["code"]}</b><span>{html.escape(r["title"])}</span></a>')

    member = json.load(open(OUT / "collections.json")) if (OUT / "collections.json").exists() else {}
    member = {k: set(v) for k, v in member.items()}
    groups = {}
    for r in rows:
        if r["file"]:
            groups.setdefault("Other" if r["group"] == "Rondelle" else r["group"], []).append(r)
    order = [g for g, _ in BLOCKS if g in groups] + [g for g in groups if g not in dict(BLOCKS)]
    label = dict(BLOCKS)
    nav, parts = [], []
    for g in order:
        items = groups[g]
        gid = label.get(g, g).lower().replace(" ", "-")
        letter = items[0]["code"].rstrip("0123456789")
        nav.append(f'<a href="#{gid}">{label.get(g, g)} <i>{len(items)}</i></a>')
        if g in SUBS and member:
            left, subs = list(items), []
            for name, handle in SUBS[g]:
                take = [r for r in left if handle is None or r["url"].rsplit("/", 1)[1] in member.get(handle, ())]
                left = [r for r in left if r not in take]
                if take:
                    subs.append(f'<div class="sub"><h3>{name} <small>{len(take)}</small></h3><div class="g">{"".join(map(card, take))}</div></div>')
            body = "".join(subs)
        else:
            body = f'<div class="g">{"".join(map(card, items))}</div>'
        parts.append(f'<section id="{gid}"><h2>{label.get(g, g)} <small>{letter} · {len(items)}</small></h2>{body}</section>')
    n = sum(len(v) for v in groups.values())
    (ROOT / "products.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>7th & Hill pieces</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:120px}}
body{{margin:0;background:#F3F1EC;color:#2E2A26;font:14px/1.45 Inter,Arial,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:28px 16px 60px}}
h1{{font:400 40px/1.05 Cormorant,Georgia,serif;margin:0 0 6px}}
.lead{{margin:0 0 4px;color:#5E5950}}.key{{margin:0;color:#8A857C;font-size:12px}}
.bar{{position:sticky;top:0;z-index:5;background:#F3F1EC;padding:14px 0 12px;border-bottom:1px solid #E2DDD3;margin:18px 0 8px}}
.nav{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}}
.nav a{{color:#58744E;border:1px solid #58744E;padding:6px 12px;text-decoration:none;font-size:12px;letter-spacing:.06em;text-transform:uppercase;background:#fff}}
.nav a:hover{{background:#58744E;color:#fff}}.nav i{{font-style:normal;opacity:.6;margin-left:4px}}
input{{width:100%;max-width:380px;padding:10px 12px;border:1px solid #D8D3C9;font:14px Inter,Arial,sans-serif;background:#fff}}
section{{background:#fff;border:1px solid #E6E1D8;box-shadow:0 4px 24px rgba(46,42,38,.07);padding:22px 20px 24px;margin:22px 0}}
h2{{font:400 32px/1.1 Cormorant,Georgia,serif;margin:0 0 16px}}h2 small,h3 small{{font:400 12px Inter,Arial;color:#9C7E4A;letter-spacing:.12em;margin-left:8px}}
.sub{{margin:0 0 22px}}.sub:last-child{{margin-bottom:0}}
h3{{font:600 11px Inter,Arial,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:#9C7E4A;margin:0 0 10px;padding-top:14px;border-top:1px solid #EEEAE3}}
.sub:first-child h3{{border-top:0;padding-top:0}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}}
.c{{display:block;color:inherit;text-decoration:none}}.c img{{width:100%;display:block}}
.c b{{display:block;font:600 14px Inter,Arial;margin-top:7px;letter-spacing:.04em}}.c span{{display:block;font-size:12px;line-height:1.35;color:#5E5950}}
@media (max-width:600px){{h1{{font-size:32px}}section{{padding:18px 12px}}.g{{grid-template-columns:repeat(2,1fr)}}
.bar{{margin-left:-16px;margin-right:-16px;padding-left:16px;padding-right:16px}}
.nav{{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}}.nav a{{flex:0 0 auto}}}}
</style></head>
<body><div class="wrap"><h1>7th &amp; Hill pieces</h1>
<p class="lead">{n} pieces from the site on the moonlit backdrop, by category. To put a piece in a letter, name its code, for example R012.</p>
<p class="key">C charm · R ring · E earrings · N necklace · CH chain · B bracelet · CN connector · L lock · O other. Click a tile for the product page.</p>
<div class="bar"><div class="nav">{"".join(nav)}</div>
<input id="q" type="search" placeholder="Search by code or name: R012, scarab, heart"></div>
{"".join(parts)}
</div>
<script>document.getElementById('q').addEventListener('input',function(){{var q=this.value.trim().toLowerCase();
document.querySelectorAll('.c').forEach(function(c){{c.style.display=!q||c.dataset.k.indexOf(q)>-1?'':'none'}});
document.querySelectorAll('.sub,section').forEach(function(s){{s.style.display=s.querySelector('.c:not([style*="none"])')?'':'none'}})}});</script>
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
