#!/usr/bin/env python3
"""Check whether <name>.<tld> is registered, across many TLDs.

Usage: domain-check.py NAME [NAME...] [--tlds com,it] [--all] [--json]

Method per domain, first that answers wins:
  1. RDAP (server from the IANA bootstrap file): 200 = registered, 404 = available
  2. WHOIS over port 43 (server from whois.iana.org): matched against known phrases
  3. otherwise "unknown" (a DNS hit still proves "registered")
Standard library only. Status is one of: registered, available, unknown.
"""
import argparse
import json
import socket
import sys
import threading
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path(__file__).parent / "data"
BOOTSTRAP = "https://data.iana.org/rdap/dns.json"
TIMEOUT = 10
PER_HOST = 2  # concurrent requests per server

NOT_FOUND = ("no match", "not found", "no data found", "no entries found",
             "is free", "status: free", "status: available", "available for registration",
             "no object found", "domain not found", "nothing found")
FOUND = ("registrar:", "creation date", "created:", "registry domain id", "status: active",
         "name server", "nserver", "status: connect", "registrant")

_locks = {}
_locks_guard = threading.Lock()


def host_lock(host):
    with _locks_guard:
        return _locks.setdefault(host, threading.Semaphore(PER_HOST))


def load_tlds(path):
    return [l.strip().lower() for l in path.read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def load_bootstrap():
    with urllib.request.urlopen(BOOTSTRAP, timeout=TIMEOUT) as r:
        services = json.load(r)["services"]
    out = {}
    for tlds, urls in services:
        url = sorted(urls, key=lambda u: not u.startswith("https"))[0].rstrip("/")
        for t in tlds:
            out[t.lower()] = url
    return out


def rdap(domain, base):
    url = f"{base}/domain/{domain}"
    for _ in range(2):
        host = base.split("//")[1].split("/")[0]
        with host_lock(host):
            try:
                req = urllib.request.Request(url, headers={"Accept": "application/rdap+json", "User-Agent": "launchpad-domain-check/1.0"})
                with urllib.request.urlopen(req, timeout=TIMEOUT):
                    return "registered"
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return "available"
                if e.code != 429:
                    return None
            except Exception:
                return None
        threading.Event().wait(2)
    return None


def whois_query(server, query):
    with host_lock(server):
        with socket.create_connection((server, 43), timeout=TIMEOUT) as s:
            s.sendall((query + "\r\n").encode("idna" if query.isascii() else "utf-8"))
            chunks = []
            while True:
                b = s.recv(4096)
                if not b:
                    break
                chunks.append(b)
    return b"".join(chunks).decode("utf-8", "replace")


_whois_servers = {}


def whois_server(tld):
    if tld not in _whois_servers:
        try:
            for line in whois_query("whois.iana.org", tld).splitlines():
                if line.lower().startswith("whois:"):
                    _whois_servers[tld] = line.split(":", 1)[1].strip() or None
                    break
            else:
                _whois_servers[tld] = None
        except Exception:
            _whois_servers[tld] = None
    return _whois_servers[tld]


def whois(domain, tld):
    server = whois_server(tld)
    if not server:
        return None
    try:
        text = " ".join(whois_query(server, domain).lower().split())
    except Exception:
        return None
    if any(p in text for p in NOT_FOUND):
        return "available"
    if any(p in text for p in FOUND):
        return "registered"
    return None


def dns_registered(domain):
    try:
        socket.getaddrinfo(domain, None)
        return True
    except Exception:
        return False


def check(name, tld, bootstrap):
    domain = f"{name}.{tld}"
    try:
        ascii_domain = domain.encode("idna").decode()
        ascii_tld = tld.encode("idna").decode()
    except UnicodeError:
        return {"domain": domain, "status": "unknown", "method": "invalid-name"}
    status, method = None, None
    if ascii_tld in bootstrap:
        status, method = rdap(ascii_domain, bootstrap[ascii_tld]), "rdap"
    if status is None:
        status, method = whois(ascii_domain, ascii_tld), "whois"
    if status is None:
        if dns_registered(ascii_domain):
            status, method = "registered", "dns"
        else:
            status, method = "unknown", "none"
    return {"domain": domain, "status": status, "method": method}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("names", nargs="+", help="label(s) without TLD, e.g. acme")
    ap.add_argument("--tlds", help="comma-separated TLDs (overrides the default list)")
    ap.add_argument("--all", action="store_true", help="check every open TLD in data/tlds-all.txt")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--workers", type=int, default=32)
    a = ap.parse_args()

    if a.tlds:
        tlds = [t.strip().lstrip(".").lower() for t in a.tlds.split(",") if t.strip()]
    else:
        tlds = load_tlds(DATA / ("tlds-all.txt" if a.all else "tlds-default.txt"))
    names = [n.strip().lower().replace(" ", "") for n in a.names]

    try:
        bootstrap = load_bootstrap()
    except Exception as e:
        print(f"warning: RDAP bootstrap unavailable ({e}); using whois/DNS only", file=sys.stderr)
        bootstrap = {}

    jobs = [(n, t) for n in names for t in tlds]
    with ThreadPoolExecutor(a.workers) as ex:
        results = list(ex.map(lambda j: check(j[0], j[1], bootstrap), jobs))

    if a.json:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return
    if a.all:
        print("note: --all includes closed brand/restricted TLDs; an 'available' there is "
              "not necessarily registrable. Add such TLDs to data/tlds-denylist.txt.\n")
    for n in names:
        rs = [r for r in results if r["domain"].startswith(n + ".")]
        print(f"## {n}")
        for status in ("available", "unknown", "registered"):
            sel = [r for r in rs if r["status"] == status]
            if sel:
                body = ", ".join(r["domain"].split(".", 1)[1] + (f" ({r['method']})" if status != "available" and r["method"] != "rdap" else "") for r in sel)
                print(f"{status} ({len(sel)}): {body}")
        print()


if __name__ == "__main__":
    main()
