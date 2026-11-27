"""make.fun news-image-20261126 entry point.

Running this module produces the front page for Thursday 26 November
2026 — the day the US proposed tariffs on fourteen trading partners,
missiles flew over Kyiv while Ukraine struck a Russian power plant, a
drone attack in Kuwait killed two Italians, and Spain's Hernandez de
Cos was picked to lead the European Central Bank — and drops it at
/output/entry.png as an 800 by 800 PNG under one mebibyte.

The picture itself ships inside this repository next to this file, so
the program needs no network and no randomness: every run writes the
exact same bytes, which the digest comparison at the end confirms.
"""

from hashlib import file_digest
from os import environ
from pathlib import Path

SIZE_LIMIT = 1_048_576
PNG_SIGNATURE = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
SOURCE_NAME = "entry.png"


def build() -> Path:
    """Copy the shipped front page into the output directory."""
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if source.stat().st_size > SIZE_LIMIT:
        raise SystemExit(f"{SOURCE_NAME} is over the one-mebibyte limit")
    with source.open("rb") as handle:
        if handle.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            raise SystemExit(f"{SOURCE_NAME} does not start with a PNG signature")
    target_dir = Path(environ.get("OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / SOURCE_NAME
    target.write_bytes(source.read_bytes())
    if file_digest(source.open("rb"), "sha256").hexdigest() != (
        file_digest(target.open("rb"), "sha256").hexdigest()
    ):
        raise SystemExit("written image differs from the shipped front page")
    return target


build()
