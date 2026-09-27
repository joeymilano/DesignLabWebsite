"""Crop individual student works out of the long portfolio sheets (portfolio-2..5.png).

Row bands were detected by scanning for the sheets' background colour (#E7E5D9).
Output: assets/work/<slug>.webp (max 1600px wide, background margins trimmed)
        assets/work/sm/<slug>.webp (900px wide, for grids and previews)
Run: python3 scripts/crop-work.py
"""
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "work"
BG = np.array([231, 229, 217])

# slug: (sheet, top, bottom)
CROPS = {
    "wearable-memory": (3, 435, 1872),
    "e-motorcycle": (3, 1917, 2853),
    "mars-research": (3, 2877, 4518),
    "mars-modules": (3, 4542, 5772),
    "vehicle-lighting": (3, 5829, 7086),
    "journey-map": (2, 480, 1401),
    "sustainable-app": (2, 1431, 2313),
    "vehicle-hmi": (2, 2343, 3549),
    "kitchen-sink": (2, 3579, 4578),
    "pet-locker": (2, 4608, 5934),
    "head-wearables": (2, 5964, 7191),
    "dance-video-app": (4, 39, 1761),
    "property-legal-app": (4, 1812, 3720),
    "souffle-jewelry": (4, 3768, 5592),
    "atlantic-collage": (4, 5643, 7149),
    "sky-city": (5, 48, 1539),
    "zeon-identity": (5, 1590, 2634),
    "hotel-cover": (5, 2685, 3663),
    "spatial-audio": (5, 3714, 4830),
    "realtime-visuals": (5, 4857, 5856),
    "drone-render": (5, 5862, 7191),
}


def trim_columns(img):
    a = np.asarray(img.convert("RGB")).astype(int)
    is_bg = (np.abs(a - BG).sum(axis=2) < 25).mean(axis=0) > 0.97
    cols = np.where(~is_bg)[0]
    if len(cols) == 0:
        return img
    return img.crop((int(cols[0]), 0, int(cols[-1]) + 1, img.height))


def main():
    (OUT / "sm").mkdir(parents=True, exist_ok=True)
    sheets = {}
    for slug, (sheet, top, bottom) in CROPS.items():
        if sheet not in sheets:
            sheets[sheet] = Image.open(ROOT / f"portfolio-{sheet}.png").convert("RGB")
        src = sheets[sheet]
        piece = trim_columns(src.crop((0, top, src.width, bottom)))
        if piece.width > 1600:
            piece = piece.resize((1600, round(piece.height * 1600 / piece.width)), Image.LANCZOS)
        piece.save(OUT / f"{slug}.webp", "WEBP", quality=82, method=6)
        small = piece.resize((900, round(piece.height * 900 / piece.width)), Image.LANCZOS)
        small.save(OUT / "sm" / f"{slug}.webp", "WEBP", quality=78, method=6)
        print(f"{slug:22s} {piece.width}x{piece.height}")


if __name__ == "__main__":
    main()
