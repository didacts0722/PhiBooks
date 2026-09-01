# -*- coding: utf-8 -*-
"""抓取 marxists.org 马克思《法哲学批判》德文版 §296-298"""
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}
cands = [
    "https://www.marxists.org/deutsch/archiv/marx/1843/kritik-hegel/14-staatsrecht.htm",
    "https://www.marxists.org/deutsch/archiv/marx/1843/kritik-hegel/",
]
for url in cands:
    print("=== ", url)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = resp.read()
        txt = data.decode("utf-8", errors="replace")
        print(f"   {len(txt)}B")
        plain = re.sub(r"<[^>]+>", " ", txt)
        plain = re.sub(r"\s+", " ", plain)
        for s in range(295, 301):
            i = plain.find(f"§ {s}.")
            if i >= 0:
                print(f"   §{s}: {plain[i:i+150]}")
        break
    except Exception as e:
        print(f"   FAIL {e}")
