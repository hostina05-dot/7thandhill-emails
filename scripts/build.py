#!/usr/bin/env python3
"""7th & Hill email build.

    python3 scripts/compose.py   # writes templates/ from the copy and blocks
    python3 scripts/build.py     # preview.html grouped by stage + klaviyo/ copies

    build.py rebuilds preview.html: every template grouped by launch stage, with labels,
        a plain overview of each stage on top, images embedded, Klaviyo tags filled
        with sample data. Open it in any browser.

        Also writes klaviyo/*.html: the same templates with image paths pointed
        at the image host (by default this public repo's main branch via jsDelivr),
        ready to paste into Klaviyo (Content > Templates > Create > HTML).

No dependencies beyond Python 3.8+.
"""
import argparse
import base64
import json
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
IMAGES = ROOT / "assets" / "images"
LOCAL_PREFIX = "../assets/images/"
DEFAULT_BASE = "https://cdn.jsdelivr.net/gh/hostina05-dot/7thandhill-emails@main/assets/images/"

# Preview order inside each stage (brief order). Stage comes from the file name prefix s1-, s2-...
ORDER = [
    "s1-p0", "s1-w1", "s1-w2", "s1-w3", "s1-w4", "s1-w5", "s1-t1", "s1-t2", "s1-t3",
    "s2-k3", "s2-c1", "s2-c2", "s2-co1", "s2-co2", "s2-co3", "s2-cc1", "s2-cc2",
    "s3-b1", "s3-b2", "s3-pp1", "s3-pp2", "s3-pp3", "s3-an1", "s3-k1",
    "s4-s1", "s4-s2", "s4-s3", "s4-dyo", "s4-k4", "s4-k2", "s4-lc", "s4-hn",
]
STAGES = {
    1: "STAGE 1 · Goes live Tue, Oct 27",
    2: "STAGE 2 · Goes live Mon, Nov 2 (K3 sends Tue, Nov 3)",
    3: "STAGE 3 · Goes live Mon, Nov 9",
    4: "STAGE 4 · By Tue, Nov 24",
}
# Plain overview at the top of the preview
OVERVIEW = [
    ("Етап 1 · запуск у вівторок, 27 жовтня",
     "Усе, що потрібно з першого дня. Попап на сайті запрошує в 7H Vault. Хто підписався, отримує 5 вітальних листів: "
     "одразу лист із кодом на 15%, потім історію бренду, добірку Sally, головне про золото й доставку і пропозицію допомогти з вибором "
     "(дні 0, 1, 3, 5, 8). Окремо 3 листи для старих клієнтів SALT: Sally представляє 7th & Hill і питає, чи писати їм далі. "
     "Хто натиснув «Yes», отримує ті самі вітальні листи. Хто мовчить, отримує ще одне нагадування, а потім прощальний лист."),
    ("Етап 2 · запуск у понеділок, 2 листопада",
     "Листи, що повертають покупців. Розсилка K3 у вівторок, 3 листопада: до яких дат замовляти подарунки на свята. "
     "Хто поклав виріб у кошик і пішов, отримує 2 листи (через 2 години і через добу). Хто дійшов до оплати й не завершив, "
     "отримує 3 листи (через 2 години, добу і 2 доби). Якщо сума від $5,500, замість них приходять 2 особисті записки від Sally."),
    ("Етапи 3 і 4 · з 9 листопада, усе готово до 24 листопада",
     "Етап 3: хто переглядав виріб, отримує 2 листи. Після покупки йдуть 3 листи: подяка одразу, догляд за прикрасою на 21-й день, "
     "нові вироби на 35-й день. Привітання з річницею покупки. Щотижнева розсилка «New in the studio». "
     "Етап 4: Black Friday (25, 27 і 30 листопада), Design Your Own (17 листопада), гід подарунків (3 грудня), Sally’s edit (8 грудня), "
     "останній день замовлень (15 грудня) і святкова записка від Sally (24 грудня)."),
]

SAMPLE = {
    "first_name": "Margaret",
    "organization.full_address": "190 Roslin Avenue, Toronto, Ontario M4N 1Z6",
}
# sample event data so dynamic blocks show something in the preview (Klaviyo fills the real values)
SAMPLE_ITEMS = [
    {"ProductName": "Marquise Diamond Open Wing Ring", "ImageURL": LOCAL_PREFIX + "product-21.jpg", "ProductURL": "#"},
    {"ProductName": "Pear Lab Diamond Studs", "ImageURL": LOCAL_PREFIX + "product-16.jpg", "ProductURL": "#"},
]
SAMPLE_EVENT = {"ProductName": "Lovers Tarot Pendant", "ImageURL": LOCAL_PREFIX + "product-01.jpg", "URL": "#"}


def fill_klaviyo(src: str, first_name: str) -> str:
    """Very small stand-in for Klaviyo's renderer, enough for a visual preview."""
    def if_block(m):
        return m.group(1) if first_name else m.group(2)

    def items(m):
        body = m.group(1)
        return "".join(re.sub(r"{{\s*item\.(\w+)\s*}}", lambda v: it.get(v.group(1), ""), body) for it in SAMPLE_ITEMS)

    src = re.sub(r"{%\s*if first_name\s*%}(.*?){%\s*else\s*%}(.*?){%\s*endif\s*%}", if_block, src, flags=re.S)
    src = re.sub(r"{{\s*first_name\|default:'[^']*'\s*}}", first_name, src)
    src = re.sub(r"{%\s*for item in event\.Items\s*%}(.*?){%\s*endfor\s*%}", items, src, flags=re.S)
    src = re.sub(r"{{\s*event\.(ProductName|ImageURL)\s*}}", lambda v: SAMPLE_EVENT[v.group(1)], src)
    src = re.sub(r"{{\s*event\.URL\s*}}", "#", src)
    src = re.sub(r"{{\s*organization\.full_address\s*}}", SAMPLE["organization.full_address"], src)
    src = re.sub(r"{%\s*unsubscribe\s*%}", '<a href="#">Unsubscribe</a>', src)
    src = re.sub(r"{%\s*unsubscribe_url\s*%}", "#", src)
    src = re.sub(r"{%\s*manage_preferences\s*%}", '<a href="#">Manage preferences</a>', src)
    src = re.sub(r"{%\s*coupon_code\s+'([^']+)'\s*%}", r"\1-SAMPLE", src)   # Klaviyo makes a unique code per person
    src = re.sub(r"{{\s*[\w.]+\|default:'([^']*)'\s*}}", r"\1", src)  # any other var -> its default
    return src


def image_map(names) -> dict:
    """Each image once, as a data URI, so the preview stays self-contained without repeating files."""
    out = {}
    for name in sorted(names):
        path = IMAGES / name
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        out[name] = "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())
    return out


def meta(src: str, key: str) -> str:
    m = re.search(r"^\s*%s:\s*(.+)$" % key, src, flags=re.M)
    return m.group(1).strip() if m else ""


def order_key(path: Path):
    stem = path.name
    for i, prefix in enumerate(ORDER):
        if stem.startswith(prefix + "-") or stem == prefix + ".html":
            return (i, stem)
    return (len(ORDER), stem)


def build_preview():
    cards, used = [], set()
    for path in sorted(TEMPLATES.glob("*.html"), key=order_key):
        raw = path.read_text(encoding="utf-8")
        used.update(re.findall(re.escape(LOCAL_PREFIX) + r"([\w.-]+)", raw))
        head = raw.split("-->", 1)[0]
        stage = int(re.match(r"s(\d)-", path.name).group(1)) if re.match(r"s\d-", path.name) else 0
        cards.append({
            "file": path.name,
            "stage": stage,
            "label": meta(head, "Card"),
            "subject": meta(head, "Subject"),
            "preheader": meta(head, "Preheader"),
            "kb": round(len(raw.encode("utf-8")) / 1024, 1),
            "named": fill_klaviyo(raw, SAMPLE["first_name"]),
            "anon": fill_klaviyo(raw, ""),
        })
    page = (PREVIEW.replace("/*DATA*/[]", json.dumps(cards))
            .replace("/*IMAGES*/{}", json.dumps(image_map(used)))
            .replace("/*STAGES*/{}", json.dumps(STAGES))
            .replace("/*OVERVIEW*/[]", json.dumps(OVERVIEW, ensure_ascii=False)))
    (ROOT / "preview.html").write_text(page, encoding="utf-8")
    print("preview.html written (%d templates)" % len(cards))


def build_dist(base_url: str):
    base = base_url if base_url.endswith("/") else base_url + "/"
    out = ROOT / "klaviyo"
    out.mkdir(exist_ok=True)
    for old in out.glob("*.html"):
        old.unlink()
    for path in sorted(TEMPLATES.glob("*.html")):
        src = path.read_text(encoding="utf-8").replace(LOCAL_PREFIX, base)
        src = re.sub(r"  Images use relative paths.*?\n.*?klaviyo/[\w.-]+\n",
                     "  Ready to paste into Klaviyo: images load from %s\n" % base, src)
        (out / path.name).write_text(src, encoding="utf-8")
        print("klaviyo/%s" % path.name)


PREVIEW = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>7th &amp; Hill Launch Letters</title>
<style>
  :root { --bg:#101613; --panel:#161E1A; --line:#26302B; --ink:#EDE8DF; --dim:#9AA59F; --accent:#C9A96A; --ok:#8FA79B; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:300 14px/1.5 "Helvetica Neue", Helvetica, Arial, sans-serif; }
  header { position:sticky; top:0; z-index:5; display:flex; flex-wrap:wrap; gap:16px 28px; align-items:center; justify-content:space-between;
           padding:16px 24px; background:rgba(16,22,19,.95); border-bottom:1px solid var(--line); backdrop-filter:blur(6px); }
  h1 { margin:0; font:400 24px/1.2 Georgia, serif; }
  h1 small { display:block; margin-top:4px; font:300 10px/1.4 "Helvetica Neue", Arial, sans-serif; letter-spacing:3px; color:var(--dim); text-transform:uppercase; }
  .controls { display:flex; flex-wrap:wrap; gap:12px; }
  .seg { display:inline-flex; border:1px solid var(--line); }
  .seg button { appearance:none; border:0; background:transparent; color:var(--dim); padding:8px 13px; cursor:pointer;
                font:400 10px/1 "Helvetica Neue", Arial, sans-serif; letter-spacing:2.5px; text-transform:uppercase; }
  .seg button[aria-pressed="true"] { background:var(--ink); color:var(--bg); }
  .seg button:focus-visible { outline:1px solid var(--accent); outline-offset:2px; }
  .overview { margin:24px 24px 0; display:flex; flex-wrap:wrap; gap:18px; }
  .overview div { flex:1 1 300px; max-width:520px; padding:18px 22px; border:1px solid var(--line); }
  .overview h2 { margin:0 0 8px; font:400 11px/1.5 "Helvetica Neue", Arial, sans-serif; letter-spacing:2.5px; text-transform:uppercase; color:var(--accent); }
  .overview p { margin:0; color:var(--ink); font-size:14px; line-height:22px; }
  .stage { padding:28px 0 8px; }
  .stage h2 { margin:0 24px 16px; font:400 12px/1.4 "Helvetica Neue", Arial, sans-serif; letter-spacing:3.5px; color:var(--accent);
              border-bottom:1px solid var(--line); padding-bottom:10px; }
  .row { display:flex; gap:32px; padding:0 24px 24px; overflow-x:auto; align-items:flex-start; }
  .card { flex:0 0 auto; }
  .meta { margin:0 0 12px; }
  .meta .label { font-size:10px; letter-spacing:2.5px; text-transform:uppercase; color:var(--accent); }
  .meta .file { font:11px/1.4 ui-monospace, Menlo, monospace; color:var(--dim); margin-top:2px; }
  .meta .subject { margin-top:6px; font:400 17px/1.3 Georgia, serif; color:var(--ink); }
  .meta .pre { color:var(--dim); font-size:12px; }
  .frame { border:1px solid var(--line); background:var(--panel); }
  iframe { display:block; border:0; width:600px; height:900px; background:#101613; }
  footer { padding:8px 24px 40px; color:var(--dim); font-size:12px; }
  @media (max-width:700px) { .row { flex-direction:column; } iframe { width:100% !important; } .card { width:100%; } }
</style>
</head>
<body>
<header>
  <h1>7th &amp; Hill <small>Launch letters · preview by stage</small></h1>
  <div class="controls">
    <div class="seg" data-key="width" aria-label="Width">
      <button data-v="600" aria-pressed="true">Desktop</button><button data-v="375">Mobile</button>
    </div>
    <div class="seg" data-key="name" aria-label="First name">
      <button data-v="named" aria-pressed="true">With name</button><button data-v="anon">No name</button>
    </div>
    <div class="seg" data-key="zoom" aria-label="Zoom">
      <button data-v="1">100%</button><button data-v="0.75">75%</button><button data-v="0.5" aria-pressed="true">50%</button>
    </div>
  </div>
</header>
<section class="overview" id="overview"></section>
<main id="stages"></main>
<footer>Generated by scripts/build.py. Sample name, address, coupon and bag contents are placeholders; Klaviyo fills the real ones.</footer>
<script>
  const DATA = /*DATA*/[];
  const IMAGES = /*IMAGES*/{};
  const STAGES = /*STAGES*/{};
  const OVERVIEW = /*OVERVIEW*/[];
  const state = { width: "600", name: "named", zoom: "0.5" };
  const root = document.getElementById("stages");
  OVERVIEW.forEach(([t, d]) => {
    const box = document.createElement("div");
    box.innerHTML = "<h2></h2><p></p>";
    box.querySelector("h2").textContent = t; box.querySelector("p").textContent = d;
    document.getElementById("overview").appendChild(box);
  });

  function source(c) {
    return c[state.name].replace(/\.\.\/assets\/images\/([\w.-]+)/g, (m, f) => IMAGES[f] || m);
  }
  function fit(f) {
    try { f.style.height = f.contentDocument.documentElement.scrollHeight + "px"; } catch (e) {}
  }
  function render() {
    root.innerHTML = "";
    Object.keys(STAGES).forEach(n => {
      const cards = DATA.filter(c => String(c.stage) === n);
      if (!cards.length) return;
      const sec = document.createElement("section");
      sec.className = "stage";
      sec.innerHTML = '<h2></h2><div class="row"></div>';
      sec.querySelector("h2").textContent = STAGES[n];
      const row = sec.querySelector(".row");
      cards.forEach(c => {
        const card = document.createElement("article");
        card.className = "card";
        card.style.zoom = state.zoom;
        card.innerHTML = '<div class="meta" style="width:' + state.width + 'px"><div class="label"></div><div class="file"></div>' +
                         '<div class="subject"></div><div class="pre"></div></div><div class="frame"><iframe></iframe></div>';
        card.querySelector(".label").textContent = c.label;
        card.querySelector(".file").textContent = c.file + " · " + c.kb + " KB";
        card.querySelector(".subject").textContent = c.subject;
        card.querySelector(".pre").textContent = c.preheader;
        const f = card.querySelector("iframe");
        f.title = c.label;
        f.style.width = state.width + "px";
        f.addEventListener("load", () => { fit(f); setTimeout(() => fit(f), 700); });
        f.srcdoc = source(c);
        row.appendChild(card);
      });
      root.appendChild(sec);
    });
  }
  document.querySelectorAll(".seg").forEach(seg => {
    seg.addEventListener("click", e => {
      const b = e.target.closest("button"); if (!b) return;
      seg.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b));
      state[seg.dataset.key] = b.dataset.v;
      render();
    });
  });
  render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=DEFAULT_BASE,
                    help="public folder URL where assets/images/* are hosted (default: %(default)s)")
    args = ap.parse_args()
    build_preview()
    build_dist(args.base_url)
