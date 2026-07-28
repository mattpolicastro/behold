# gyre

Spin a 3D model in your terminal. One file, no dependencies.

> Turning and turning in the widening gyre…

```sh
gyre                        # spins the bundled model
gyre model.fbx --blocks     # half-blocks, truecolour, transparent background
gyre model.stl --ascii      # character ramp, 256-colour
```

Loads `.obj`, `.stl` (binary + ASCII) and binary `.fbx`, then software-renders
it — perspective projection, z-buffer, Gouraud + specular shading — straight to
your terminal at 15–30 fps.

## Install

Needs **python3 and nothing else**. No numpy, no Pillow, no FBX SDK.

```sh
curl -o ~/.local/bin/gyre https://raw.githubusercontent.com/mattpolicastro/gyre/main/gyre
chmod +x ~/.local/bin/gyre

# optional: the bundled model, so bare `gyre` has something to spin
mkdir -p ~/.local/share/gyre
curl -o ~/.local/share/gyre/spot.obj https://raw.githubusercontent.com/mattpolicastro/gyre/main/models/spot.obj
```

Run with no arguments and `gyre` spins **Spot**, by [Keenan Crane][spot],
released into the public domain — see [`models/NOTICE.md`](models/NOTICE.md).
It looks for the model next to the script (following symlinks) and then in
`$XDG_DATA_HOME/gyre`, falling back to `--demo torus` if it finds neither.

Otherwise pass a file — anything Blender exports will do.

[spot]: https://www.cs.cmu.edu/~kmcrane/Projects/ModelRepository/

## Output modes

`gyre` picks the best mode your terminal supports, and you can force any of them.

| mode | flag | what you get |
|---|---|---|
| Kitty graphics | *(default where supported)* | real pixels — Ghostty, Kitty, WezTerm |
| Half-blocks | `--blocks` | `▀`/`▄` cells, 24-bit colour, 2× vertical resolution, terminal background shows through |
| Character ramp | `--ascii` | ` .:-=+*#%@` in a 256-colour bronze→gold palette |

Half-block mode leaves the background *unset* rather than painting it black, so
it composites over whatever your terminal background is — it looks native rather
than like a pasted-in rectangle.

## Options

```
--speed N        rotation, radians/second (default 1.0)
--fps N          frame rate cap (default 20)
--pitch N        camera tilt in radians (default 0.45)
--zoom N         scale factor; <1 leaves more margin (default 1.0)
--duration N     stop after N seconds (default: until Ctrl-C)
--still ANGLE    render one frame and exit
--cols / --rows  override the auto-detected viewport
--cell N         pixels per cell (default: ask the terminal)
--budget N       max samples/frame; caps cost on big windows (default 260000)
--truecolor      smooth 24-bit gold in --ascii instead of the stepped palette
--spec           specular highlight in --ascii
--mono           no colour
--keep           draw inline and leave the last frame on screen
--demo torus|cube   built-in mesh instead of the bundled model
```

## How it works

Everything is stdlib, which forced a few things to be written out longhand:

- **Rasteriser.** Perspective projection, then a z-buffered barycentric
  triangle fill. Shading is Lambert plus a specular term, interpolated across
  vertex normals where the file has them and computed per-face where it
  doesn't.
- **Two-sided shading, no backface culling.** Meshes disagree about winding
  order constantly, and guessing wrong lights the interior of the model instead
  of the exterior. Normals facing away from the camera are flipped and the
  z-buffer sorts out occlusion, so any file renders correctly regardless of
  convention.
- **Framing is measured, not bounded.** A bounding sphere is a terrible fit for
  a flat model — it can waste 40% of the frame. Instead `gyre` sweeps a full
  rotation at startup, finds the widest actual projection, and solves the focal
  length so that peak lands exactly at the frame edge. Fixed for the whole
  animation, so the model doesn't pulse as it turns.
- **Real cell geometry.** Terminal cells aren't exactly 2:1. `gyre` asks via
  `CSI 16 t` and uses the answer, falling back to the usual assumption if the
  terminal stays quiet. A ~6% aspect error is very visible on a spinning object.
- **PNG encoder** for the Kitty path — about fifteen lines of `zlib`.
- **FBX reader.** Binary FBX is a tree of length-prefixed records with
  zlib-deflated array properties, and polygons mark their last vertex by
  bitwise-NOT. Roughly eighty lines, no SDK.

- **Leaves your terminal alone.** The animation runs on the alternate screen
  buffer, so the terminal snapshots what you had and restores it exactly when
  `gyre` exits — no clearing, no clobbered scrollback. Kitty image placements
  aren't part of that snapshot, so they're deleted explicitly first. Cleanup
  runs on SIGINT, SIGTERM and SIGHUP, and is flushed. `--keep` opts out and
  draws inline.

On a large window the Kitty path renders at true 1:1 pixels until that exceeds
the sample budget, then it renders smaller and lets the terminal scale it up —
so framerate stays put whether the window is 80 columns or 300.

## Prior art

Terminal 3D is well-trodden — there are plenty of ASCII OBJ renderers, and
[chafa][] and [timg][] are excellent at getting *images* into terminals. If you
want the best quality, rendering with a real engine and piping frames to one of
those will beat this.

`gyre`'s niche is narrow and deliberate: a single file you can `scp` anywhere
that already has python3, which takes a *mesh* rather than an image.

[chafa]: https://hpjansson.org/chafa/
[timg]: https://github.com/hzeller/timg

## License

MIT
