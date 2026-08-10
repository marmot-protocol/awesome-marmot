#!/usr/bin/env python3
"""Fast structural checks for the Markdown catalog."""

from pathlib import Path
import re
import sys


text = Path("README.md").read_text(encoding="utf-8")
errors: list[str] = []
urls = re.findall(r"https?://github\.com/[^/)\s]+/[^/)#\s]+", text, re.I)
normalized = [url.lower().removesuffix(".git") for url in urls]
allowed_repeats = {
    "https://github.com/marmot-protocol/marmot",
    "https://github.com/marmot-protocol/mdk",
    "https://github.com/vitorpamplona/amethyst",
}
for url in sorted(set(normalized)):
    if normalized.count(url) > 1 and url not in allowed_repeats:
        errors.append(f"duplicate canonical GitHub URL: {url}")

for line_number, line in enumerate(text.splitlines(), 1):
    if line.startswith("- [") and "http" in line and "**" not in line:
        errors.append(f"catalog entry lacks an explicit status at line {line_number}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"catalog structure OK: {len(urls)} GitHub links checked")
