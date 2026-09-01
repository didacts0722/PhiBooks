# -*- coding: utf-8 -*-
"""检查 7 个内部国家法 JSON：段落数、段内是否含 § 号、内容关键词"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EX = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted")
names = [
    "Das_Innere_Staatsrecht.json",
    "I._Innere_Verfassung_für_sich.json",
    "Innere_Verfassung_für_sich.json",
    "a._Die_fürstliche_Gewalt.json",
    "b._Die_Regierungsgewalt.json",
    "c._Die_gesetzgebende_Gewalt.json",
    "II._Die_Souveränität_gegen_außen.json",
]
for n in names:
    f = EX / n
    if not f.exists():
        print(f"=== {n}：不存在")
        continue
    d = json.loads(f.read_text(encoding="utf-8-sig"))
    items = d["items"]
    ps = [it for it in items if it["type"] == "p"]
    hs = [it for it in items if it["type"] in ("h4", "h5")]
    # 段落内 § 号
    sec_in_para = []
    for it in ps:
        m = re.findall(r"§\s*(\d+)", it["text"])
        if m:
            sec_in_para.append(m[0])
    print(f"=== {n}：{len(items)} items（p={len(ps)} h={len(hs)}）")
    if ps:
        print(f"   首段: {ps[0]['text'][:60]}")
        print(f"   末段: {ps[-1]['text'][:60]}")
        print(f"   段内§号: {sec_in_para[:12]}")
    print()
