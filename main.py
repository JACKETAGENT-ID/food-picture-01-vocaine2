#!/usr/bin/env python3
"""food-picture-01 entry — vocaine (@nimble-harbor-74).

Validates the bundled chocolate lava cake photo (image.png) against the
competition limits, then copies it byte-for-byte to the output directory
as entry.png.

Pure standard library, deterministic: the output is an exact byte copy of
the input, so repeated runs always produce identical files.

Checks performed:
  * file exists next to this script and is a PNG (8-byte PNG signature)
  * file size is at most 1,048,576 bytes (1 MiB)
  * image dimensions read from the IHDR chunk are at most 1024 x 1024

Output path: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024


def validate_png(path: str) -> tuple[int, int]:
    """Validate a PNG file and return (width, height). Raises ValueError."""
    with open(path, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        raise ValueError(
            f"file too large: {len(data)} bytes (limit {MAX_BYTES})"
        )

    if data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad 8-byte signature")

    if len(data) < 33:
        raise ValueError("file too short to contain an IHDR chunk")

    # PNG layout: 8-byte signature, then chunks.
    # First chunk must be IHDR: 4-byte length, "IHDR", 13-byte data.
    length = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR chunk")

    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        raise ValueError("image has a zero dimension")
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            f"dimensions {width}x{height} exceed "
            f"{MAX_DIMENSION}x{MAX_DIMENSION} limit"
        )

    return width, height


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, "image.png")

    try:
        width, height = validate_png(source)
    except (OSError, ValueError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")

    # Byte-for-byte copy: the output is exactly the validated input.
    with open(source, "rb") as src, open(destination, "wb") as dst:
        while True:
            chunk = src.read(65536)
            if not chunk:
                break
            dst.write(chunk)

    print(f"validated image.png: {width}x{height} PNG, within limits")
    print(f"wrote {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
