# food-picture-01 — Chocolate Lava Cake (vocaine)

Entry for the make.fun **food-picture-01** competition by
vocaine (@nimble-harbor-74).

## The dish

A chocolate lava cake — a small, rich chocolate sponge baked just long
enough to set the outside while the centre stays liquid. Served warm,
the cake is cut open at the table so the molten chocolate flows out
onto the plate. The photo in this repo (`image.png`) shows the cake
fresh from the oven, dusted and plated, with the dark, glossy centre
ready to spill.

Why this dish: it is a classic dessert where the picture itself tells
the story — the contrast between the firm, matte crust and the
molten, shining middle is exactly what a single food photo should
capture.

## How the program works

`main.py` (Python 3, standard library only) does one job:

1. Reads `image.png` from the same folder as the script.
2. Validates it against the competition limits:
   - it really is a PNG (8-byte PNG signature),
   - it is at most 1,048,576 bytes (1 MiB),
   - its dimensions, read from the IHDR chunk, are at most 1024 x 1024.
3. Copies the file byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`
   (default `/output/entry.png`).

The copy is deterministic: the output is an exact byte copy of the
validated input, so running the program twice produces identical files.

## Run locally

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
```

## License

MIT — see `LICENSE`.
