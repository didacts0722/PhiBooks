# -*- coding: utf-8 -*-
"""诊断 zeno URL：HTTP 状态码、重定向、内容来源"""
import re
import sys
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}
P = ("/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/Grundlinien+der+Philosophie+des+Rechts/"
     "Dritter+Teil.+Die+Sittlichkeit/Dritter+Abschnitt.+Der+Staat/")

tests = [
    ("http", P + "A.+Das+Innere+Staatsrecht/%5BDas+Innere+Staatsrecht%5D"),
    ("https", P + "A.+Das+Innere+Staatsrecht/%5BDas+Innere+Staatsrecht%5D"),
    ("http", P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/a.+Die+f%C3%BCrstliche+Gewalt"),
    ("https", P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/a.+Die+f%C3%BCrstliche+Gewalt"),
    ("http", "/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/Grundlinien+der+Philosophie+des+Rechts"),
    ("http", P),  # Der_Staat 目录页（已成功抓过）
]
for scheme, path in tests:
    url = f"{scheme}://www.zeno.org{path}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as resp:
            code = resp.status
            final = resp.geturl()
            data = resp.read()
        txt = data.decode("iso-8859-1", errors="replace")
        hs = re.findall(r"<h[45][^>]*>(.*?)</h[45]>", txt, re.S)
        htxt = [re.sub(r"<[^>]+>", "", h).strip()[:40] for h in hs[:3]]
        print(f"[{scheme}] {code} | 最终URL: {final[:90]}")
        print(f"    {len(data)}B | 标题: {htxt}")
    except urllib.error.HTTPError as e:
        print(f"[{scheme}] HTTPError {e.code}")
    except Exception as e:
        print(f"[{scheme}] FAIL: {e}")
    print()
