#!/usr/bin/env python3
import os, sys
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    raise SystemExit('Pillow is required to generate launcher icons')
source = Path(os.environ['LOGO_FILE'])
root = Path('app/src/main/res')
image = Image.open(source).convert('RGBA')
for density, size in {'mdpi':48, 'hdpi':72, 'xhdpi':96, 'xxhdpi':144, 'xxxhdpi':192}.items():
    out = root / f'mipmap-{density}'
    out.mkdir(parents=True, exist_ok=True)
    image.copy().thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (size, size), (255,255,255,0))
    scaled = image.copy(); scaled.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas.paste(scaled, ((size-scaled.width)//2, (size-scaled.height)//2), scaled)
    canvas.save(out / 'ic_launcher.png', 'PNG')
