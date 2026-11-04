"""Produce a deterministic conformance archive with an explicit file allowlist."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

from check import ROOT, main as check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    check()
    version = json.loads((ROOT / "manifest.json").read_text())["version"]
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / f"peru-sdk-conformance-{version}.tar.gz"
    with target.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            for name in ("LICENSE", "README.md", "cases.json", "manifest.json"):
                data = (ROOT / name).read_bytes()
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(data), 0o644, 0
                archive.addfile(info, io.BytesIO(data))
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (args.output / "SHA256SUMS").write_text(f"{digest}  {target.name}\n")
    print(target)


if __name__ == "__main__":
    main()
