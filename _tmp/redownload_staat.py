# -*- coding: utf-8 -*-
"""重新下载法哲学内部国家法 7 个错误页面（zeno 正确 URL），验证内容后覆盖保存"""
import json
import re
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}
BASE = "http://www.zeno.org"
P = ("/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/Grundlinien+der+Philosophie+des+Rechts/"
     "Dritter+Teil.+Die+Sittlichkeit/Dritter+Abschnitt.+Der+Staat/")

TARGETS = [
    # (url 片段, 本地文件名)
    (P + "A.+Das+Innere+Staatsrecht/%5BDas+Innere+Staatsrecht%5D", "Das_Innere_Staatsrecht.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich", "I._Innere_Verfassung_für_sich.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/%5BInnere+Verfassung+f%C3%BCr+sich%5D", "Innere_Verfassung_für_sich.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/a.+Die+f%C3%BCrstliche+Gewalt", "a._Die_fürstliche_Gewalt.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/b.+Die+Regierungsgewalt", "b._Die_Regierungsgewalt.html"),
    (P + "A.+Das+Innere+Staatsrecht/I.+Innere+Verfassung+f%C3%BCr+sich/c.+Die+gesetzgebende+Gewalt", "c._Die_gesetzgebende_Gewalt.html"),
    (P + "A.+Das+Innere+Staatsrecht/II.+Die+Souver%C3%A4nit%C3%A4t+gegen+au%C3%9Fen", "II._Die_Souveränität_gegen_außen.html"),
]

OUT = r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts"


def fetch(url: str, retries: int = 3) -> bytes:
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as e:
            last = e
            print(f"    重试 {i + 1}/{retries}: {e}")
            time.sleep(3)
    raise last


def validate(name: str, data: bytes) -> tuple:
    """验证：内容含 § 标题(h4/h5) 或正文，且非他书跳转"""
    txt = data.decode("iso-8859-1", errors="replace")
    hs = re.findall(r"<h[45][^>]*>(.*?)</h[45]>", txt, re.S)
    htxt = [re.sub(r"<[^>]+>", "", h).strip() for h in hs]
    secs = [h for h in htxt if re.match(r"§\s*\d+", h)]
    # 黑格尔正文特征词
    hegel_words = sum(w in txt for w in ["Gewalt", "Verfassung", "Sittlichkeit", "Monarch", "Hegel"])
    # 他书跳转特征（zeno 随机跳转页的标题）
    foreign = any(w in h for h in htxt for w in ["Schlegel", "Florentin", "Schnitzler", "Tschechow", "Lewald", "Grabbe", "Wei"])
    return len(data), len(secs), hegel_words, foreign, htxt[:3]


print("=== 重新下载内部国家法页面 ===")
ok = 0
for url, fname in TARGETS:
    print(f"-- {fname}")
    data = fetch(BASE + url)
    size, nsec, hw, foreign, h3 = validate(fname, data)
    print(f"   {size}B | §标题={nsec} | 黑格尔词={hw} | 他书跳转={foreign}")
    if h3:
        print("   前3标题:", [h[:36] for h in h3])
    if size < 5000 or foreign:
        print("   !! 疑似错误内容，跳过覆盖")
        continue
    with open(rf"{OUT}\{fname}", "wb") as f:
        f.write(data)
    print(f"   OK 已覆盖 {fname}")
    ok += 1
    time.sleep(1)
print(f"\n完成：{ok}/{len(TARGETS)} 页已更新")
