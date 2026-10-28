#!/usr/bin/env python3
"""7th & Hill letters: every template in templates/ and every snippet in blocks/ is written by this file.

    python3 scripts/compose.py && python3 scripts/build.py

Shared blocks (top bar, photo with seal, titles, buttons, collages, notes, footer) are defined once below,
then each letter is a short list of blocks with Sally's copy. Edit the copy here and re-run, so all
letters stay in step. Pieces come from assets/catalog.json (numbers 1-32 = photo catalog, 101+ = extra
packshots, 201+ = worn photos) or by code from the site set in assets/products/ (R012 = ring no. 12, see products.html).
"""
import os, json, re, csv, shutil
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "assets", "catalog.json"))).items()}
SITE = "https://www.7thandhilljewelry.ca"
SHOP = SITE + "/collections"; DYO = SITE + "/collections/design-your-own-jewelry"
STORY = SITE + "/pages/about-salt"; CARE = SITE + "/pages/jewelry-care"; CONTACT = SITE + "/pages/contact"
IG = "https://www.instagram.com/7thandhilljewelry"; TT = "https://www.tiktok.com/@7thandhilljewelry"
IMG = "../assets/images/"
SITE_SET = {r["code"]: r for r in csv.DictReader(open(os.path.join(ROOT, "assets", "products", "index.csv"))) if r["code"]}

OUTER = "#101613"; PAGE = "#FFFFFF"; INK = "#2E2A26"; BODY = "#4A463F"; SOFT = "#8A857C"
GOLD = "#9C7E4A"; LINE = "#E6E2DB"; GREEN = "#58744E"; GREEN_L = "#9DB092"; BAR = "#111111"
NIGHT = "#111815"; IVORY = "#EDE8DF"; GOLD_L = "#C9A96A"; NDIM = "#9AA59F"
DISPLAY = "Cormorant, 'Cormorant Garamond', Georgia, 'Times New Roman', serif"   # the site: headings
SANS = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"                   # the site: body text
WORDMARK = "Montserrat, 'Helvetica Neue', Helvetica, Arial, sans-serif"          # the site: text logo, medium

def size(src):
    w, h = Image.open(os.path.join(ROOT, "assets/images", src)).size
    return w, h

HEAD = """<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>@@TITLE@@</title>
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
<style>
  .display { font-family: Georgia, 'Times New Roman', serif !important; }
  .sans { font-family: Arial, Helvetica, sans-serif !important; }
</style>
<![endif]-->
<!--[if !mso]><!-->
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500&amp;family=Inter:wght@400;500&amp;family=Montserrat:wght@500&amp;display=swap" rel="stylesheet">
<!--<![endif]-->
<style>
  :root { color-scheme: light; supported-color-schemes: light; }
  html, body { margin: 0 !important; padding: 0 !important; width: 100% !important; }
  body { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
  table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
  img { border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
  a { text-decoration: none; }
  a[x-apple-data-detectors], u + #body a, #MessageViewBody a { color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }
  .legal a { color: #9A9A9A !important; text-decoration: underline !important; }
  @media screen and (max-width: 599px) {
    .px { padding-left: 28px !important; padding-right: 28px !important; }
    .pxs { padding-left: 16px !important; padding-right: 16px !important; }
    .h1 { font-size: 32px !important; line-height: 38px !important; }
    .t-sm { font-size: 10px !important; letter-spacing: 1.5px !important; }
    .pname { font-size: 17px !important; line-height: 21px !important; }
    .ptext { padding-left: 8px !important; padding-right: 8px !important; }
    .tname { font-size: 15px !important; line-height: 19px !important; }
  }
</style>
</head>
"""

def open_body(title, preheader):
    filler = "&#8199;&#847;" * 70
    return f"""<body id="body" style="margin:0; padding:0; background-color:{OUTER};">
  <!-- PREHEADER: the line shown after the subject in the inbox -->
  <div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">{preheader}</div>
  <div style="display:none; font-size:1px; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">{filler}</div>

  <div role="article" aria-roledescription="email" aria-label="{title}" lang="en" style="background-color:{OUTER};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{OUTER}" style="background-color:{OUTER};">
    <tr>
      <td align="center" style="padding:0;">
        <!--[if mso]><table role="presentation" width="600" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{PAGE}" style="width:100%; max-width:600px; margin:0 auto; background-color:{PAGE};">
"""
CLOSE_BODY = """        </table>
        <!--[if mso]></td></tr></table><![endif]-->
      </td>
    </tr>
  </table>
  </div>
</body>
</html>
"""

def block(name, inner, pad="0 64px", cls="px", align="center", bg=None):
    bgs = f' bgcolor="{bg}"' if bg else ""
    bgc = f" background-color:{bg};" if bg else ""
    return f"""
          <!-- ═══════════ BLOCK: {name} ═══════════ -->
          <tr>
            <td class="{cls}"{bgs} align="{align}" style="padding:{pad};{bgc}">
{inner}            </td>
          </tr>
"""

def topbar():
    return f"""
          <!-- ═══════════ BLOCK: TOP BAR ═══════════ -->
          <tr>
            <td bgcolor="{BAR}" align="center" style="padding:14px 24px; background-color:{BAR};">
              <a class="sans" href="{SITE}" target="_blank" style="font-family:{WORDMARK}; font-size:11px; line-height:14px; font-weight:500; letter-spacing:5px; text-transform:uppercase; color:#FFFFFF; text-decoration:none;">7th &amp; Hill</a>
            </td>
          </tr>
"""

def hero(src, alt, href=SITE):
    w, h = size(src)
    return f"""
          <!-- ═══════════ BLOCK: HERO · photo with the round logo on its lower edge ═══════════
               The logo is part of the image ({src}), so no email client can move or hide it.
               New photo: see README, "Hero images". -->
          <tr>
            <td style="padding:0;">
              <a href="{href}" target="_blank" style="display:block; text-decoration:none;"><img src="{IMG}{src}" width="600" height="{round(h * 600 / w)}" alt="{alt}" style="display:block; width:100%; max-width:600px; height:auto; border:0; background-color:#EEEEEE; color:{SOFT}; font-family:{SANS}; font-size:12px;"></a>
            </td>
          </tr>
"""

def star(mt=0, mb=0, color=GOLD):
    """The 7th & Hill sunburst (from the book box), used as the brand's divider."""
    src = "sunburst-light.png" if color == GOLD_L else "sunburst-gold.png"
    return f"""              <img src="{IMG}{src}" width="40" height="20" alt="" style="display:block; width:40px; height:20px; margin:{mt}px auto {mb}px; border:0;">
"""

def dot(light=False):
    src = "sunburst-dot-light.png" if light else "sunburst-dot.png"
    return f'<img src="{IMG}{src}" width="14" height="7" alt="" style="display:block; width:14px; height:7px; border:0; margin-top:8px;">'

def eyebrow(text, mb=12, color=GOLD):
    return f"""              <p class="sans" style="margin:0 0 {mb}px; font-family:{SANS}; font-size:11px; line-height:16px; font-weight:400; letter-spacing:3.5px; text-transform:uppercase; color:{color};">{text}</p>
"""


def h1(text, mb=16, color=INK, size_=36):
    return f"""              <h1 class="display h1" style="margin:0 0 {mb}px; font-family:{DISPLAY}; font-size:{size_}px; line-height:{size_ + 6}px; font-weight:400; color:{color};">{text}</h1>
"""

def goldline(mt=0, mb=22, w=36):
    return f"""              <table role="presentation" width="{w}" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:{mt}px auto {mb}px;">
                <tr><td height="1" style="height:1px; border-top:1px solid {GOLD}; font-size:0; line-height:0;">&nbsp;</td></tr>
              </table>
"""

def p(text, mb=14, color=BODY, size_=15, lh=26, align="center"):
    return f"""              <p class="sans" style="margin:0 0 {mb}px; font-family:{SANS}; font-size:{size_}px; line-height:{lh}px; font-weight:400; color:{color}; text-align:{align};">{text}</p>
"""

def quote(text, color=IVORY, mb=0):
    return f"""              <p class="display" style="margin:0 0 {mb}px; font-family:{DISPLAY}; font-size:28px; line-height:34px; color:{color};">{text}</p>
"""

def title_block(eyebrow_text, title, text=None, pt=18):
    inner = (eyebrow(eyebrow_text) if eyebrow_text else "") + h1(title) + goldline()
    if text:
        inner += p(text, mb=0)
    return block("TITLE · eyebrow + headline + text", inner, pad=f"{pt}px 64px 34px")

def button(label, href, mt=0, mb=0):
    return f"""              <!-- BUTTON: edit label and href -->
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:{mt}px auto {mb}px;">
                <tr>
                  <td bgcolor="{GREEN}" style="background-color:{GREEN}; padding:3px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td align="center" style="border:1px solid {GREEN_L}; mso-padding-alt:0;">
                          <a class="sans" href="{href}" target="_blank" style="display:inline-block; padding:16px 40px; font-family:{SANS}; font-size:12px; line-height:14px; font-weight:400; letter-spacing:3px; text-transform:uppercase; color:#F7F5F1; text-decoration:none; mso-padding-alt:0;"><!--[if mso]><i style="letter-spacing:34px; mso-font-width:-100%; mso-text-raise:20pt;" hidden>&nbsp;</i><![endif]--><span style="mso-text-raise:10pt;">{label}</span><!--[if mso]><i style="letter-spacing:34px; mso-font-width:-100%;" hidden>&nbsp;</i><![endif]--></a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
"""

def cta(label, href, pad="6px 64px 34px", extra=""):
    return block("CTA · button", button(label, href) + extra, pad=pad)

def text_link(label, href, mt=16, color=INK, line=GOLD):
    return f"""              <p class="sans" style="margin:{mt}px 0 0; font-family:{SANS}; font-size:11px; line-height:14px; letter-spacing:2.5px; text-transform:uppercase;"><a href="{href}" target="_blank" style="color:{color}; text-decoration:none; border-bottom:1px solid {line}; padding-bottom:2px;">{label}</a></p>
"""

def ps(text):
    return block("P.S. · Sally", p(f'<span style="font-weight:400; color:{INK};">P.S.</span> {text}', mb=0, size_=14, lh=23, align="left"), pad="0 40px 30px")

# ── images inside collages
ANIM = {  # animated grid cells: cross-fade between pieces (GIF; Outlook for Windows shows the first one)
    "rings": ("anim-rings.gif", "Rings", SITE + "/search?q=ring"),
    "charms": ("anim-charms.gif", "Charms", SITE + "/search?q=charm"),
    "pendants": ("anim-pendants.gif", "Pendants", SITE + "/search?q=pendant"),
    "earrings": ("anim-earrings.gif", "Earrings", SITE + "/search?q=earrings"),
    "necklaces": ("anim-necklaces.gif", "Necklaces", SITE + "/search?q=necklace"),
    "w3-rings": ("anim-w3-rings.gif", "Marquise Art Deco Ring, Art Deco Sunburst Ring, Custom Date Ring", SITE + "/search?q=ring"),
    "w3-hearts": ("anim-w3-hearts.gif", "Radiant Sunburst Heart, Hand &amp; Footprint Heart", SITE + "/search?q=heart"),
}

def is_anim(n):
    return isinstance(n, str) and n in ANIM

def short_name(title):
    """Site titles lead with the metal; the letters name the piece."""
    t = re.sub(r"^(The )?(Solid )?(1[048]k )?(Solid )?(Italian )?(Gold )?(And |& )?", "", title, flags=re.I).strip()
    return t[:1].upper() + t[1:] if t else title

def site_piece(code):
    """A piece from assets/products/ by its code: the tile is copied into assets/images/ for the letters."""
    m = re.fullmatch(r"([A-Za-z]+)0*(\d+)", code.strip())
    assert m and f"{m[1].upper()}{int(m[2]):03d}" in SITE_SET, f"{code}: no such code in products.html"
    r = SITE_SET[f"{m[1].upper()}{int(m[2]):03d}"]
    img = f"site-{r['code']}.jpg"
    dst = os.path.join(ROOT, "assets", "images", img)
    if not os.path.exists(dst):
        shutil.copyfile(os.path.join(ROOT, "assets", "products", r["file"]), dst)
    return {"name": short_name(r["title"]), "url": r["url"], "img": img}

def piece(n):
    """n = catalog number or site code (R012), or (number or code, display name) to rename a piece in one letter."""
    if isinstance(n, tuple):
        d = dict(piece(n[0])); d["name"] = n[1]
        return d
    if isinstance(n, str) and not is_anim(n):
        return site_piece(n)
    if isinstance(n, str):   # animated cell: named after the kind of piece it cycles through
        src, alt, url = ANIM[n]
        return {"name": alt, "url": url, "img": src}
    return P[n]

def pimg(n, w):
    if is_anim(n):
        src, alt, url = ANIM[n]
        return f'<a href="{url}" target="_blank" style="display:block; text-decoration:none;"><img src="{IMG}{src}" width="{w}" height="{w}" alt="{alt}" style="display:block; width:100%; max-width:{w}px; height:auto; border:0; background-color:#E9EDF1; color:{SOFT}; font-family:{SANS}; font-size:11px;"></a>'
    pr = piece(n)
    return f'<a href="{pr["url"]}" target="_blank" style="display:block; text-decoration:none;"><img src="{IMG}{pr["img"]}" width="{w}" height="{w}" alt="{pr["name"]}" style="display:block; width:100%; max-width:{w}px; height:auto; border:0; background-color:#E9EDF1; color:{SOFT}; font-family:{SANS}; font-size:11px;"></a>'

def fimg(src, w, alt, href=SHOP):
    return f'<a href="{href}" target="_blank" style="display:block; text-decoration:none;"><img src="{IMG}{src}" width="{w}" height="{w}" alt="{alt}" style="display:block; width:100%; max-width:{w}px; height:auto; border:0; background-color:#E9EDF1; color:{SOFT}; font-family:{SANS}; font-size:11px;"></a>'

def collage(name, small_pair, feature, row, feature_side="right"):
    """Collage: two small pieces stacked + one large photo, then a row of three pieces.
    small_pair / row: product numbers from blocks/catalog.md; feature: (image, alt, link)."""
    a, b = small_pair
    side = f"""<td width="33.33%" valign="top" style="padding:4px;">{pimg(a, 172)}</td>""", None
    left_stack = f"""                    <td width="33.33%" valign="top" style="padding:0;">
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr><td style="padding:4px;">{pimg(a, 172)}</td></tr>
                        <tr><td style="padding:4px;">{pimg(b, 172)}</td></tr>
                      </table>
                    </td>
"""
    big = f"""                    <td width="66.67%" valign="top" style="padding:4px;">{fimg(feature[0], 352, feature[1], feature[2])}</td>
"""
    top = left_stack + big if feature_side == "right" else big + left_stack
    cells = "".join(f"""                    <td width="33.33%" valign="top" style="padding:4px;">{pimg(n, 172)}</td>
""" for n in row)
    return f"""
          <!-- ═══════════ BLOCK: {name} · collage ═══════════
               Pieces link to their product pages. To swap a piece, change the product image
               (assets/images/product-NN.jpg), its alt and its link (all 32 in blocks/catalog.md).
               anim-*.gif cells cross-fade between several pieces (Outlook for Windows shows the first). -->
          <tr>
            <td class="pxs" align="center" style="padding:0 26px 26px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
{top}                </tr>
              </table>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
{cells}                </tr>
              </table>
            </td>
          </tr>
"""

def checker(name, ids):
    """Alternating rows: piece photo on one side, its name on the other (K2 layout)."""
    assert not any(is_anim(i) for i in ids), f"{name}: named rows need named pieces"
    rows = ""
    for i, n in enumerate(ids):
        pr = piece(n)
        img = f"""                    <td width="50%" valign="middle" style="padding:0;">{pimg(n, 270)}</td>
"""
        txt = f"""                    <td class="ptext" width="50%" valign="middle" align="center" style="padding:10px 18px;">
                      <p class="display pname" style="margin:0 0 12px; font-family:{DISPLAY}; font-size:22px; line-height:25px; color:{INK};"><a href="{pr['url']}" target="_blank" style="color:{INK}; text-decoration:none;">{pr['name']}</a></p>
                      <p class="sans t-sm" style="margin:0; font-family:{SANS}; font-size:10px; line-height:14px; letter-spacing:2.5px; text-transform:uppercase;"><a href="{pr['url']}" target="_blank" style="color:{INK}; text-decoration:none; border-bottom:1px solid {GOLD}; padding-bottom:2px;">View piece</a></p>
                    </td>
"""
        rows += "                <tr>\n" + (img + txt if i % 2 == 0 else txt + img) + "                </tr>\n"
    return f"""
          <!-- ═══════════ BLOCK: {name} · pieces with names ═══════════
               Each row: photo + name, sides alternate. Add or delete whole <tr> rows. -->
          <tr>
            <td class="pxs" align="center" style="padding:0 30px 30px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{rows}              </table>
            </td>
          </tr>
"""

def row3(name, ids):
    cells = ""
    for n in ids:
        pr = piece(n)
        cells += f"""                    <td width="33.33%" valign="top" align="center" style="padding:4px 4px 0;">
                      {pimg(n, 172)}
                      <p class="display tname" style="margin:12px 0 0; font-family:{DISPLAY}; font-size:18px; line-height:21px; color:{INK};"><a href="{pr['url']}" target="_blank" style="color:{INK}; text-decoration:none;">{pr['name']}</a></p>
                    </td>
"""
    return f"""
          <!-- ═══════════ BLOCK: {name} · three pieces with names ═══════════ -->
          <tr>
            <td class="pxs" align="center" style="padding:0 26px 30px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
{cells}                </tr>
              </table>
            </td>
          </tr>
"""

def night(name, inner, pad="40px 56px 46px", sun=True):
    return block(name + " (night band)", (star(mb=18, color=GOLD_L) if sun else "") + inner, pad=pad, bg=NIGHT)

def vault_key():
    """15% welcome code. In Klaviyo create a coupon named VAULT15: unique codes, single use, 30 days,
    does not combine with sale prices. Never type a code by hand."""
    return night("YOUR KEY · VAULT15 unique coupon",
        eyebrow("Your key", mb=10, color=GOLD_L)
        + h1("15% off your first piece", mb=22, color=IVORY, size_=32)
        + f"""              <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto 18px;">
                <tr><td align="center" style="border:1px solid {GOLD_L}; padding:14px 30px;">
                  <p class="sans" style="margin:0; font-family:{SANS}; font-size:18px; line-height:22px; letter-spacing:5px; color:{IVORY};">{{% coupon_code 'VAULT15' %}}</p>
                </td></tr>
              </table>
"""
        + p("Use it once, within 30 days. It does not combine with sale prices.", mb=22, color=NDIM, size_=13, lh=21)
        + night_list([
            ("First looks at every new collection", ""),
            ("First word on private and flash sales", ""),
            ("Complimentary jewelry cleaning in the GTA", ""),  # waiting for Sally: keep or remove
            ("A private invitation to design a piece with me", ""),
          ], numerals=["i", "ii", "iii", "iv"]))

def night_list(items, numerals=None):
    rows = ""
    for i, (t, d) in enumerate(items):
        top = f"border-top:1px solid #26302B; " if i == 0 else ""
        mark = (f'<p class="display" style="margin:0; font-family:{DISPLAY}; font-size:21px; line-height:26px; color:{GOLD_L};">{numerals[i]}</p>'
                if numerals else dot(True))
        rows += f"""                <tr>
                  <td width="30" valign="top" style="{top}border-bottom:1px solid #26302B; padding:14px 0;">{mark}</td>
                  <td valign="top" style="{top}border-bottom:1px solid #26302B; padding:14px 0;">
                    <p class="display" style="margin:0 0 2px; font-family:{DISPLAY}; font-size:23px; line-height:26px; color:{IVORY};">{t}</p>
                    {f'<p class="sans" style="margin:0; font-family:{SANS}; font-size:14px; line-height:22px; font-weight:400; color:{NDIM};">{d}</p>' if d else ''}
                  </td>
                </tr>
"""
    return f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="text-align:left;">
{rows}              </table>
"""

def light_list(items):
    rows = ""
    for i, (t, d) in enumerate(items):
        top = f"border-top:1px solid {LINE}; " if i == 0 else ""
        rows += f"""                <tr>
                  <td width="30" valign="top" style="{top}border-bottom:1px solid {LINE}; padding:14px 0;">{dot()}</td>
                  <td valign="top" style="{top}border-bottom:1px solid {LINE}; padding:14px 0;">
                    <p class="display" style="margin:0 0 2px; font-family:{DISPLAY}; font-size:23px; line-height:26px; color:{INK};">{t}</p>
                    <p class="sans" style="margin:0; font-family:{SANS}; font-size:14px; line-height:22px; font-weight:400; color:{BODY};">{d}</p>
                  </td>
                </tr>
"""
    return f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="text-align:left;">
{rows}              </table>
"""

# Necklaces and Chains are separate collections on the site (Sally), so seven tiles: the last one spans the row
CATS_DEFAULT = CATS = [("Charms &amp; talismans", SITE + "/search?q=charm"), ("Necklaces", SITE + "/collections/necklaces"),
        ("Chains", SITE + "/collections/chains-2"), ("Rings", SITE + "/collections/rings"),
        ("Earrings", SITE + "/collections/earrings"), ("Bracelets", SITE + "/collections/bracelets"),
        ("Personalized", SITE + "/collections/personalized-jewelry")]

def find_your_piece(title="Find your piece", cats=None):
    CATS = cats or CATS_DEFAULT
    cell = lambda t, u, span=1: f"""<td width="{50 * span}%"{' colspan="2"' if span > 1 else ''} style="padding:4px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="border:1px solid {GREEN}; padding:13px 6px;"><a class="sans t-sm" href="{u}" target="_blank" style="font-family:{SANS}; font-size:11px; line-height:14px; letter-spacing:2px; text-transform:uppercase; color:{GREEN}; text-decoration:none;">{t}</a></td></tr></table></td>"""
    rows = "".join(f"""                <tr>{cell(*CATS[i])}{cell(*CATS[i + 1])}</tr>
""" for i in range(0, len(CATS) - 1, 2))
    if len(CATS) % 2:  # an odd tile out spans the whole row
        rows += f"""                <tr>{cell(*CATS[-1], span=2)}</tr>
"""
    return block("FIND YOUR PIECE · categories", f"""              <p class="display" style="margin:0 0 14px; font-family:{DISPLAY}; font-size:26px; line-height:30px; color:{GREEN};">{title}</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{rows}              </table>
""", pad="4px 36px 30px", cls="pxs")

def cat_line():
    links = " &nbsp;&middot;&nbsp; ".join(f'<a href="{u}" target="_blank" style="color:{INK}; text-decoration:none;">{t.replace("&amp; talismans","").strip()}</a>' for t, u in CATS)
    return block("CATEGORY LINE", f"""              <p class="sans t-sm" style="margin:0; font-family:{SANS}; font-size:10px; line-height:22px; letter-spacing:2px; text-transform:uppercase; color:{INK};">{links}</p>
""", pad="0 24px 22px", cls="pxs")

def footer(reason):
    return f"""
          <!-- ═══════════ BLOCK: FOOTER (sender name, contact, unsubscribe; no street address: Sally's is her home, add a business mailing address here when there is one) ═══════════ -->
          <tr>
            <td bgcolor="{BAR}" style="padding:16px 24px; background-color:{BAR};">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td class="sans t-sm" align="left" style="font-family:{SANS}; font-size:11px; line-height:14px; letter-spacing:2px; text-transform:uppercase;"><a href="{SITE}" target="_blank" style="color:#F7F5F1; text-decoration:none;">7thandhilljewelry.ca</a></td>
                  <td class="sans t-sm" align="right" style="font-family:{SANS}; font-size:11px; line-height:14px; letter-spacing:2px; text-transform:uppercase;"><a href="{IG}" target="_blank" style="color:#F7F5F1; text-decoration:none;">Instagram</a>&nbsp;&nbsp;&nbsp;<a href="{TT}" target="_blank" style="color:#F7F5F1; text-decoration:none;">TikTok</a></td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" style="padding:24px 40px 30px;">
              <img src="{IMG}sunburst-gold.png" width="40" height="20" alt="" style="display:block; width:40px; height:20px; margin:0 auto 12px; border:0;">
              <p class="display" style="margin:0 0 10px; font-family:{DISPLAY}; font-size:15px; line-height:20px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{GREEN};">Modern Heirlooms.<br>Timeless Classics.</p>
              <p class="sans" style="margin:0 0 10px; font-family:{SANS}; font-size:12px; line-height:18px; font-weight:400;"><a href="mailto:hello@7thandhilljewelry.ca" style="color:{INK}; text-decoration:none;">hello@7thandhilljewelry.ca</a></p>
              <p class="sans legal" style="margin:0; font-family:{SANS}; font-size:11px; line-height:17px; font-weight:400; color:#9A958B;">
                7th &amp; Hill Jewelry<br>
                {reason}<br>
                {{% unsubscribe %}} &nbsp;&middot;&nbsp; {{% manage_preferences %}}
              </p>
            </td>
          </tr>
"""

SUB = "You're receiving this because you subscribed at 7thandhilljewelry.ca or shopped with us."
VAULT = "You're receiving this because you joined the 7H Vault at 7thandhilljewelry.ca."
SALT_REASON = "You're receiving this as a former SALT Fine Jewelry client of Sally's."

FROM = "Sally at 7th & Hill <hello@7thandhilljewelry.ca> · replies to hello@7thandhilljewelry.ca"
GROUPS = {"flow": "Flows · live from Tue, Oct 27 (automatic)",
          "salt": "SALT list · from Tue, Oct 27",
          "camp": "Campaigns · by date"}
READY, DRAFT = "Ready for Sally", "Draft, not yet approved by Sally"
WRITTEN = []

def doc(fname, *, code, flow, pos, when, card, label=None, title, subject, preheader, body, status=READY,
        reason=SUB, logic=(), notes=(), page=False):
    """Write one letter. The comment header is what the preview reads: stage, card label, status, logic."""
    group = GROUPS[fname.split("-", 1)[0]]
    lines = [f"  {group} · {flow} · {code} ({pos}) · {when}",
             f"  Card: {label or code + ' · ' + card}",
             f"  Status: {status}",
             f"  Subject: {subject}",
             f"  Preheader: {preheader}",
             f"  From: {FROM}"]
    lines += [f"  Logic: {l}" for l in logic]
    lines += [f"  Note: {n}" for n in notes]
    lines += ["  Images use relative paths (../assets/images/) for local preview.",
              f"  Ready-to-paste copy with hosted images: klaviyo/{fname}"]
    top = "<!--\n" + "\n".join(lines) + "\n-->\n"
    html = top + (body if page else HEAD.replace("@@TITLE@@", title) + open_body(title, preheader) + topbar() + body + footer(reason) + CLOSE_BODY)
    with open(os.path.join(ROOT, "templates", fname), "w") as fh:
        fh.write(html)
    WRITTEN.append(fname)

FN = "{{ first_name|default:'' }}"
def greet(yes, no):
    return f"{{% if first_name %}}{yes}{{% else %}}{no}{{% endif %}}"


def masthead(issue, theme):
    """Series masthead: the same in every issue so readers recognise it at a glance.
    Issue number and theme live in the subject line only."""
    return block("MASTHEAD · Sally's edit",
        h1("Sally&rsquo;s edit", mb=16, size_=43)
        + goldline(mb=0), pad="26px 40px 26px")

def sally_note(text):
    """Sally's short note with her round portrait; signed in the headline font."""
    return block("SALLY'S NOTE · 2 to 3 sentences, in Sally's voice", f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="72" valign="top" style="padding:2px 16px 0 0;"><img src="{IMG}sally-avatar.png" width="56" height="56" alt="Sally Brooks" style="display:block; width:56px; height:56px; border:0;"></td>
                  <td valign="top" style="text-align:left;">
                    <p class="sans" style="margin:0 0 10px; font-family:{SANS}; font-size:15px; line-height:26px; font-weight:400; color:{BODY};">{text}</p>
                    <p class="display" style="margin:0; font-family:{DISPLAY}; font-size:24px; line-height:26px; color:{INK};">Sally</p>
                  </td>
                </tr>
              </table>
""", pad="28px 56px 34px")


# ───────── more shared blocks
VAULT_PAGE = SITE + "/pages/7h-vault"
MAIL = "mailto:hello@7thandhilljewelry.ca"
CHECKOUT = "{{ event.extra.checkout_url|default:'https://www.7thandhilljewelry.ca/cart' }}"   # Started Checkout (Shopify)
CART_URL = "{{ event.CheckoutURL|default:'https://www.7thandhilljewelry.ca/cart' }}"          # Added to Cart

def utm(url, campaign, content):
    return f"{url}?utm_source=klaviyo&amp;utm_medium=email&amp;utm_campaign={campaign}&amp;utm_content={content}"

def logo_header():
    return f"""
          <!-- ═══════════ BLOCK: SEAL · for letters that open without a photo ═══════════ -->
          <tr>
            <td align="center" style="padding:30px 24px 6px;">
              <a href="{SITE}" target="_blank" style="display:inline-block; text-decoration:none;"><img src="{IMG}seal.png" width="78" height="78" alt="7th &amp; Hill Jewelry" style="display:block; width:78px; height:78px; border:0; margin:0 auto;"></a>
            </td>
          </tr>
"""

def caption(text, pad="12px 40px 0"):
    return block("CAPTION", f"""              <p class="sans" style="margin:0; font-family:{SANS}; font-size:11px; line-height:17px; letter-spacing:2px; text-transform:uppercase; color:{SOFT};">{text}</p>
""", pad=pad)

def heading(eyebrow_text, title=None, pad="6px 40px 20px"):
    inner = eyebrow(eyebrow_text, mb=8 if title else 0)
    if title:
        inner += h1(title, mb=0, size_=28)
    return block("HEADING", inner, pad=pad)

def tagline(pad="6px 40px 20px", color=GREEN):
    """The brand line in Cormorant capitals on two lines, as on Sally's brand font sheet."""
    return block("TAGLINE", f"""              <p class="display" style="margin:0; font-family:{DISPLAY}; font-size:17px; line-height:23px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{color};">Modern Heirlooms.<br>Timeless Classics.</p>
""", pad=pad)

def letter(paras, pad="6px 48px 30px", sign=True, ps=None):
    """Sally's words beside her round portrait, signed, like her notes in Sally's edit."""
    body = "".join(f'<p class="sans" style="margin:0 0 14px; font-family:{SANS}; font-size:15px; line-height:26px; font-weight:400; color:{BODY};">{t}</p>' for t in paras)
    if sign:
        body += (f'<p class="display" style="margin:4px 0 0; font-family:{DISPLAY}; font-size:28px; line-height:30px; color:{INK};">Sally</p>'
                 f'<p class="sans t-sm" style="margin:2px 0 0; font-family:{SANS}; font-size:10px; line-height:15px; letter-spacing:2.5px; text-transform:uppercase; color:{SOFT};">Sally Brooks &middot; Founder &amp; designer</p>')
    if ps:
        body += f'<p class="sans" style="margin:16px 0 0; font-family:{SANS}; font-size:14px; line-height:23px; font-weight:400; color:{BODY};"><span style="font-weight:400; color:{INK};">P.S.</span> {ps}</p>'
    return block("LETTER · Sally's words", f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="72" valign="top" style="padding:4px 16px 0 0;"><img src="{IMG}sally-avatar.png" width="56" height="56" alt="Sally Brooks" style="display:block; width:56px; height:56px; border:0;"></td>
                  <td valign="top" style="text-align:left;">{body}</td>
                </tr>
              </table>
""", pad=pad, align="left")

def facts_band(rows):
    """Facts in the dark band, as in the approved letters (title on top, line under it)."""
    return night("FACTS", night_list(rows), pad="34px 56px 40px")

def signature(align="left", pad="0 56px 28px"):
    return block("SIGNATURE · Sally", f"""              <p class="display" style="margin:0; font-family:{DISPLAY}; font-size:35px; line-height:38px; color:{INK}; text-align:{align};">Sally</p>
              <p class="sans t-sm" style="margin:2px 0 0; font-family:{SANS}; font-size:10px; line-height:15px; letter-spacing:2.5px; text-transform:uppercase; color:{SOFT}; text-align:{align};">Sally Brooks &middot; Founder &amp; designer</p>
""", pad=pad, align=align)

def line(text, pad="0 56px 24px", size_=15, color=BODY):
    return block("LINE", p(text, mb=0, size_=size_, color=color), pad=pad)

def facts(name, rows, pad="0 48px 32px"):
    trs = ""
    for i, (k, v) in enumerate(rows):
        top = f"border-top:1px solid {LINE}; " if i == 0 else ""
        trs += f"""                <tr>
                  <td width="30%" valign="top" style="{top}border-bottom:1px solid {LINE}; padding:14px 12px 14px 0;"><p class="sans" style="margin:0; font-family:{SANS}; font-size:11px; line-height:22px; letter-spacing:2px; text-transform:uppercase; color:{GOLD};">{k}</p></td>
                  <td valign="top" style="{top}border-bottom:1px solid {LINE}; padding:14px 0;"><p class="sans" style="margin:0; font-family:{SANS}; font-size:14px; line-height:22px; font-weight:400; color:{BODY};">{v}</p></td>
                </tr>
"""
    return block(name + " · facts", f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="text-align:left;">
{trs}              </table>
""", pad=pad)

def grid(name, items, cols=3, captions=None):
    """Pieces in rows of 2 or 3, name under each (and an optional line, e.g. who it is for).
    Every card shows a real piece name, so animated cells belong in collages, not here."""
    assert not any(is_anim(i) for i in items), f"{name}: grid cards need named pieces"
    w, pct = (172, "33.33%") if cols == 3 else (262, "50%")
    rows = ""
    for r in range(0, len(items), cols):
        cells = ""
        for k in range(r, min(r + cols, len(items))):
            pr = piece(items[k])
            cap = (f'<p class="sans" style="margin:4px 0 0; font-family:{SANS}; font-size:13px; line-height:19px; font-weight:400; color:{SOFT};">{captions[k]}</p>'
                   if captions else "")
            cells += f"""                    <td width="{pct}" valign="top" align="center" style="padding:4px 4px 18px;">
                      {pimg(items[k], w)}
                      <p class="display tname" style="margin:12px 0 0; font-family:{DISPLAY}; font-size:18px; line-height:21px; color:{INK};"><a href="{pr['url']}" target="_blank" style="color:{INK}; text-decoration:none;">{pr['name']}</a></p>
                      {cap}
                    </td>
"""
        rows += f"                <tr>\n{cells}                </tr>\n"
    return f"""
          <!-- ═══════════ BLOCK: {name} · grid of pieces (numbers in blocks/catalog.md) ═══════════ -->
          <tr>
            <td class="pxs" align="center" style="padding:0 26px 14px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
{rows}              </table>
            </td>
          </tr>
"""

def picture(name, src, w, h, alt, cap=None, pad="0 64px 30px"):
    c = (f'\n              <p class="sans" style="margin:12px 0 0; font-family:{SANS}; font-size:11px; line-height:17px; letter-spacing:2px; text-transform:uppercase; color:{SOFT};">{cap}</p>'
         if cap else "")
    return block(name, f"""              <img src="{IMG}{src}" width="{w}" height="{h}" alt="{alt}" style="display:block; width:100%; max-width:{w}px; height:auto; margin:0 auto; border:0; background-color:#E9EDF1;">{c}
""", pad=pad)

def trust_strip(items=(("Solid gold", "Never tarnishes"), ("Book box", "Ready to give"), ("Duties", "Covered worldwide"))):
    return night("TRUST STRIP", f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
""" + "".join(f"""                  <td width="33%" align="center" valign="top" style="{'border-left:1px solid #26302B; ' if i else ''}padding:2px 6px;">
                    <p class="display tname" style="margin:0 0 4px; font-family:{DISPLAY}; font-size:19px; line-height:22px; color:{IVORY};">{a}</p>
                    <p class="sans t-sm" style="margin:0; font-family:{SANS}; font-size:9px; line-height:13px; letter-spacing:2px; text-transform:uppercase; color:{GOLD_L};">{b}</p>
                  </td>
""" for i, (a, b) in enumerate(items)) + """                </tr>
              </table>
""", pad="28px 30px 28px", sun=False)

def dyn_cart():
    return f"""
          <!-- ═══════════ BLOCK: BAG · Klaviyo dynamic block (Shopify "Added to Cart" event) ═══════════
               Lists the pieces in the bag from event.Items (ProductName, ImageURL, ProductURL).
               Check it in Klaviyo with Preview & test on a real profile before going live. -->
          <tr>
            <td class="px" align="center" style="padding:0 64px 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
              {{% for item in event.Items %}}
                <tr>
                  <td width="120" valign="middle" style="padding:10px 16px 10px 0; border-bottom:1px solid {LINE};"><a href="{{{{ item.ProductURL }}}}" target="_blank" style="text-decoration:none;"><img src="{{{{ item.ImageURL }}}}" width="104" height="104" alt="{{{{ item.ProductName }}}}" style="display:block; width:104px; height:104px; border:0; background-color:#E9EDF1;"></a></td>
                  <td valign="middle" style="padding:10px 0; border-bottom:1px solid {LINE}; text-align:left;"><p class="display" style="margin:0; font-family:{DISPLAY}; font-size:22px; line-height:25px; color:{INK};"><a href="{{{{ item.ProductURL }}}}" target="_blank" style="color:{INK}; text-decoration:none;">{{{{ item.ProductName }}}}</a></p></td>
                </tr>
              {{% endfor %}}
              </table>
            </td>
          </tr>
"""

def dyn_viewed():
    return f"""
          <!-- ═══════════ BLOCK: VIEWED PIECE · Klaviyo dynamic block (Shopify "Viewed Product" event) ═══════════
               Uses event.ProductName, event.ImageURL and event.URL. No copy about the piece itself. -->
          <tr>
            <td class="px" align="center" style="padding:0 64px 26px;">
              <a href="{{{{ event.URL }}}}" target="_blank" style="display:block; text-decoration:none;"><img src="{{{{ event.ImageURL }}}}" width="300" height="300" alt="{{{{ event.ProductName }}}}" style="display:block; width:100%; max-width:300px; height:auto; margin:0 auto; border:0; background-color:#E9EDF1;"></a>
              <p class="display" style="margin:16px 0 0; font-family:{DISPLAY}; font-size:26px; line-height:30px; color:{INK};"><a href="{{{{ event.URL }}}}" target="_blank" style="color:{INK}; text-decoration:none;">{{{{ event.ProductName }}}}</a></p>
            </td>
          </tr>
"""

FACT_GOLD = "Solid gold. It never tarnishes."
FACT_TIMING = "In stock ships in 1 to 2 business days.<br>7th &amp; Hill Exclusives: 2 to 4 weeks.<br>Curated designs: 6 to 8 weeks."
FACT_DELIVERY = "Worldwide shipping. Taxes and duties are covered."
FACT_CARE = f'Three simple habits, on our <a href="{CARE}" target="_blank" style="color:{GOLD_L}; text-decoration:underline;">Jewelry Care page</a>.'
FACT_SIZING = "Not sure about size? Send me a photo of what you already wear, and I&rsquo;ll help you choose."
FACTS_W4 = [("Gold", FACT_GOLD), ("Timing", FACT_TIMING), ("Delivery", FACT_DELIVERY), ("Care", FACT_CARE)]
CATS_W1 = CATS_DEFAULT[:6] + [("Design your own", DYO)]
HI = greet(f"Hi {FN},", "Hello,")

SALT_WAVES = "Daily waves from Tue Oct 27: 200, 400, 800, then 1,500 a day while complaints stay under 0.1% and bounces under 2%"
SALT_LOGIC = [
    "No consent step: T1 is the only SALT letter. The unsubscribe link stays in the footer.",
    SALT_WAVES + ".",
    "After T1, SALT contacts join the campaign audience from K3 (Tue Nov 3). They do not get the welcome flow.",
    "Sunset: SALT contacts with no opens or clicks within 30 days of T1 are suppressed.",
]

# ═════════════════════════ STAGE 1 · goes live Tue Oct 27 ═════════════════════════
# Look of every letter (the approved one): our photo with the seal, a short title, Sally's words in her
# note with the portrait, facts in a dark band, pieces as large photos, the category line at the end.
W = dict(flow="Welcome flow 01")

doc("flow-w1-welcome.html", **W, code="W1", pos="email 1 of 5", when="Right after signup",
    card="Welcome 01 · email 1 of 5 · right after signup",
    title="Welcome to 7th &amp; Hill", subject="Your key to the Vault",
    preheader="15% off your first piece, and first word on every sale.",
    status="Waiting for Sally: GTA cleaning perk, collection tiles", reason=VAULT,
    notes=["Coupon: Klaviyo unique coupon VAULT15 (single use, 30 days, not with sale prices).",
           "Perk iii (complimentary cleaning in the GTA) waits for Sally: keep or remove."],
    body=hero("hero-sally-fireplace.jpg", "Sally Brooks, founder and designer of 7th &amp; Hill, by the fireplace")
    + title_block("The 7H Vault", "Welcome to 7th &amp; Hill",
        "Welcome! I&rsquo;m Sally, and I design modern heirlooms, timeless classics, and personalized jewelry&mdash;one piece, one story at a time. From now on, you&rsquo;ll be among the first to see what leaves the workbench.")
    + heading("First looks from the workbench", pad="0 40px 18px")
    + collage("FIRST LOOKS", (202, "charms"), ("feature-hands.jpg", "Marquise Art Deco rings worn on the hand", P[203]["url"]), ("rings", 16, "necklaces"), feature_side="left")
    + vault_key()
    + cta("Step inside", SHOP, pad="34px 64px 30px")
    + find_your_piece("Find your place", CATS_W1)
    + ps("Reply to this letter anytime. It lands in my inbox, not in a folder nobody reads.").replace("padding:0 40px 30px", "padding:0 40px 14px")
    + signature(pad="0 40px 30px"))

doc("flow-w2-story.html", **W, code="W2", pos="email 2 of 5", when="Day 1 after signup",
    card="Welcome 01 · email 2 of 5 · day 1",
    title="Jewelry should mean something", subject="It started on a corner in Los Angeles",
    preheader="Gold leaf, a sketch, and a necklace I still wear.", reason=VAULT,
    body=hero("hero-archive-building.jpg", "The St. Vincent's Jewelry Center on the corner of 7th and Hill, downtown Los Angeles")
    + caption("The corner of 7th &amp; Hill, downtown Los Angeles")
    + title_block("Our story &middot; Los Angeles, 1962", "Jewelry should mean something.", pt=26)
    + letter(["My dad was a gold leaf letterer at the St. Vincent&rsquo;s Jewelry Center, on the corner of 7th and Hill in downtown Los Angeles.",
              "One afternoon in the eighties, my sister Jen and I watched him sketch a necklace. A jeweler friend carved the wax, and the gold poured like lava. I was nine. We still wear those necklaces today."], sign=False)
    + night("QUOTE", quote("&ldquo;Jewelry is more than metal and stone. It is a work of art, and a wearable memory.&rdquo;"), pad="34px 56px 40px")
    + line("That corner gave the brand its name, and it is still how I work. I listen to your story first, then I design around it.", pad="34px 64px 30px")
    + picture("BOOK BOX · animation", "unboxing.gif", 300, 403, "A 7th &amp; Hill book box opening to show diamond earrings and a ring",
              cap="Your jewellery arrives in our luxurious book packaging featuring velvet lining.")
    + tagline(pad="0 40px 22px")
    + cta("Meet Sally", STORY)
    + cat_line())

doc("flow-w3-find-your-piece.html", **W, code="W3", pos="email 3 of 5", when="Day 3 after signup",
    card="Welcome 01 · email 3 of 5 · day 3",
    title="Find the piece that feels like you", subject="Nine pieces I'd start with",
    preheader="Charms, rings and a locket, chosen by Sally.", reason=VAULT,
    status="Waiting for Sally: nine pieces",
    notes=["Placeholder nine until Sally sends hers (needed by Oct 29). Only pieces with a real price on the site."],
    body=hero("hero-model-sweater-bag.jpg", "A woman in a green sweater wearing a gold enamel pendant, a heart charm necklace and a marquise ring, beside a 7th &amp; Hill bag")
    + title_block("Sally&rsquo;s edit", "Find the piece that feels like you.",
        "Some women start with a charm. Some with a ring they never take off. These are the nine pieces I would start with.")
    + collage("SALLY'S NINE · all nine pieces, the two top cells change", ("w3-rings", "w3-hearts"),
              ("feature-locket.jpg", "Talisman Keepsake Locket, worn", P[201]["url"]),
              ((8, "The Working Scissors"), (28, "The iLove Smartphone"), 104), feature_side="left")
    + cta("See every piece", SHOP, pad="16px 64px 10px")
    + sally_note("Not sure where to start? Reply and tell me who it&rsquo;s for.")
    + cat_line())

doc("flow-w4-worn-and-kept.html", **W, code="W4", pos="email 4 of 5", when="Day 5 after signup",
    card="Welcome 01 · email 4 of 5 · day 5",
    title="Made to be worn. Made to be kept.", subject="Worth knowing before you choose",
    preheader="Solid gold, timing and delivery, in short.", reason=VAULT,
    status="Waiting for Sally: 14k or Solid gold",
    body=hero("hero-lily-bracelet.jpg", "Sally holding her grandmother Lily's gold charm bracelet")
    + title_block("The quiet, important part", "Made to be worn.<br>Made to be kept.",
        "My grandmother Lily wore her charm bracelet from 1913 to 2013. It&rsquo;s why I make pieces for every day, not for a drawer.")
    + facts_band(FACTS_W4)
    + heading("Made personal", pad="34px 40px 18px")
    + checker("MADE PERSONAL", [5, 12, 7])
    + cta("Ask Sally anything", MAIL + "?subject=A%20question%20for%20Sally", pad="4px 64px 12px")
    + line("Or simply reply to this email.", pad="0 64px 30px", size_=13, color=SOFT)
    + cat_line())

doc("flow-w5-help-finding.html", **W, code="W5", pos="email 5 of 5", when="Day 8 after signup",
    card="Welcome 01 · email 5 of 5 · day 8",
    title="Need help finding the one?", subject="Need help finding the one?",
    preheader="Tell me who it's for. I'll pick three.", reason=VAULT,
    body=hero("hero-sally-velvet.jpg", "Sally Brooks in black velvet")
    + title_block(None, "Need help finding the one?")
    + letter([HI,
              "Tell me who it&rsquo;s for and the moment behind it. I&rsquo;ll pick three pieces and tell you why each one fits.",
              "And if what you have in mind doesn&rsquo;t exist yet, we can design it together, one on one.",
              "No pressure, and no follow-up barrage. One honest shortlist."],
             ps="If nothing fits, I&rsquo;m happy to suggest other options.")
    + collage("THREE TO START", (105, 1), ("feature-rings-table.jpg", "Gold rings on a library table beside a 7th &amp; Hill bag", SITE + "/search?q=ring"), (103, "charms", "necklaces"))
    + cta("Reply to Sally", MAIL + "?subject=Help%20me%20find%20the%20one", pad="4px 64px 8px",
          extra=text_link("Or start with Design Your Own", DYO, mt=18))
    + block("SPACER", "", pad="22px 0 0")
    + cat_line())

def moving_row(name, cells, eyebrow_text):
    """A light row of three cells that each cycle through pieces. No names, like the collages."""
    tds = "".join(f"""                    <td width="33.33%" valign="top" style="padding:4px;">{pimg(c, 172)}</td>
""" for c in cells)
    return heading(eyebrow_text, pad="4px 40px 16px") + f"""
          <!-- ═══════════ BLOCK: {name} · three moving cells ═══════════ -->
          <tr>
            <td class="pxs" align="center" style="padding:0 26px 30px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
{tds}                </tr>
              </table>
            </td>
          </tr>
"""

def gift_ps():
    """P.S. with Sally's welcome gift and the unique coupon (Klaviyo coupon VAULT15)."""
    return (f'A small welcome gift from me: 15% off your first 7th &amp; Hill piece.'
            f'</p><table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:12px 0 10px;">'
            f'<tr><td align="center" style="border:1px solid {GOLD}; padding:11px 22px;">'
            f'<p class="sans" style="margin:0; font-family:{SANS}; font-size:16px; line-height:20px; letter-spacing:4px; color:{INK};">{{% coupon_code \'VAULT15\' %}}</p>'
            f'</td></tr></table><p class="sans" style="margin:0; font-family:{SANS}; font-size:13px; line-height:21px; font-weight:400; color:{SOFT};">'
            f'Use it once, within 30 days. It does not combine with sale prices.')

doc("salt-t1-note-from-sally.html", code="T1", flow="SALT list", pos="T1 only", when=SALT_WAVES,
    card="", label="SALT list · T1 only · " + SALT_WAVES[0].lower() + SALT_WAVES[1:],
    title="A note from Sally", subject="A note from Sally", preheader="You may remember me from SALT.",
    reason=SALT_REASON, logic=SALT_LOGIC,
    notes=["Coupon: the same Klaviyo unique coupon VAULT15 (single use, 30 days, does not combine with sale prices).",
           "No prices. One light row of three moving cells (rings, necklaces, earrings) to invite a first look."],
    body=hero("hero-sally-fireplace.jpg", "Sally Brooks, founder and designer of 7th &amp; Hill, by the fireplace")
    + title_block(None, "A note from Sally")
    + letter([HI,
              "You may remember me as the previous Co-Founder of SALT Fine Jewelry. For eight years I designed for so many of you, and many of you became more than clients. I still remember the stories behind your pieces.",
              "Now I&rsquo;ve started something of my own: 7th &amp; Hill Jewelry. It&rsquo;s named after the corner in downtown Los Angeles where my dad ran his gold leaf lettering business, and where I first watched molten gold become a necklace.",
              "Every piece is solid gold, made to order in Toronto, Los Angeles and Italy. And I still begin the same way. I listen, I design, and then you wear it.",
              "You&rsquo;re receiving this because you were part of my SALT family."],
             ps=gift_ps())
    + moving_row("FROM THE WORKBENCH", ["rings", "necklaces", "earrings"], "From the workbench")
    + cta("Meet 7th &amp; Hill", utm(SITE, "salt_t1", "meet"), pad="0 64px 38px"))

# P0 popup: a layout mock and spec (the live popup is built in Klaviyo Forms)
POPUP = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>7H Vault popup</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:wght@400;500&amp;family=Inter:wght@400;500&amp;family=Montserrat:wght@500&amp;display=swap" rel="stylesheet">
<style>
  body {{ margin:0; background:{OUTER}; font-family:{SANS}; color:{INK}; }}
  .stage {{ padding:32px 16px 40px; display:flex; flex-wrap:wrap; gap:28px; justify-content:center; }}
  .pop {{ width:100%; max-width:420px; background:#fff; position:relative; }}
  .pop img {{ display:block; width:100%; height:auto; }}
  .x {{ position:absolute; top:10px; right:14px; color:#fff; font-size:22px; line-height:1; }}
  .in {{ padding:26px 34px 30px; text-align:center; }}
  .eb {{ font-size:11px; letter-spacing:3.5px; text-transform:uppercase; color:{GOLD}; margin:0 0 10px; }}
  h1 {{ font-family:{DISPLAY}; font-weight:400; font-size:30px; line-height:36px; margin:0 0 14px; }}
  .tx {{ font-size:14px; line-height:23px; font-weight:400; color:{BODY}; margin:0 0 20px; }}
  .field {{ border:1px solid #CFCFCF; padding:13px 14px; text-align:left; font-size:13px; color:{SOFT}; margin:0 0 10px; }}
  .btn {{ background:{GREEN}; color:#F7F5F1; padding:15px; font-size:12px; letter-spacing:3px; text-transform:uppercase; }}
  .fine {{ font-size:11px; line-height:17px; color:{SOFT}; margin:14px 0 0; font-weight:400; }}
  .done {{ padding:40px 34px; text-align:center; }}
  .spec {{ max-width:420px; width:100%; color:{IVORY}; font-size:13px; line-height:21px; font-weight:400; }}
  .spec b {{ color:{GOLD_L}; font-weight:400; letter-spacing:2px; text-transform:uppercase; font-size:11px; display:block; margin:14px 0 2px; }}
</style></head><body>
<div class="stage">
  <div class="pop">
    <img src="{IMG}popup-locket.jpg" alt="A gold capsule locket set with diamonds, worn">
    <div class="x">&times;</div>
    <div class="in">
      <p class="eb">The 7H Vault</p>
      <h1>Some pieces never make it to the site</h1>
      <p class="tx">Early access to new drops, private previews and notes from Sally. 15% off your first purchase, plus first word on our sales.</p>
      <div class="field">Email</div>
      <div class="btn">Unlock the Vault</div>
      <p class="fine">By subscribing you agree to receive emails from 7th &amp; Hill. Unsubscribe anytime.</p>
    </div>
  </div>
  <div class="pop">
    <div class="done">
      <img src="{IMG}seal.png" alt="" style="width:78px; margin:0 auto 18px;">
      <p class="eb">After signup</p>
      <h1>You&rsquo;re in.</h1>
      <p class="tx" style="margin:0">Your 15% code is on its way to your inbox.</p>
    </div>
  </div>
  <div class="spec">
    <b>Built in</b>Klaviyo Forms, popup, option B. This page is a layout mock only.
    <b>Shows</b>New visitors, after 8 seconds or on exit, once every 14 days. Not to existing subscribers.
    <b>On submit</b>Adds to the Vault list, which starts Welcome flow 01 (W1 carries the unique VAULT15 coupon).
    <b>Image</b>The piece up close (option B), not Sally&rsquo;s portrait.
    <b>Fonts</b>Cormorant for the headline, Inter for the text, as on the site; button #58744E (Sally's green).
  </div>
</div>
</body></html>
"""
doc("flow-p0-vault-popup.html", code="P0", flow="Site popup", pos="Klaviyo form, option B",
    when="New visitors, after 8 s or on exit, once every 14 days, not existing subscribers",
    card="Popup · new visitors, after 8 s or on exit, once every 14 days",
    title="7H Vault popup", subject="(popup, not an email)", preheader="Some pieces never make it to the site",
    status="Waiting for Sally: which pieces are subscriber-only", page=True, body=POPUP,
    notes=["Layout mock and copy spec. The live popup is built in Klaviyo Forms."])

# ═════════════════════════ STAGE 2 · goes live Mon Nov 2 ═════════════════════════
GIFTS = [201, 202, 203, (28, "iLove Smartphone Charm")]
GIFT_FOR = ["For the one who keeps your secrets", "For your sister", "For yourself", "For the little ones"]

doc("camp-k3-holiday-deadline.html", code="K3", flow="Campaign", pos="whole list", when="Tue Nov 3",
    card="Campaign · holiday deadline · Tue Nov 3",
    title="For holiday gifts, the clock starts now", subject="For holiday gifts, the clock starts now",
    preheader="Order dates for every kind of piece.",
    status="Draft, not yet approved by Sally · waiting for holiday order dates",
    logic=["Audience: Vault list plus SALT contacts. This is the first campaign the SALT list receives."],
    notes=["Suggested order-by dates for Sally to confirm: curated designs Nov 6, Exclusives Nov 30, in stock Dec 17.",
           "Neutral holiday wording on purpose: no trees, no Christmas."],
    body=hero("hero-rings-table.jpg", "Gold rings on a library table beside a 7th &amp; Hill bag")
    + title_block("The only deadline we have", "For holiday gifts, the clock starts now",
        "Some pieces are ready to go, others are made for you over a few weeks. Here&rsquo;s when to order so yours arrives in time.")
    + facts_band([("In stock", "Order by [date]. Ships in 1 to 2 business days."),
                  ("7th &amp; Hill Exclusives", "Order by [date]. Made in 2 to 4 weeks."),
                  ("Curated designs", "Order by [date]. Made in 6 to 8 weeks.")])
    + block("SPACER", "", pad="30px 0 0")
    + grid("GIFTS", GIFTS, cols=2, captions=GIFT_FOR)
    + cta("Start a gift", SHOP, pad="12px 64px 16px")
    + line("Your jewellery arrives in our luxurious book packaging featuring velvet lining.", pad="0 64px 34px", size_=13, color=SOFT)
    + trust_strip())

C = dict(status=DRAFT)
doc("flow-c1-piece-waiting.html", **C, code="C1", flow="Cart flow 06", pos="email 1 of 2", when="2 h after Added to Cart",
    card="Cart 06 · email 1 of 2 · 2 h after Added to Cart", title="Your piece is waiting", subject="Your piece is waiting",
    preheader="Saved in your bag, whenever you're ready.",
    notes=["Bag contents come from the Klaviyo Added to Cart event (dynamic block)."],
    body=hero("hero-pendant-book.jpg", "An enamel pendant resting on a gilded book", CART_URL)
    + title_block("Saved for you", "Your piece is waiting",
        "Some pieces are ready to ship, others are made for you over a few weeks. Starting now means yours arrives when you need it.")
    + dyn_cart()
    + cta("Return to your bag", CART_URL, pad="4px 64px 34px")
    + heading("From the workbench", pad="0 40px 18px")
    + grid("FROM THE WORKBENCH", [21, 13, 17])
    + trust_strip())

doc("flow-c2-sizing-question.html", **C, code="C2", flow="Cart flow 06", pos="email 2 of 2", when="24 h after Added to Cart",
    card="Cart 06 · email 2 of 2 · 24 h after Added to Cart", title="A question about sizing?", subject="A question about sizing?",
    preheader="Send me a photo of what you already wear.",
    body=hero("hero-sweater-hand.jpg", "A hand wearing a Marquise Art Deco ring, beside a gold enamel pendant", CART_URL)
    + title_block(None, "A question about sizing?")
    + letter([HI,
              "Not sure about size? Send me a photo of what you already wear, and I&rsquo;ll help you choose.",
              "A ring on your hand, a chain on your neck, anything that already feels right. Simply reply to this email and I&rsquo;ll tell you what to order."])
    + collage("WHAT OTHERS WEAR", (16, 13), ("feature-hands.jpg", "Marquise Art Deco rings worn on the hand", P[26]["url"]), (31, "rings", 2))
    + cta("Reply to Sally", MAIL + "?subject=A%20question%20about%20sizing", pad="4px 64px 8px",
          extra=text_link("Return to your bag", CART_URL, mt=20))
    + block("SPACER", "", pad="24px 0 0"))

doc("flow-co1-one-step-away.html", **C, code="CO1", flow="Checkout flow 07", pos="email 1 of 3", when="2 h after Started Checkout",
    card="Checkout 07 · email 1 of 3 · 2 h after Started Checkout", title="You were one step away", subject="You were one step away",
    preheader="Your order is saved, just as you left it.",
    logic=["If checkout value is $5,500 or more, the flow sends CC1 and CC2 instead of CO1 to CO3."],
    body=hero("hero-envelope-rings.jpg", "Two rings resting on a sealed letter", CHECKOUT)
    + title_block("Saved for you", "You were one step away",
        "Your order is saved, just as you left it. When you&rsquo;re ready, it&rsquo;s one click away.")
    + cta("Return to your bag", CHECKOUT, pad="4px 64px 36px")
    + heading("If you&rsquo;re still deciding", "A few favourites", pad="0 40px 22px")
    + checker("FAVOURITES", [14, 21, 2])
    + trust_strip())

doc("flow-co2-questions.html", **C, code="CO2", flow="Checkout flow 07", pos="email 2 of 3", when="22 h after CO1",
    card="Checkout 07 · email 2 of 3 · 22 h after CO1", title="Any questions before you decide?", subject="Any questions before you decide?",
    preheader="Sizing, timing and delivery, in short.",
    body=hero("hero-necklaces-book.jpg", "Gold necklaces resting on an old green leather book", CHECKOUT)
    + title_block("Short answers", "Any questions before you decide?", "For anything else, simply reply.")
    + facts_band([("Sizing", FACT_SIZING), ("Timing", FACT_TIMING), ("Delivery", FACT_DELIVERY)])
    + block("SPACER", "", pad="30px 0 0")
    + grid("WORTH A LOOK", [25, 16, 20])
    + cta("Return to your bag", CHECKOUT, pad="12px 64px 36px"))

doc("flow-co3-meant-for-a-date.html", **C, code="CO3", flow="Checkout flow 07", pos="email 3 of 3", when="48 h after CO1",
    card="Checkout 07 · email 3 of 3 · 48 h after CO1", title="If it's meant for a date", subject="If it's meant for a date",
    preheader="Count back from the day you need it.",
    body=hero("hero-locket-closeup.jpg", "A gold capsule locket set with diamonds, worn", CHECKOUT)
    + title_block("Timing", "If it&rsquo;s meant for a date",
        "A birthday, an anniversary, a holiday. Count back from the day you need it.")
    + facts_band([("In stock", "Ships in 1 to 2 business days."),
                  ("7th &amp; Hill Exclusives", "Made in 2 to 4 weeks."),
                  ("Curated designs", "Made in 6 to 8 weeks.")])
    + sally_note("Tell me the date and I&rsquo;ll tell you what&rsquo;s possible.")
    + grid("IN TIME", [23, 31, 9])
    + cta("Return to your bag", CHECKOUT, pad="12px 64px 8px", extra=text_link("Reply to Sally", MAIL, mt=20))
    + block("SPACER", "", pad="24px 0 0"))

doc("flow-cc1-concierge-note.html", **C, code="CC1", flow="Checkout flow 07 · concierge", pos="note 1 of 2",
    when="2 h after Started Checkout, checkout $5,500 or more (instead of CO1 to CO3)",
    card="Checkout 07 · concierge note 1 of 2 · 2 h after Started Checkout, $5,500 or more", title="A quick note from Sally", subject="A quick note from Sally",
    preheader="I'd like to help you choose, personally.",
    logic=["Flow split on checkout value: $5,500 or more goes here instead of CO1 to CO3. Sally replies personally."],
    body=hero("hero-sally-fireplace.jpg", "Sally Brooks, founder and designer of 7th &amp; Hill, by the fireplace", CHECKOUT)
    + title_block(None, "A quick note from Sally")
    + letter([HI,
              "Thank you for considering a piece from 7th &amp; Hill. For something this considered, I&rsquo;d like to help personally: size, stones, timing, anything at all.",
              "Simply reply to this email and I&rsquo;ll answer myself."])
    + cta("Reply to Sally", MAIL + "?subject=A%20note%20for%20Sally", pad="0 64px 8px",
          extra=text_link("Return to your bag", CHECKOUT, mt=20))
    + block("SPACER", "", pad="24px 0 0"))

doc("flow-cc2-concierge-timeline.html", **C, code="CC2", flow="Checkout flow 07 · concierge", pos="note 2 of 2",
    when="24 h after CC1, only if there was no reply",
    card="Checkout 07 · concierge note 2 of 2 · 24 h after CC1, only if no reply", title="About your timeline", subject="About your timeline",
    preheader="If it's easier to talk, I'm here.",
    logic=["Sends only if there was no reply to CC1 within a day."],
    body=hero("hero-sally-velvet.jpg", "Sally Brooks in black velvet", CHECKOUT)
    + title_block(None, "About your timeline")
    + letter([HI,
              "If it&rsquo;s easier to talk it through, I&rsquo;d be glad to set up a short call. Reply with a day and time that suit you, and I&rsquo;ll make it work.",
              "And if you&rsquo;d rather take your time, your bag is saved."])
    + cta("Set up a short call", MAIL + "?subject=A%20short%20call%20with%20Sally", pad="0 64px 8px",
          extra=text_link("Return to your bag", CHECKOUT, mt=20))
    + block("SPACER", "", pad="24px 0 0"))

# ═════════════════════════ STAGE 3 · goes live Mon Nov 9 ═════════════════════════
B = dict(status=DRAFT)
doc("flow-b1-still-thinking.html", **B, code="B1", flow="Browse flow 05", pos="email 1 of 2", when="4 h after Viewed Product",
    card="Browse 05 · email 1 of 2 · 4 h after Viewed Product", title="Still thinking about it?", subject="Still thinking about it?",
    preheader="A piece worth a second look.",
    logic=["Re-entry: once every 14 days per person."],
    notes=["The viewed piece comes from the Klaviyo Viewed Product event. The collage beside it is curated;",
           "swap it for a Klaviyo product recommendation block if you prefer."],
    body=hero("hero-model-armchair.jpg", "A woman in a green velvet armchair wearing a zodiac compass pendant and a pavé horn pendant")
    + title_block("Still thinking about it?", "A piece worth a second look")
    + dyn_viewed()
    + cta("See it again", "{{ event.URL|default:'https://www.7thandhilljewelry.ca/collections' }}", pad="0 64px 30px")
    + heading("Beside it", pad="0 40px 18px")
    + collage("BESIDE IT", (13, "pendants"), ("feature-compass.jpg", "A zodiac compass pendant and a pavé horn pendant on green velvet", SITE + "/search?q=pendant"), (21, 16, 31))
    + cat_line())

doc("flow-b2-worth-knowing.html", **B, code="B2", flow="Browse flow 05", pos="email 2 of 2", when="24 h after B1",
    card="Browse 05 · email 2 of 2 · 24 h after B1", title="Worth knowing before you choose", subject="Worth knowing before you choose",
    preheader="Solid gold, timing and delivery, in short.",
    body=hero("hero-necklaces-book.jpg", "Gold necklaces resting on an old green leather book")
    + title_block("The quiet, important part", "Worth knowing before you choose")
    + facts_band(FACTS_W4)
    + block("SPACER", "", pad="30px 0 0")
    + checker("WORTH A LOOK", [14, 4, 26])
    + cta("Discover 7th &amp; Hill", SHOP)
    + cat_line())

doc("flow-pp1-thank-you.html", **B, code="PP1", flow="After-purchase flow 10", pos="email 1 of 3", when="Right after Placed Order",
    card="After purchase 10 · email 1 of 3 · right after Placed Order", title="Thank you", subject="Thank you for choosing 7th & Hill",
    preheader="Your piece is in good hands.",
    body=hero("hero-bookbox-library.jpg", "Green 7th &amp; Hill book boxes, lined in velvet, in a library")
    + title_block("Thank you", greet(f"Thank you, {FN}", "Thank you"),
        "Your order is in good hands. Pieces in stock ship in 1 to 2 business days; anything made for you takes a little longer. We&rsquo;ll write to you the moment it ships.")
    + picture("UNBOXING · animation", "unboxing.gif", 300, 403, "A 7th &amp; Hill book box opening to show diamond earrings and a ring",
              cap="Your jewellery arrives in our luxurious book packaging featuring velvet lining.", pad="0 64px 10px")
    + sally_note("Thank you for choosing a piece of mine. I hope it becomes one you never take off.")
    + grid("ALONGSIDE", [13, 31, 17])
    + cat_line())

doc("flow-pp2-care.html", **B, code="PP2", flow="After-purchase flow 10", pos="email 2 of 3", when="Day 21 after Placed Order",
    card="After purchase 10 · email 2 of 3 · day 21", title="Welcome to the 7H story", subject="Welcome to the 7H story",
    preheader="A few habits that keep it beautiful for years.",
    notes=["Care rules follow the site's Jewelry Care page."],
    body=hero("hero-pendant-book.jpg", "An enamel pendant resting on a gilded book")
    + title_block("Day 21", "Welcome to the 7H story",
        "Your piece has had a few weeks to settle in. A few habits keep it beautiful for years.")
    + night("CARE · from the Jewelry Care page",
        eyebrow("Jewelry care", mb=20, color=GOLD_L)
        + night_list([
            ("Last on, first off", "Perfume, lotion and makeup go on before jewelry."),
            ("Clean gently", "Warm soapy water, a soft brush behind the stones, rinse, pat dry. Pearls: wipe with a soft dry cloth, never soak."),
            ("Everyday wear", "Solid gold, diamonds and gemstones are fine for daily washing and showers. Keep pearls dry."),
            ("Nothing harsh", "No bleach, harsh chemicals, commercial jewelry cleaners or ultrasonic cleaners."),
            ("Store apart", "Each piece on its own, in a soft pouch or lined box."),
          ])
        + text_link("Read the Jewelry Care page", CARE, mt=24, color=IVORY, line=GOLD_L))
    + picture("THE BOOK BOX", "story-bookbox.jpg", 488, 364, "The green 7th &amp; Hill book box, lined in velvet",
              cap="Store it in its book box between wears", pad="34px 64px 30px")
    + heading("To wear alongside it", "Charms to add over time", pad="0 40px 22px")
    + grid("ALONGSIDE", [(23, "Signature Toggle Charm"), 2, 9])
    + cat_line())

doc("flow-pp3-next-piece.html", **B, code="PP3", flow="After-purchase flow 10", pos="email 3 of 3", when="Day 35 after Placed Order",
    card="After purchase 10 · email 3 of 3 · day 35", title="Your next piece", subject="Your next piece",
    preheader="New from the workbench, in case something speaks to you.",
    body=hero("hero-model-armchair-locket.jpg", "A woman in a green velvet armchair wearing a gold capsule locket")
    + title_block("New from the workbench", "Your next piece",
        "A few new arrivals, in case something speaks to you.")
    + collage("NEW ARRIVALS", ("pendants", 31), ("feature-rings-table.jpg", "Gold rings on a library table beside a 7th &amp; Hill bag", SITE + "/search?q=ring"), (4, "rings", 32))
    + cta("Step inside", SHOP)
    + cat_line())

doc("flow-an1-a-year-ago.html", **B, code="AN1", flow="Anniversary flow 15", pos="email 1 of 1",
    when="Two weeks before the anniversary of the first purchase",
    card="Anniversary 15 · two weeks before the purchase anniversary", title="A year ago", subject="A year ago",
    preheader="A year with your 7th & Hill piece.",
    notes=["Trigger: date property of the first order. To show the exact date, insert the profile date property in the first line."],
    body=hero("hero-bookbox-library.jpg", "Green 7th &amp; Hill book boxes, lined in velvet, in a library")
    + title_block("A year ago", "A year with your piece",
        "A year ago this month, a 7th &amp; Hill piece became yours. If the year deserves marking, a charm, a date or a new piece can carry it.")
    + collage("TO MARK THE YEAR", (103, 105), ("feature-compass.jpg", "A zodiac compass pendant and a pavé horn pendant on green velvet", SITE + "/search?q=pendant"), (7, 3, "charms"), feature_side="left")
    + cta("Mark the year", SHOP)
    + cat_line())

doc("camp-k1-new-in-studio.html", status=DRAFT, code="K1", flow="Weekly campaign", pos="skeleton",
    when="Tue Nov 10", card="Campaign · New in the studio · Tue Nov 10",
    title="New in the studio", subject="New in the studio: [this week]", preheader="[What just left the workbench]",
    notes=["Skeleton: Sally sends the pieces each week. Swap the photo, the six pieces and the two lines."],
    body=hero("hero-locket-closeup.jpg", "A gold capsule locket set with diamonds, worn")
    + title_block("New in the studio", "[This week&rsquo;s headline]",
        "[Two calm sentences about what just left the workbench.]")
    + heading("What just left the workbench", pad="0 40px 18px")
    + collage("THIS WEEK", ("charms", 9), ("feature-compass.jpg", "A zodiac compass pendant and a pavé horn pendant on green velvet", SITE + "/search?q=pendant"), (7, 3, "rings"))
    + cta("Step inside", SHOP)
    + cat_line())

# ═════════════════════════ STAGE 4 · by Tue Nov 24 ═════════════════════════
SALE_NOTES = ["Sale series: three letters, one look each (private note, the sale, the last word). For New Year, Valentine's,",
              "Mother's Day or a flash sale, reuse one of them and change the offer block and the pieces.",
              "Calm on purpose: no red, no countdown timers, no Shop now.",
              "Pieces are placeholders: replace with pieces marked A 7th & Hill Exclusive."]

def offer_light(big, small):
    """Offer on white, framed in gold: quieter than the dark band, for the private and last-day letters."""
    return block("OFFER · swap for each sale", f"""              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr><td align="center" style="border:1px solid {GOLD}; padding:26px 24px;">
                  {eyebrow("The offer", mb=8)}
                  <p class="display" style="margin:0 0 8px; font-family:{DISPLAY}; font-size:43px; line-height:44px; color:{INK};">{big}</p>
                  <p class="sans" style="margin:0; font-family:{SANS}; font-size:14px; line-height:22px; font-weight:400; color:{BODY};">{small}</p>
                </td></tr>
              </table>
""", pad="0 48px 32px")

SALE = dict(status=DRAFT, flow="Sale template", pos="Black Friday", notes=SALE_NOTES)

# S1 · private: close-up photo, Sally's note, the offer framed in gold, three pieces
doc("camp-s1-vault-early-access.html", **SALE, code="S1", when="Wed Nov 25, 18:00",
    card="Campaign · Vault early access · Wed Nov 25, 18:00", title="Before anyone else",
    subject="Before anyone else", preheader="Early access for the Vault.",
    logic=["Audience: Vault list plus SALT contacts."],
    body=hero("hero-locket-closeup.jpg", "A gold capsule locket set with diamonds, worn")
    + title_block("For the Vault, first", "Before anyone else")
    + sally_note("Black Friday opens to the Vault tonight, a little before everyone else. I wanted you to see these first.").replace("padding:28px 56px 34px", "padding:0 56px 30px")
    + offer_light("20% off", "Every piece marked A 7th &amp; Hill Exclusive.<br>Each is made in 2 to 4 weeks, in time for the holidays.")
    + grid("EXCLUSIVES", [26, 21, 14])
    + cta("Step inside", SHOP, pad="16px 64px 40px"))

# S2 · the sale: model photo, the offer in the dark band, a collage with moving cells
doc("camp-s2-black-friday.html", **SALE, code="S2", when="Fri Nov 27, 08:00",
    card="Campaign · Black Friday · Fri Nov 27, 08:00", title="20% off our Exclusives",
    subject="20% off our Exclusives", preheader="From today until Monday.",
    body=hero("hero-water-lilies.jpg", "A woman in a pale blue dress lying by a lily pond, wearing a heart charm necklace, a medallion and a gold bracelet")
    + night("OFFER · swap for each sale",
        eyebrow("Black Friday", mb=10, color=GOLD_L)
        + h1("20% off our Exclusives", mb=12, color=IVORY, size_=37)
        + p("From today until Monday, every piece marked A 7th &amp; Hill Exclusive. Each is made in 2 to 4 weeks, in time for the holidays.", mb=0, color=NDIM),
        pad="34px 56px 40px")
    + block("SPACER", "", pad="28px 0 0")
    + collage("EXCLUSIVES", ("rings", 1), ("feature-hands.jpg", "Marquise Art Deco rings worn on the hand", P[26]["url"]), (13, 16, "pendants"), feature_side="left")
    + cta("Step inside", SHOP)
    + trust_strip())

# S3 · the last word: a letter on the desk, short, pieces with names
doc("camp-s3-last-day.html", **SALE, code="S3", when="Mon Nov 30",
    card="Campaign · last day of the sale · Mon Nov 30", title="Today is the last day",
    subject="Today is the last day", preheader="The 20% on our Exclusives ends tonight.",
    logic=["Audience: opened S2 and did not buy."],
    body=hero("hero-envelope-rings.jpg", "Two rings resting on a sealed letter")
    + title_block("The last day", "Today is the last day",
        "The 20% on our Exclusives ends tonight. If one has been on your mind, this is the moment.")
    + offer_light("Until midnight", "20% off every piece marked A 7th &amp; Hill Exclusive.")
    + checker("STILL HERE", [21, 14, 1])
    + cta("Step inside", SHOP, pad="0 64px 40px"))

doc("camp-dyo-design-your-own.html", status=DRAFT, code="DYO", flow="Campaign", pos="whole list",
    when="Tue Nov 17", card="Campaign · Design Your Own · Tue Nov 17",
    title="Design your own", subject="Some pieces don't exist yet", preheader="Let's make yours together.",
    body=hero("hero-necklaces-book.jpg", "Gold necklaces resting on an old green leather book")
    + title_block("Design your own", "Listen. Design. Adorn.",
        "Some pieces don&rsquo;t exist yet. We can make yours together, one on one.")
    + night("THREE STEPS",
        night_list([
            ("Listen", "Send me your idea, a photo, the story behind it."),
            ("Design", "I sketch it, and you choose the gold, the stones and the details."),
            ("Adorn", "It&rsquo;s made to order, just for you."),
          ], numerals=["i", "ii", "iii"]), pad="34px 56px 40px")
    + heading("Made personal", pad="34px 40px 18px")
    + checker("MADE PERSONAL", [5, 12, 105])
    + cta("Start your design", MAIL + "?subject=Design%20my%20own", pad="4px 64px 8px",
          extra=text_link("See Design Your Own", DYO, mt=20))
    + block("SPACER", "", pad="24px 0 0")
    + cat_line())

doc("camp-k4-gift-guide.html", status="Draft, not yet approved by Sally · waiting for the in-stock and Exclusives list",
    code="K4", flow="Campaign", pos="whole list", when="Thu Dec 3", card="Campaign · gift guide · Thu Dec 3",
    title="The 7H gift guide", subject="The 7H gift guide", preheader="Pieces that can still arrive in time.",
    notes=["Show only pieces that can still arrive: in stock and 7th & Hill Exclusives. Grid below is a placeholder."],
    body=hero("hero-model-sweater.jpg", "A woman between old books wearing a gold enamel pendant, a heart charm necklace and a marquise ring, holding a 7th &amp; Hill bag")
    + title_block("The 7H gift guide", "Gifts that arrive in time",
        "Every piece here is in stock or one of our Exclusives, so it can still arrive before the holidays.")
    + grid("GIFTS", [201, 13, 21, (28, "iLove Smartphone Charm")], cols=2,
           captions=["For the one who keeps your secrets", "For your sister", "For yourself", "For the little ones"])
    + cta("Start a gift", SHOP, pad="12px 64px 16px")
    + line("Your jewellery arrives in our luxurious book packaging featuring velvet lining.", pad="0 64px 34px", size_=13, color=SOFT)
    + trust_strip())

EDIT = dict(status=DRAFT, code="K2", flow="Campaign", pos="Sally’s Edit")
doc("camp-k2-sallys-edit-dec8.html", **EDIT, when="Tue Dec 8", card="Campaign · Sally’s Edit · green library · Tue Dec 8",
    title="Sally&rsquo;s edit", subject="Sally's edit · [theme]", preheader="The pieces I kept reaching for this week.",
    notes=["The green library layout Sally chose. Reusable: swap the photo, the note and the pieces."],
    body=masthead("", "")
    + hero("hero-rings-table.jpg", "Gold rings on a library table beside a 7th &amp; Hill bag", SITE + "/search?q=ring")
    + sally_note("This week I kept reaching for small talismans: a compass, a horseshoe, a crown. Pieces that carry a wish, worn every day.")
    + collage("THE EDIT", ("charms", 9), ("feature-compass.jpg", "A zodiac compass pendant and a pavé horn pendant on green velvet", SITE + "/search?q=pendant"), (7, 3, "rings"))
    + cta("Discover 7th &amp; Hill", SHOP)
    + cat_line())
doc("camp-k2-sallys-edit-oct27.html", **EDIT, when="Tue Oct 27, 11:00", card="Campaign · Sally’s Edit · Tue Oct 27, 11:00",
    title="Sally&rsquo;s edit", subject="Sally's edit · [theme]", preheader="Four I'd give, and four I'd keep.",
    logic=["Audience: Vault list only. SALT contacts join the campaign audience from K3 (Tue Nov 3)."],
    notes=["Layout: photo, note, pieces with names."],
    body=masthead("", "")
    + hero("hero-pendant-book.jpg", "An enamel pendant resting on a gilded book", SITE + "/search?q=pendant")
    + sally_note("Every pendant here holds something: a name, a date, a small superstition. These are the ones I&rsquo;d give, and the ones I&rsquo;d keep.")
    + checker("THE EDIT", [1, 12, 4, 3])
    + cta("Discover 7th &amp; Hill", SHOP)
    + cat_line())
doc("camp-k2-sallys-edit-spare.html", **EDIT, when="No date yet (spare layout)", card="Campaign · Sally’s Edit · spare layout, no date yet",
    title="Sally&rsquo;s edit", subject="Sally's edit · [the piece]", preheader="[One line from Sally]",
    notes=["Alternative layout: one piece. Sally writes the two lines about it; nothing is invented for her."],
    body=masthead("", "")
    + hero("hero-locket-closeup.jpg", "A gold capsule locket set with diamonds, worn", SITE + "/search?q=locket")
    + title_block("The piece of the week", "[Name of the piece]", "[Two lines from Sally about this piece.]", pt=18)
    + cta("View the piece", SITE + "/search?q=locket", pad="0 64px 34px")
    + heading("Wear it with")
    + grid("WEAR IT WITH", [13, 16, (23, "Signature Toggle Charm")])
    + cat_line())

doc("camp-lc-last-call.html", status=DRAFT, code="LC", flow="Campaign", pos="whole list", when="Tue Dec 15",
    card="Campaign · last call · Tue Dec 15", title="Last call for in-stock pieces", subject="Last call for in-stock pieces",
    preheader="Order by [date] and it arrives in time.",
    notes=["Pieces: in-stock only (placeholders below)."],
    body=hero("hero-bookbox-library.jpg", "Green 7th &amp; Hill book boxes, lined in velvet, in a library")
    + title_block("Last call", "Last call for in-stock pieces",
        "In-stock pieces ordered by [date] ship in 1 to 2 business days and arrive in time for the holidays.")
    + collage("IN STOCK", (16, 13), ("feature-rings-table.jpg", "Gold rings on a library table beside a 7th &amp; Hill bag", SITE + "/search?q=ring"), ("rings", 28, 31))
    + cta("Start a gift", SHOP, pad="6px 64px 16px")
    + line("Your jewellery arrives in our luxurious book packaging featuring velvet lining.", pad="0 64px 30px", size_=13, color=SOFT)
    + trust_strip())

doc("camp-hn-holiday-note.html", status=DRAFT, code="HN", flow="Campaign", pos="whole list", when="Thu Dec 24",
    card="Campaign · holiday note · Thu Dec 24", title="A holiday note from Sally", subject="A holiday note from Sally",
    preheader="Thank you, from the workbench.",
    notes=["No selling and no button to buy. Holiday wording for all clients."],
    body=hero("hero-sally-velvet.jpg", "Sally Brooks in black velvet")
    + title_block(None, "A holiday note from Sally")
    + letter([HI,
              "This year, thank you. For the stories you shared with me, for the pieces you chose for the people you love, and for every note you sent back.",
              "Whatever you celebrate, I hope these days are warm and unhurried.",
              "See you in the new year."])
    + picture("THE BOOK BOX", "story-bookbox.jpg", 488, 364, "The green 7th &amp; Hill book box, lined in velvet", pad="0 64px 40px"))


# ───────── blocks/ (paste-ready snippets) and the catalog list
B_DIR = os.path.join(ROOT, "blocks"); os.makedirs(B_DIR, exist_ok=True)
for fn in os.listdir(B_DIR):
    if fn.endswith(".html"):
        os.remove(os.path.join(B_DIR, fn))
SNIPS = {
    "collage.html": ("Two small pieces stacked + one large photo, then three in a row.", collage("PIECES", ("rings", 2), ("feature-hands.jpg", "Rings worn on the hand", SHOP), (24, 13, "earrings"))),
    "grid.html": ("Pieces in rows of three with names.", grid("PIECES", [13, 16, 21])),
    "pieces-with-names.html": ("Rows of photo + name, sides alternate.", checker("PIECES", [5, 12, 7])),
    "facts.html": ("Facts Sally confirmed: gold, timing, delivery, care.", facts("WORTH KNOWING", FACTS_W4)),
    "letter-and-signature.html": ("Sally's words beside her portrait, signed.", letter([HI, "[Sally's words]"])),
    "facts-band.html": ("Facts in the dark band.", facts_band(FACTS_W4)),
    "night-quote.html": ("Dark band with a quote.", night("QUOTE", quote("[Quote]"), pad="34px 56px 38px")),
    "find-your-place.html": ("Seven collection tiles.", find_your_piece("Find your place", CATS_W1)),
    "trust-strip.html": ("Solid gold · Book box · Duties.", trust_strip()),
}
for fn, (desc, html) in SNIPS.items():
    with open(os.path.join(B_DIR, fn), "w") as fh:
        fh.write(f"<!--\n  7th & Hill · snippet: {desc}\n  Paste between the top bar and the footer of any template.\n-->{html}")
with open(os.path.join(B_DIR, "catalog.md"), "w") as fh:
    fh.write("# 7th & Hill · pieces used in the letters\n\nNumber = key in `assets/catalog.json`, used in `scripts/compose.py`. "
             "1 to 32: photo catalog. 101+: extra packshots. 201+: worn photos.\n\n| # | Piece | Image | Link |\n|---|---|---|---|\n")
    for k in sorted(P):
        fh.write(f"| {k} | {P[k]['name'].replace('&amp;', '&')} | {P[k]['img']} | {P[k]['url']} |\n")

# remove letters this script no longer writes
for fn in os.listdir(os.path.join(ROOT, "templates")):
    if fn.endswith(".html") and fn not in WRITTEN:
        os.remove(os.path.join(ROOT, "templates", fn))
print(f"{len(WRITTEN)} letters written")
