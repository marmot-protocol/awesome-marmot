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

generation_labels = {
    "current-spec",
    "legacy-spec",
    "transitional",
    "unknown",
    "adjacent",
}
activity_labels = {"active", "inactive", "archived"}
for line_number, line in enumerate(text.splitlines(), 1):
    if not (line.startswith("- [") and "http" in line):
        continue
    if "**" not in line:
        errors.append(f"catalog entry lacks explicit labels at line {line_number}")
        continue
    if not any(label in line for label in generation_labels):
        errors.append(f"catalog entry lacks a protocol-generation label at line {line_number}")
    if not any(label in line for label in activity_labels):
        errors.append(f"catalog entry lacks a repository-activity label at line {line_number}")

required_fragments = {
    "Marmot for Hermes": "first-party Hermes connector",
    "Marmot for OpenClaw": "first-party OpenClaw connector",
    "wn-codex": "first-party Codex connector",
    "wn-opencode": "first-party OpenCode connector",
    "wn-pi": "first-party Pi connector",
}
for fragment, purpose in required_fragments.items():
    if fragment not in text:
        errors.append(f"missing {purpose}: {fragment}")

for obsolete in (
    "https://github.com/marmot-protocol/mdk-web",
    "https://github.com/marmot-protocol/mdk-ruby-example",
    "Marmot Improvement Proposals (MIPs)",
    "MIP-05 notification server",
):
    if obsolete in text:
        errors.append(f"obsolete or non-substantive catalog content remains: {obsolete}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"catalog structure OK: {len(urls)} GitHub links checked")
