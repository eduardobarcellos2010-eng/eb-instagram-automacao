#!/usr/bin/env python
"""Exporta um carrossel HTML em PNGs 1080x1350 com valida??o anti-corte."""
from __future__ import annotations
import argparse, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from urllib.parse import quote
from PIL import Image

CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
PAGE_BG = (232, 233, 237)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path, help="index.html do carrossel")
    ap.add_argument("saida", type=Path, help="pasta de PNGs")
    ap.add_argument("--slides", type=int, required=True, help="quantidade de cards")
    args = ap.parse_args()
    if not CHROME.exists(): raise SystemExit(f"Chrome n?o encontrado: {CHROME}")
    if not args.html.exists(): raise SystemExit(f"Arquivo n?o encontrado: {args.html}")
    args.saida.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="eb-carousel-render-"))
    try:
        url_base = args.html.resolve().as_uri()
        for n in range(1, args.slides + 1):
            target = args.saida / f"slide-{n:02d}.png"
            url = f"{url_base}?export={n}"
            command = [str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                       "--no-first-run", "--no-default-browser-check", "--disable-background-networking",
                       f"--user-data-dir={profile}", "--window-size=1080,1350",
                       f"--screenshot={target}", url]
            subprocess.run(command, check=True, timeout=60, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not target.exists(): raise RuntimeError(f"Slide {n} n?o foi renderizado")
        validar(args.saida, args.slides)
        prancha(args.saida, args.slides)
        print(f"OK: {args.slides} PNGs validados em {args.saida}")
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    return 0

def validar(folder: Path, total: int) -> None:
    for n in range(1, total + 1):
        path = folder / f"slide-{n:02d}.png"
        with Image.open(path).convert("RGB") as im:
            if im.size != (1080, 1350):
                raise RuntimeError(f"{path.name}: esperado 1080x1350, recebido {im.size}")
            preview = im.resize((108, 135))
            blank = sum(1 for px in preview.getdata() if sum(abs(px[i]-PAGE_BG[i]) for i in range(3)) < 12)
            if blank / (108 * 135) > 0.05:
                raise RuntimeError(f"{path.name}: ?rea vazia detectada; n?o publicar")

def prancha(folder: Path, total: int) -> None:
    thumbs=[]
    for n in range(1, total + 1):
        with Image.open(folder / f"slide-{n:02d}.png").convert("RGB") as im:
            thumbs.append(im.resize((216, 270)))
    cols=4; rows=(total+cols-1)//cols
    sheet=Image.new("RGB", (cols*216, rows*270), PAGE_BG)
    for i,im in enumerate(thumbs): sheet.paste(im, ((i%cols)*216, (i//cols)*270))
    sheet.save(folder / "prancha-validacao.jpg", quality=90)

if __name__ == "__main__":
    raise SystemExit(main())
