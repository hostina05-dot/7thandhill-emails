#!/usr/bin/env python3
"""7th & Hill photo pipeline: one colour grade for every photo, then the crops the emails use.

    python3 scripts/photos.py

Reads originals from assets/photos/ and writes assets/images/:
  hero-*.jpg     full-width photo (1200 px, shown at 600) with the round seal on its lower edge
  feature-*.jpg  large square photo for collages (704 px, shown at 352)
  story-*.jpg    photo inside a dark band (no seal)

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
    "hero-welcome-1.jpg":      ("sally-home.jpg",            "hero",    (0, 0, 1, 0.68)),
    "hero-welcome-2.jpg":      ("sally-lily-bracelet.jpg",   "hero",    (0, 0.10, 1, 0.90)),
    "hero-welcome-3.jpg":      ("model-library-locket.jpg",  "hero",    (0, 0, 1, 0.92)),
    "hero-campaign.jpg":       ("model-green-armchair.jpg",  "hero",    (0, 0.02, 1, 0.80)),
    "hero-thank-you.jpg":      ("bookbox-library.jpg",       "hero",    (0, 0.06, 1, 1)),
    "hero-abandoned-cart.jpg": ("envelope-rings.jpg",        "hero",    (0, 0.08, 1, 1)),
    "hero-salt.jpg":           ("sally-home.jpg",            "hero",    (0, 0.04, 1, 0.62)),
    "feature-hands.jpg":       ("hand-rings.jpg",            "feature", (0, 0, 1, 1)),
    "feature-spines.jpg":      ("pendants-book-spines.jpg",  "feature", (0.10, 0.10, 0.96, 0.74)),
    "feature-locket.jpg":      ("locket-closeup.jpg",        "feature", (0, 0.30, 1, 1)),
    "feature-tusk.jpg":        ("necklaces-green-book-hires.jpg", "feature", (0.14, 0.49, 0.72, 0.92)),
    "feature-rings-table.jpg": ("rings-table-bag.jpg",       "feature", (0, 0.20, 1, 0.95)),
    "hero-edit-collage.jpg":   ("rings-table-bag.jpg",       "hero",    (0, 0.30, 1, 0.88)),
    "hero-edit-spotlight.jpg": ("locket-closeup.jpg",        "hero",    (0, 0.18, 1, 0.92)),
    "hero-edit-split.jpg":     ((("model-green-armchair.jpg", (0.12, 0.0, 0.88, 0.76)),
                                 ("compass-horn-velvet.jpg", (0.0, 0.0, 1.0, 1.0))), "split", None),
    "sally-avatar.png":        ("sally-avatar.jpg",          "avatar",  None),
    "story-corner.jpg":        ("corner-7th-hill-1920s.jpg", "story",   None),
    "bookbox.jpg":             ("bookbox-library.jpg",       "story",   None),
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


# animated GIFs cut from short videos: name -> (video, start s, length s, hold last frame s, width, crop as fractions)
CLIPS = {
    "unboxing.gif": ("unboxing.mov", 0.0, 3.0, 2.5, 300, (0.145, 0.26, 0.865, 0.80)),
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
            face = ImageOps.fit(im, (size - 2 * ring,) * 2, Image.LANCZOS, centering=(0.5, 0.35))
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
        else:
            w = min(1200, im.size[0])
            out = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
        out.save(OUT / name, quality=82, optimize=True, progressive=True)
        print(f"{name:26} {out.size[0]}x{out.size[1]}")


def clips():
    """Video -> graded GIF. First frame is what Outlook for Windows shows, so start on a good frame."""
    import subprocess, tempfile
    for name, (video, start, length, hold, width, box) in CLIPS.items():
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-t", str(length), "-i", str(PHOTOS / video),
                        "-vf", "fps=8,hqdn3d=6:6:12:12", str(tmp / "raw%04d.png")], check=True)
        raw = sorted(tmp.glob("raw*.png"))
        frames = []
        for f in raw:
            im = crop(Image.open(f).convert("RGB"), box)
            frames.append(grade(im.resize((width, round(im.size[1] * width / im.size[0])), Image.LANCZOS)))
        frames += [frames[-1]] * int(hold * 8)
        for i, im in enumerate(frames):
            im.save(tmp / f"g{i:04d}.png")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "8", "-i", str(tmp / "g%04d.png"),
                        "-vf", "palettegen=max_colors=96:stats_mode=full", str(tmp / "pal.png")], check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "8", "-i", str(tmp / "g%04d.png"), "-i", str(tmp / "pal.png"),
                        "-lavfi", "paletteuse=dither=none:diff_mode=rectangle", "-loop", "0", str(OUT / name)], check=True)
        print(f"{name:26} {frames[0].size[0]}x{frames[0].size[1]}  {(OUT / name).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
    clips()
