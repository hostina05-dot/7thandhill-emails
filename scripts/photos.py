#!/usr/bin/env python3
"""7th & Hill photo pipeline: one colour grade for every photo, then the crops the emails use.

    python3 scripts/photos.py

Reads originals from assets/photos/ and writes assets/images/:
  hero-*.jpg     full-width photo (1200 px, shown at 600) with the round seal on its lower edge
  feature-*.jpg  large square photo for collages (704 px, shown at 352)
  tile-*.jpg     small square of a worn piece, same size as a product tile
  story-*.jpg    photo inside a block (no seal)
  product-1xx.jpg  packshots on the moonlit backdrop (PACKSHOTS); seal.png for letters without a photo

To swap a photo: put the new original in assets/photos/, change its name in SHOTS below, run the
script, then `python3 scripts/build.py`. Product photos (product-NN.jpg) are not touched here.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PHOTOS, OUT = ROOT / "assets" / "photos", ROOT / "assets" / "images"

# name -> (original, kind, crop box as fractions (left, top, right, bottom) or None)
SHOTS = {
    # full-width photos with the seal (hero)
    "hero-sally-home.jpg":       ("sally-home.jpg",                  "hero",    (0, 0, 1, 0.68)),
    "hero-sally-velvet.jpg":     ("sally-velvet.jpg",                "hero",    (0, 0.03, 1, 0.48)),
    "hero-lily-bracelet.jpg":    ("sally-lily-bracelet.jpg",         "hero",    (0, 0.10, 1, 0.90)),
    "hero-model-library.jpg":    ("model-library-locket.jpg",        "hero",    (0, 0, 1, 0.92)),
    "hero-model-sweater.jpg":    ("model-green-sweater.jpg",         "hero",    (0.10, 0, 0.90, 1)),
    "hero-model-armchair.jpg":   ("model-green-armchair.jpg",        "hero",    (0, 0.02, 1, 0.64)),
    "hero-bookbox-library.jpg":  ("bookbox-library.jpg",             "hero",    (0, 0.06, 1, 1)),
    "hero-envelope-rings.jpg":   ("envelope-rings.jpg",              "hero",    (0, 0.08, 1, 1)),
    "hero-rings-table.jpg":      ("rings-table-bag.jpg",             "hero",    (0, 0.30, 1, 0.88)),
    "hero-locket-closeup.jpg":   ("locket-closeup.jpg",              "hero",    (0, 0.18, 1, 0.92)),
    "hero-pendant-book.jpg":     ("pendant-red-book.jpg",            "hero",    (0, 0.04, 1, 1)),
    "hero-necklaces-book.jpg":   ("necklaces-green-book-hires.jpg",  "hero",    (0, 0.0, 1, 0.60)),
    "hero-hand-rings.jpg":       ("hand-rings.jpg",                  "hero",    (0, 0.12, 1, 0.88)),
    "hero-archive-corner.jpg":   ("corner-7th-hill-1920s.jpg",       "hero",    None),
    "hero-archive-building.jpg": ("archive-st-vincent-building.jpg",  "hero",    (0, 0.08, 1, 0.70)),
    # large square photos inside collages (feature)
    "feature-hands.jpg":         ("hand-rings.jpg",                  "feature", (0, 0, 1, 1)),
    "feature-rings-table.jpg":   ("rings-table-bag.jpg",             "feature", (0, 0.20, 1, 0.95)),
    "feature-compass.jpg":       ("compass-horn-velvet.jpg",         "feature", (0, 0.06, 1, 0.86)),
    # small squares of worn pieces, same size as product tiles (tile)
    "tile-talisman-locket.jpg":  ("locket-worn.jpg",                 "tile",    None),
    "tile-lovers-tarot.jpg":     ("lovers-worn.jpg",                 "tile",    None),
    "tile-marquise-ring.jpg":    ("ring-marquise-worn.jpg",          "tile",    None),
    # photos inside a block, no seal (story)
    "story-bookbox.jpg":         ("bookbox-library.jpg",             "story",   None),
    "popup-locket.jpg":          ("locket-closeup.jpg",              "story",   (0, 0.28, 1, 0.78)),
    # round portrait for Sally's notes
    "sally-avatar.png":          ("sally-velvet.jpg",                "avatar",  (0.000, 0.045, 1.000, 0.603)),
}

# white-background packshots -> product tiles on the soft moonlit backdrop all catalog pieces share
PACKSHOTS = {
    "product-101.jpg": "ring-sunburst.jpg",     # Art Deco Sunburst Ring
    "product-102.jpg": "heart-sunburst.jpg",    # Radiant Sunburst Heart
    "product-103.jpg": "charm-baby.jpg",        # Hand & Footprint Heart
    "product-104.jpg": "charm-butterfly.jpg",   # Fluted Diamond Butterfly
    "product-105.jpg": "ring-date.jpg",         # Custom Date Ring
}


def grade(im: Image.Image) -> Image.Image:
    """Warm, slightly muted, matte: deep green-tinted shadows, soft warm highlights."""
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]
    a = lum + (a - lum) * 0.80                                  # mute colour a little
    a = a * np.array([1.015, 1.0, 0.965])                      # warm the whole frame slightly
    mean = float(lum.mean())                                    # pull very bright photos down,
    a = a * (1 - 0.65 * max(0.0, mean - 0.40))                  # so all shots sit at a similar key
    a = 0.035 + a * 0.93                                        # matte: lifted blacks, softer whites
    a = np.clip(a, 0, 1)
    a = a + 0.5 * (a - 0.5) * 0.12 * (1 - np.abs(a - 0.5) * 2)  # gentle S-curve in the mid-tones
    shadow = np.clip(1 - lum * 2.2, 0, 1)                       # split tone
    high = np.clip((lum - 0.55) * 2.2, 0, 1)
    a = a + shadow * np.array([-0.012, 0.010, 0.004]) + high * np.array([0.040, 0.016, -0.034])
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


# animated GIFs cut from short videos: name -> (video, start s, length s, hold last frame s, width, crop as fractions[, fps])
CLIPS = {
    "unboxing.gif": ("unboxing.mov", 0.0, 3.0, 2.5, 300, (0.145, 0.26, 0.865, 0.80)),
}


# slideshows from a video: name -> (video, [frame times in s], seconds per slide, width, crop)
# A whole video as a GIF is too heavy for email; a few sharp frames hold up better and weigh far less.
SLIDES = {
    "library-reel.gif": ("library-reel.mov", [1.6, 4.8, 2.4, 3.2, 5.6, 6.4], 1.6, 300, (0.0, 0.15, 1.0, 0.85)),
}


def crop(im, box):
    if not box:
        return im
    w, h = im.size
    return im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))


def seal_disc(d=144, ring=6):
    logo = Image.open(OUT / "logo.png").convert("RGBA").resize((d, d), Image.LANCZOS)
    disc = Image.new("RGBA", (d + 2 * ring,) * 2, (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse([0, 0, d + 2 * ring - 1, d + 2 * ring - 1], fill=(247, 245, 241, 255))
    disc.alpha_composite(logo, (ring, ring))
    return disc


def moonlit(w, h, top=(214, 222, 231), bot=(243, 245, 248)):
    """The backdrop of every product tile: cool vertical gradient with a soft glow behind the piece."""
    from PIL import ImageFilter
    g = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        g.putpixel((0, y), tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    g = g.resize((w, h))
    glow = Image.new("L", (w, h), 0); r = w * 0.36
    ImageDraw.Draw(glow).ellipse([w / 2 - r, h * 0.46 - r, w / 2 + r, h * 0.46 + r], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(w * 0.12))
    return Image.composite(Image.new("RGB", (w, h), (250, 251, 252)), g, glow)


def packshots():
    from PIL import ImageChops
    for name, src in PACKSHOTS.items():
        im = ImageOps.fit(Image.open(PHOTOS / "packshots" / src).convert("RGB"), (600, 600), Image.LANCZOS)
        ImageChops.multiply(im, moonlit(600, 600)).save(OUT / name, quality=82, optimize=True, progressive=True)
        print(f"{name:26} 600x600 (moonlit)")


def seal_png():
    """The seal on its own, for letters that open without a photo."""
    seal_disc().save(OUT / "seal.png", optimize=True)


def main():
    disc = seal_disc()
    for name, (src, kind, box) in SHOTS.items():
        if kind == "split":  # two photos side by side, one seal across the seam
            halves = [ImageOps.fit(grade(crop(Image.open(PHOTOS / f).convert("RGB"), b)), (600, 760), Image.LANCZOS) for f, b in src]
            out = Image.new("RGB", (1200, 760 + disc.size[1] // 2), "white")
            out.paste(halves[0], (0, 0)); out.paste(halves[1], (600, 0))
            out.paste(disc, ((1200 - disc.size[0]) // 2, 760 - disc.size[1] // 2), disc)
            out.save(OUT / name, quality=82, optimize=True, progressive=True)
            print(f"{name:26} {out.size[0]}x{out.size[1]}")
            continue
        im = grade(crop(Image.open(PHOTOS / src).convert("RGB"), box))
        if kind == "avatar":  # round portrait with a cream ring, transparent corners
            size, ring = 112, 4
            face = ImageOps.fit(im, (size - 2 * ring,) * 2, Image.LANCZOS, centering=(0.5, 0.5))
            out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            ImageDraw.Draw(out).ellipse([0, 0, size - 1, size - 1], fill=(247, 245, 241, 255))
            mask = Image.new("L", face.size, 0); ImageDraw.Draw(mask).ellipse([0, 0, face.size[0] - 1, face.size[1] - 1], fill=255)
            out.paste(face, (ring, ring), mask)
            out.save(OUT / name, optimize=True)
            print(f"{name:26} {size}x{size}")
            continue
        if kind == "hero":
            w = 1200
            im = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
            out = Image.new("RGB", (w, im.size[1] + disc.size[1] // 2), "white")
            out.paste(im, (0, 0))
            out.paste(disc, ((w - disc.size[0]) // 2, im.size[1] - disc.size[1] // 2), disc)
        elif kind == "feature":
            out = ImageOps.fit(im, (704, 704), Image.LANCZOS)
        elif kind == "tile":
            out = ImageOps.fit(im, (440, 440), Image.LANCZOS)
        else:
            w = min(1200, im.size[0])
            out = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
        out.save(OUT / name, quality=82, optimize=True, progressive=True)
        print(f"{name:26} {out.size[0]}x{out.size[1]}")


def clips():
    """Video -> graded GIF. First frame is what Outlook for Windows shows, so start on a good frame."""
    import subprocess, tempfile
    for name, (video, start, length, hold, width, box, *rest) in CLIPS.items():
        fps = rest[0] if rest else 8
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-t", str(length), "-i", str(PHOTOS / video),
                        "-vf", f"fps={fps},hqdn3d=6:6:12:12", str(tmp / "raw%04d.png")], check=True)
        raw = sorted(tmp.glob("raw*.png"))
        frames = []
        for f in raw:
            im = crop(Image.open(f).convert("RGB"), box)
            frames.append(grade(im.resize((width, round(im.size[1] * width / im.size[0])), Image.LANCZOS)))
        frames += [frames[-1]] * int(hold * fps)
        for i, im in enumerate(frames):
            im.save(tmp / f"g{i:04d}.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", str(tmp / "g%04d.png"),
                        "-vf", "palettegen=max_colors=96:stats_mode=full", str(tmp / "pal.png")], check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", str(tmp / "g%04d.png"), "-i", str(tmp / "pal.png"),
                        "-lavfi", "paletteuse=dither=none:diff_mode=rectangle", "-loop", "0", str(OUT / name)], check=True)
        print(f"{name:26} {frames[0].size[0]}x{frames[0].size[1]}  {(OUT / name).stat().st_size // 1024} KB")


def slides():
    """Video frames -> graded slideshow GIF with one shared palette (no fades, so each slide stays crisp)."""
    import subprocess, tempfile
    for name, (video, times, hold, width, box) in SLIDES.items():
        tmp = Path(tempfile.mkdtemp())
        frames = []
        for i, t in enumerate(times):
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(PHOTOS / video),
                            "-frames:v", "1", str(tmp / f"f{i}.png")], check=True)
            im = crop(Image.open(tmp / f"f{i}.png").convert("RGB"), box)
            frames.append(grade(im.resize((width, round(im.size[1] * width / im.size[0])), Image.LANCZOS)))
        sheet = Image.new("RGB", (width * len(frames), frames[0].size[1]))
        for i, f in enumerate(frames):
            sheet.paste(f, (i * width, 0))
        pal = sheet.quantize(colors=200, method=Image.Quantize.MEDIANCUT)
        q = [f.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]
        q[0].save(OUT / name, save_all=True, append_images=q[1:], duration=int(hold * 1000), loop=0, optimize=True)
        print(f"{name:26} {width}x{frames[0].size[1]}  {(OUT / name).stat().st_size // 1024} KB  ({len(frames)} slides)")


if __name__ == "__main__":
    main()
    packshots()
    seal_png()
    clips()
    slides()
