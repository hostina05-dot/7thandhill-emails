#!/usr/bin/env python3
"""7th&Hill email build.

    python3 scripts/build.py
        Rebuilds preview.html: every template side by side, images embedded,
        Klaviyo tags filled with sample data. Open it in any browser.

    python3 scripts/build.py --base-url https://cdn.shopify.com/s/files/.../files/
        Also writes dist/*.html with image paths pointed at your image host,
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

# Order and labels in the preview
ORDER = [
    ("welcome-1.html", "Welcome · 1 of 3"),
    ("welcome-2.html", "Welcome · 2 of 3"),
    ("welcome-3.html", "Welcome · 3 of 3"),
    ("campaign-master.html", "Campaign master"),
    ("thank-you.html", "Post-purchase"),
    ("abandoned-cart.html", "Abandoned cart"),
]

SAMPLE = {
    "first_name": "Margaret",
    "organization.full_address": "190 Roslin Avenue, Toronto, Ontario M4N 1Z6",
}


def fill_klaviyo(src: str, first_name: str) -> str:
    """Very small stand-in for Klaviyo's renderer, enough for a visual preview."""
    def if_block(m):
        return m.group(1) if first_name else m.group(2)

    src = re.sub(r"{%\s*if first_name\s*%}(.*?){%\s*else\s*%}(.*?){%\s*endif\s*%}", if_block, src, flags=re.S)
    src = re.sub(r"{{\s*first_name\|default:'[^']*'\s*}}", first_name, src)
    src = re.sub(r"{{\s*organization\.full_address\s*}}", SAMPLE["organization.full_address"], src)
    src = re.sub(r"{%\s*unsubscribe\s*%}", '<a href="#">Unsubscribe</a>', src)
    src = re.sub(r"{%\s*manage_preferences\s*%}", '<a href="#">Manage preferences</a>', src)
    src = re.sub(r"{{\s*[\w.]+\|default:'([^']*)'\s*}}", r"\1", src)  # any other var -> its default
    return src


def embed_images(src: str) -> str:
    def repl(m):
        path = IMAGES / m.group(1)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())

    return re.sub(re.escape(LOCAL_PREFIX) + r"([\w.-]+)", repl, src)


def meta(src: str, key: str) -> str:
    m = re.search(r"^\s*%s:\s*(.+)$" % key, src, flags=re.M)
    return m.group(1).strip() if m else ""


def build_preview():
    cards = []
    for name, label in ORDER:
        raw = (TEMPLATES / name).read_text(encoding="utf-8")
        cards.append({
            "file": name,
            "label": label,
            "subject": meta(raw, "Subject"),
            "preheader": meta(raw, "Preheader"),
            "kb": round(len(raw.encode("utf-8")) / 1024, 1),
            "named": embed_images(fill_klaviyo(raw, SAMPLE["first_name"])),
            "anon": embed_images(fill_klaviyo(raw, "")),
        })
    page = PREVIEW.replace("/*DATA*/[]", json.dumps(cards))
    (ROOT / "preview.html").write_text(page, encoding="utf-8")
    print("preview.html written (%d templates)" % len(cards))


def build_dist(base_url: str):
    base = base_url if base_url.endswith("/") else base_url + "/"
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for path in sorted(TEMPLATES.glob("*.html")):
        src = path.read_text(encoding="utf-8").replace(LOCAL_PREFIX, base)
        (out / path.name).write_text(src, encoding="utf-8")
        print("dist/%s" % path.name)


PREVIEW = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>7th&amp;Hill Email Preview</title>
<style>
  :root { --bg:#DEDAD2; --panel:#ECE8E0; --line:#CBC4B7; --ink:#1A1816; --dim:#6B655B; --accent:#7A5E30; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:300 14px/1.5 "Helvetica Neue", Helvetica, Arial, sans-serif; }
  header { position:sticky; top:0; z-index:5; display:flex; flex-wrap:wrap; gap:16px 28px; align-items:center; justify-content:space-between;
           padding:18px 24px; background:rgba(222,218,210,.94); border-bottom:1px solid var(--line); backdrop-filter:blur(6px); }
  h1 { margin:0; font:400 26px/1.2 "Bodoni Moda", Didot, Georgia, serif; }
  h1 small { display:block; margin-top:4px; font:300 10px/1.4 "Helvetica Neue", Arial, sans-serif; letter-spacing:3px; color:var(--dim); }
  .controls { display:flex; flex-wrap:wrap; gap:14px; }
  .seg { display:inline-flex; border:1px solid var(--line); }
  .seg button { appearance:none; border:0; background:transparent; color:var(--dim); padding:8px 14px; cursor:pointer;
                font:400 10px/1 "Helvetica Neue", Arial, sans-serif; letter-spacing:2.5px; text-transform:uppercase; }
  .seg button[aria-pressed="true"] { background:var(--ink); color:var(--bg); }
  .seg button:focus-visible { outline:1px solid var(--accent); outline-offset:2px; }
  main { display:flex; gap:32px; padding:32px 24px 64px; overflow-x:auto; align-items:flex-start; }
  .card { flex:0 0 auto; }
  .meta { margin:0 0 14px; max-width:600px; }
  .meta .label { font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--accent); }
  .meta .file { float:right; font:12px/1.4 ui-monospace, Menlo, monospace; color:var(--dim); }
  .meta .subject { margin-top:6px; font:400 18px/1.3 Georgia, serif; color:var(--ink); }
  .meta .pre { color:var(--dim); font-size:12px; }
  .frame { border:1px solid var(--line); background:var(--panel); }
  iframe { display:block; border:0; width:600px; height:900px; background:#DEDAD2; }
  footer { padding:0 24px 40px; color:var(--dim); font-size:12px; }
  @media (max-width:700px) { main { flex-direction:column; } iframe { width:100% !important; } .card { width:100%; } }
</style>
</head>
<body>
<header>
  <h1>7th&amp;Hill <small>Klaviyo templates · preview</small></h1>
  <div class="controls">
    <div class="seg" data-key="width" aria-label="Width">
      <button data-v="600" aria-pressed="true">Desktop</button><button data-v="375">Mobile</button>
    </div>
    <div class="seg" data-key="theme" aria-label="Theme">
      <button data-v="light" aria-pressed="true">Light</button><button data-v="dark">Dark mode</button>
    </div>
    <div class="seg" data-key="name" aria-label="First name">
      <button data-v="named" aria-pressed="true">With name</button><button data-v="anon">No name</button>
    </div>
    <div class="seg" data-key="zoom" aria-label="Zoom">
      <button data-v="1" aria-pressed="true">100%</button><button data-v="0.75">75%</button><button data-v="0.5">50%</button>
    </div>
  </div>
</header>
<main id="grid"></main>
<footer>Generated by scripts/build.py. Dark mode applies the templates' own prefers-color-scheme styles (as Apple Mail does). Sample name and address are placeholders.</footer>
<script>
  const DATA = /*DATA*/[];
  const state = { width: "600", theme: "light", name: "named", zoom: "1" };
  const grid = document.getElementById("grid");

  function source(c) {
    let s = c[state.name];
    if (state.theme === "dark") s = s.replace(/@media\s*\(prefers-color-scheme:\s*dark\)/g, "@media all");
    return s;
  }
  function fit(f) {
    try { f.style.height = f.contentDocument.documentElement.scrollHeight + "px"; } catch (e) {}
  }
  function render() {
    grid.innerHTML = "";
    DATA.forEach(c => {
      const card = document.createElement("section");
      card.className = "card";
      card.style.zoom = state.zoom;
      card.innerHTML = '<div class="meta" style="width:' + state.width + 'px"><span class="file"></span><div class="label"></div>' +
                       '<div class="subject"></div><div class="pre"></div></div><div class="frame"><iframe></iframe></div>';
      card.querySelector(".file").textContent = c.file + " · " + c.kb + " KB";
      card.querySelector(".label").textContent = c.label;
      card.querySelector(".subject").textContent = c.subject;
      card.querySelector(".pre").textContent = c.preheader;
      const f = card.querySelector("iframe");
      f.title = c.label;
      f.style.width = state.width + "px";
      f.addEventListener("load", () => { fit(f); setTimeout(() => fit(f), 600); });
      f.srcdoc = source(c);
      grid.appendChild(card);
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
    ap.add_argument("--base-url", help="public folder URL where assets/images/* are hosted")
    args = ap.parse_args()
    build_preview()
    if args.base_url:
        build_dist(args.base_url)
