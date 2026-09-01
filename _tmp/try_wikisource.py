# -*- coding: utf-8 -*-
"""尝试 Wikisource：法哲学页面是否存在"""
import re
import sys
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
}

tests = [
    ("WS 主页面", "https://de.wikisource.org/wiki/Grundlinien_der_Philosophie_des_Rechts"),
    ("WS 搜索", "https://de.wikisource.org/w/index.php?search=Grundlinien+der+Philosophie+des+Rechts&title=Spezial:Suche&fulltext=1"),
]
for label, url in tests:
    print(f"=== {label}")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = resp.read()
        print(f"   {resp.status} | {len(data)}B")
        txt = data.decode("utf-8", errors="replace")
        m = re.search(r"<title>(.*?)</title>", txt, re.S)
        print("   title:", m.group(1).strip() if m else "?")
        # 搜索页：找结果链接
        links = re.findall(r'href="(/wiki/[^"]*Grundlinien[^"]*)"', txt)
        print("   结果链接:", list(dict.fromkeys(links))[:8])
    except urllib.error.HTTPError as e:
        print(f"   HTTPError {e.code}")
    except Exception as e:
        print(f"   FAIL: {e}")
    print()
