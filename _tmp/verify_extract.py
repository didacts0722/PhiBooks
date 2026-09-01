# -*- coding: utf-8 -*-
"""用 extract_zeno.extract_page 验证新下载的 7 页：正文区 items + § 标题分布"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")
from extract_zeno import extract_page  # noqa: E402

OUT = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")
names = [
    "A._Das_Innere_Staatsrecht.html",
    "I._Innere_Verfassung_für_sich.html",
    "Innere_Verfassung_für_sich.html",
    "a._Die_fürstliche_Gewalt.html",
    "b._Die_Regierungsgewalt.html",
    "c._Die_gesetzgebende_Gewalt.html",
    "II._Die_Souveränität_gegen_außen.html",
]
for n in names:
    d = extract_page(OUT / n)
    items = d["items"]
    hs = [it for it in items if it["type"] in ("h4", "h5")]
    ps = [it for it in items if it["type"] == "p"]
    sec_titles = [it["text"] for it in hs if re.match(r"§\s*\d+", it["text"])]
    print(f"=== {n}：items={len(items)}（h={len(hs)} p={len(ps)}）§标题={len(sec_titles)}")
    for it in hs[:5]:
        print(f"   H: {it['text'][:50]}")
    if ps:
        print(f"   首段: {ps[0]['text'][:70]}（p.{ps[0].get('page')}）")
        print(f"   末段: {ps[-1]['text'][:70]}（p.{ps[-1].get('page')}）")
    print()
