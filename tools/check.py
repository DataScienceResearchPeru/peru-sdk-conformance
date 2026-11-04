"""Check the versioned synthetic corpus and its integrity manifest."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    content = (ROOT / "cases.json").read_bytes()
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    if hashlib.sha256(content).hexdigest() != manifest["sha256"]:
        raise SystemExit("cases.json differs from the reviewed manifest")
    cases = json.loads(content)
    if cases["version"] != manifest["format_version"]:
        raise SystemExit("corpus format version mismatch")
    for group in ("query_cases", "response_cases", "identity_cases"):
        ids = [case["id"] for case in cases[group]]
        if not ids or len(ids) != len(set(ids)):
            raise SystemExit(f"empty or duplicate cases: {group}")
    for case in cases["response_cases"]:
        if ("expected" in case) == ("error" in case):
            raise SystemExit(f"ambiguous expected outcome: {case['id']}")
        if ("body" in case) == ("raw_body" in case):
            raise SystemExit(f"ambiguous response input: {case['id']}")
    print("Verified corpus:", sum(len(cases[k]) for k in ("query_cases", "response_cases", "identity_cases")), "cases")


if __name__ == "__main__":
    main()
