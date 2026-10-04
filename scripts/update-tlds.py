#!/usr/bin/env python3
"""Rebuild data/tlds-all.txt from the IANA Root Zone Database.

Keeps `generic` and `country-code` TLDs; drops infrastructure, test,
sponsored and generic-restricted ones, plus anything in data/tlds-denylist.txt
(brand TLDs and other closed registries). Run occasionally; output is committed.
"""
import html
import unicodedata
import re
import urllib.request
from pathlib import Path

DATA = Path(__file__).parent / "data"
URL = "https://www.iana.org/domains/root/db"
KEEP = {"generic", "country-code"}

page = urllib.request.urlopen(URL, timeout=30).read().decode("utf-8")
rows = re.findall(
    r'<span class="domain tld"><a [^>]*>([^<]+)</a></span></td>\s*<td>([^<]+)</td>', page
)
deny = set()
deny_file = DATA / "tlds-denylist.txt"
if deny_file.exists():
    deny = {l.strip().lower() for l in deny_file.read_text().splitlines()
            if l.strip() and not l.startswith("#")}

tlds = sorted(
    {"".join(c for c in html.unescape(d) if unicodedata.category(c) != "Cf").lstrip(".").lower() for d, t in rows if t.strip() in KEEP} - deny
)
# IDN TLDs appear as unicode in the DB; keep them (RDAP bootstrap uses the same form).
(DATA / "tlds-all.txt").write_text("\n".join(tlds) + "\n")
print(f"{len(rows)} TLDs in root DB -> {len(tlds)} written to data/tlds-all.txt")
