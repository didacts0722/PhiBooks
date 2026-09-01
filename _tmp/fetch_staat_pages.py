# -*- coding: utf-8 -*-
"""逐个抓取内部国家法页面（用户确认 A.+Das+Innere+Staatsrecht 有内容），放慢防 503"""
import json
import re
import sys
import time
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}
BASE = "http://www.zeno.org"
P = ("/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/Grundlinien+der+Philosophie+des+Rechts/"
     "Dritter+Teil.+Die+Sittlichkeit/Dritter+Abschnitt.+Der+Staat/")

# 用户确认的 URL + 其余候选（不加子页方括号）
CANDIDATES = [
    (P + "A.+Das+Innere+Staatsrecht", "A._Das_Innere_Staatsrecht.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich", "I._Innere_Verfassung_für_sich.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/%5BInnere+Verfassung+f%C3%BCr+sich%5D", "Innere_Verfassung_für_sich.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/a.+Die+f%C3%BCrstliche+Gewalt", "a._Die_fürstliche_Gewalt.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/b.+Die+Regierungsgewalt", "b._Die_Regierungsgewalt.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/c.+Die+gesetzgebende+Gewalt", "c._Die_gesetzgebende_Gewalt.html"),
    (P + "A.+Das+Innere+Staatsrecht/II.+Die+Souver%C3%A4nit%C3%A4t+gegen+au%C3%9Fen", "II._Die_Souveränität_gegen_außen.html"),
]

OUT = r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def inspect(txt: str) -> tuple:
    hs = re.findall(r"<h[45][^>]*>(.*?)</h[45]>", txt, re.S)
    htxt = [re.sub(r"<[^>]+>", "", h).strip() for h in hs]
    secs = [h for h in htxt if re.match(r"§\s*\d+", h)]
    paras = re.findall(r"<p[^>]*>(.*?)</p>", txt, re.S)
    body = " ".join(re.sub(r"<[^>]+>", " ", p) for p in paras)
    kw = {w: (w in txt) for w in ["Innere Staatsrecht", "fürstliche Gewalt", "Regierungsgewalt", "gesetzgebende Gewalt", "Souveränität", "Verfassung"]}
    return len(txt), secs, htxt[:3], body[:120]


print("=== 逐个抓取 ===")
results = {}
for url, fname in CANDIDATES:
    print(f"-- {fname}")
    for attempt in range(4):
        try:
            data = fetch(BASE + url)
            break
        except urllib.error.HTTPError as e:
            print(f"   HTTPError {e.code}，等待 8s 重试")
            time.sleep(8)
        except Exception as e:
            print(f"   FAIL {e}，等待 8s 重试")
            time.sleep(8)
    else:
        print("   放弃")
        continue
    txt = data.decode("iso-8859-1", errors="replace")
    size, secs, h3, body = inspect(txt)
    print(f"   {size}B | §标题={len(secs)} | 前3标题={h3}")
    print(f"   正文开头: {body[:110]}")
    results[fname] = {"size": size, "secs": secs[:8], "h3": h3}
    time.sleep(4)

print("\n=== 汇总 ===")
for fname, r in results.items():
    print(f"{fname}: {r['size']}B §标题={len(r['secs'])} {r['secs'][:6]}")
