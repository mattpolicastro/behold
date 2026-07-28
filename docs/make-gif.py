#!/usr/bin/env python3
"""Render behold's ASCII mode to a shareable animated GIF.

Draws the actual characters in a monospace face, coloured with the same
xterm-256 gold ramp the terminal uses, so the GIF looks like the terminal.
"""
import importlib.util, math, os, sys
from PIL import Image, ImageDraw, ImageFont

G = os.path.expanduser("~/Projects/behold/behold")
spec = importlib.util.spec_from_loader("behold",
                                       importlib.machinery.SourceFileLoader("behold", G))
behold = importlib.util.module_from_spec(spec)
sys.argv = ["behold"]
spec.loader.exec_module(behold)

FONT = "/System/Library/Fonts/Menlo.ttc"
SIZE = 15
COLS, ROWS = 58, 34
FRAMES = 48
BG = (24, 26, 31)


def xterm(i):
    """xterm-256 index -> RGB (cube region only; our ramp lives there)."""
    lv = (0, 95, 135, 175, 215, 255)
    i -= 16
    return lv[i // 36], lv[(i // 6) % 6], lv[i % 6]


PAL = [xterm(i) for i in behold.GOLD]


def main(out="spot-ascii.gif", model=None):
    model = model or os.path.expanduser("~/Projects/behold/models/spot.obj")
    verts, norms, faces = behold.load_mesh(model)
    verts = behold.normalise(verts)

    font = ImageFont.truetype(FONT, SIZE)
    cw = font.getlength("M")
    ch = int(SIZE * 1.22)
    W, H = int(COLS * cw), ROWS * ch
    ay = cw / ch
    focal = behold.fit_focal(verts, COLS, ROWS, ay, 0.34, 3.2, 0.90)
    print(f"{len(faces)} tris, {COLS}x{ROWS} cells, {W}x{H}px, {FRAMES} frames")

    frames = []
    for n in range(FRAMES):
        sh = behold.render(verts, norms, faces, COLS, ROWS,
                         2 * math.pi * n / FRAMES, 0.34, False,
                         ay=ay, focal=focal, spec=False)
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        for r in range(ROWS):
            run, lvl, x0 = [], None, 0
            for c in range(COLS + 1):
                v = sh[r * COLS + c] if c < COLS else 0.0
                L = (min(len(behold.RAMP) - 1, int(min(1.0, v) * len(behold.RAMP)))
                     if v > 0 else None)
                if L != lvl:
                    if lvl is not None and run:
                        d.text((x0 * cw, r * ch), "".join(run),
                               font=font, fill=PAL[lvl])
                    run, lvl, x0 = [], L, c
                if L is not None:
                    run.append(behold.RAMP[L])
            if lvl is not None and run:
                d.text((x0 * cw, r * ch), "".join(run), font=font, fill=PAL[lvl])
        frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=16))
        print(f"\r  frame {n+1}/{FRAMES}", end="", flush=True)

    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=55, loop=0, optimize=True, disposal=2)
    print(f"\nwrote {out}  ({os.path.getsize(out)/1024:.0f} KB)")


if __name__ == "__main__":
    main(*sys.argv[1:])
