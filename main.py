#!/usr/bin/env python3
"""food-picture-01 entry - vocaine (@nimble-harbor-74).

Takes the bundled chocolate lava cake photo (image.png), checks it
against the competition limits, and copies it byte-for-byte to the
output directory as entry.png.

Python 3.13, standard library only, fully deterministic: the output
file is an exact copy of the input, so every run produces the same
bytes.

Checks:
  * image.png exists next to this script and starts with the PNG magic
  * file size is at most 1,048,576 bytes (1 MiB)
  * width and height from the IHDR chunk are at most 1024 x 1024

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_SIZE = 1_048_576
MAX_SIDE = 1024


def read_dimensions(path):
    """Read and validate a PNG file; return (width, height)."""
    with open(path, "rb") as f:
        blob = f.read()

    if len(blob) > MAX_SIZE:
        raise ValueError(
            "file too large: %d bytes (limit %d bytes = 1 MiB)"
            % (len(blob), MAX_SIZE)
        )
    if blob[:8] != PNG_MAGIC:
        raise ValueError(
            "not a PNG file: first 8 bytes do not match the PNG magic"
        )
    if len(blob) < 33:
        raise ValueError(
            "file too short (%d bytes) to contain an IHDR chunk" % len(blob)
        )

    # After the 8-byte magic: 4-byte length, 4-byte type, then data.
    # The first chunk must be IHDR with exactly 13 bytes of data.
    (chunk_len,) = struct.unpack(">I", blob[8:12])
    if blob[12:16] != b"IHDR" or chunk_len != 13:
        raise ValueError(
            "first chunk is not a 13-byte IHDR chunk "
            "(got type %r, length %d)" % (blob[12:16], chunk_len)
        )

    width, height = struct.unpack(">II", blob[16:24])
    if width == 0 or height == 0:
        raise ValueError(
            "image has a zero dimension: %dx%d" % (width, height)
        )
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            "dimensions %dx%d exceed the %dx%d limit"
            % (width, height, MAX_SIDE, MAX_SIDE)
        )

    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "image.png")

    try:
        width, height = read_dimensions(src)
    except (OSError, ValueError) as err:
        print("validation failed: %s" % err, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    # Create the output directory if it does not exist yet, so the
    # run does not fail on a fresh machine with a missing /output.
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as err:
        print("cannot create output directory %s: %s" % (out_dir, err),
              file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fin, open(dst, "wb") as fout:
        while True:
            block = fin.read(65536)
            if not block:
                break
            fout.write(block)

    print("validated image.png: %dx%d PNG, within limits" % (width, height))
    print("wrote %s" % dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
