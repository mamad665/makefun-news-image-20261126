"""Entry for make.fun news-image-20261126.

Writes the front page summing up Thursday 26 November 2026's world news
(US tariffs on 14 trading partners, missiles over Kyiv as Ukraine hits a
Russian power plant, drone attack in Kuwait killing two Italians, Spain's
Hernandez de Cos picked to lead the ECB, plus the Ibiza tanker, HIV jab,
Ebola and Netanyahu trial items) to /output/entry.png. Deterministic, no
network: it copies the image shipped in this repo.
"""
import hashlib
import os
import shutil

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if os.path.getsize(src) > MAX_BYTES:
        raise SystemExit("entry.png exceeds the 1 MiB gate")
    with open(src, "rb") as handle:
        if handle.read(len(PNG_MAGIC)) != PNG_MAGIC:
            raise SystemExit("entry.png is not a whole PNG file")
    dest = os.path.join(out, "entry.png")
    shutil.copyfile(src, dest)
    if _sha256(src) != _sha256(dest):
        raise SystemExit("output bytes differ from the shipped image")


if __name__ == "__main__":
    main()
