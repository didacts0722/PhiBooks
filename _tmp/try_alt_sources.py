# -*- coding: utf-8 -*-
"""尝试替代德文原文源：Wikisource / Gutenberg 等"""
import re
import sys
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}

tests = [
    ("de.wikisource", "https://de.wikisource.org/wiki/Grundlinien_der_Philosophie_des_Rechts"),
    ("de.wikisource API", "https://de.wikisource.org/w/api.php?action=query&list=search&srsearch=Grundlinien%20der%20Philosophie%20des%20Rechts&format=json&srlimit=5"),
    ("textlog", "https://www.textlog.de/hegel-rechtsphilosophie.html"),
    ("gutenberg", "https://www.projekt-gutenberg.org/hegel/rechtsph/rechtsph.html"),
]
for label, url in tests:
    print(f"=== {label}: {url[:80]}")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = resp.read()
        print(f"   {resp.status} | {len(data)}B | {resp.geturl()[:100]}")
        txt = data.decode("utf-8", errors="replace")
        head = re.sub(r"<[^>]+>", " ", txt[:600])
        print("   开头:", " ".join(head.split())[:150])
    except urllib.error.HTTPError as e:
        print(f"   HTTPError {e.code}")
    except Exception as e:
        print(f"   FAIL: {e}")
    print()
