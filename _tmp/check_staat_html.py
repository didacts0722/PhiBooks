# -*- coding: utf-8 -*-
"""检查内部国家法相关原始 HTML：是否含 § 标题、内容是否黑格尔"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")
names = [
    "Das_Innere_Staatsrecht.html",
    "I._Innere_Verfassung_für_sich.html",
    "Innere_Verfassung_für_sich.html",
    "a._Die_fürstliche_Gewalt.html",
    "b._Die_Regierungsgewalt.html",
    "c._Die_gesetzgebende_Gewalt.html",
    "II._Die_Souveränität_gegen_außen.html",
    "A._Das_Innere_Staatsrecht.html",
]
for n in names:
    f = BASE / n
    if not f.exists():
        print(f"=== {n}：文件不存在！")
        continue
    txt = f.read_text(encoding="utf-8", errors="replace")
    hs = re.findall(r"<h[45][^>]*>(.*?)</h[45]>", txt, re.S)
    htxt = [re.sub(r"<[^>]+>", "", h).strip() for h in hs]
    sec_titles = [h for h in htxt if re.match(r"§\s*\d+", h)]
    hegel = "Hegel" in txt or "Grundlinien" in txt or "Sittlichkeit" in txt
    print(f"=== {n}：{len(txt)}B | h4/h5={len(htxt)} | §标题={len(sec_titles)} | 黑格尔内容={hegel}")
    if htxt:
        print("   前4标题:", [h[:40] for h in htxt[:4]])
    if sec_titles:
        print("   §标题:", [h[:14] for h in sec_titles[:10]])
