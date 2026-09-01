# -*- coding: utf-8 -*-
"""抓取 zeno Der_Staat 目录页，列出全部子链接"""
import re
import sys
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}
url = ("http://www.zeno.org/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/"
       "Grundlinien+der+Philosophie+des+Rechts/Dritter+Teil.+Die+Sittlichkeit/"
       "Dritter+Abschnitt.+Der+Staat")
print("=== 抓取:", url)
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=60) as resp:
    data = resp.read()
txt = data.decode("iso-8859-1", errors="replace")
print(f"大小 {len(txt)}B")
links = []
for m in re.finditer(r'href="(/Philosophie/M/Hegel[^"]*)"', txt):
    h = m.group(1)
    if h not in links:
        links.append(h)
print(f"链接 {len(links)} 个：")
for h in links:
    print("  ", h)
