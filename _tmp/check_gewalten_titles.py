# -*- coding: utf-8 -*-
"""检查三权页面标题（h4/h5）中的 § 范围 + 页码分布"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")
for fn in ["a._Die_fürstliche_Gewalt.html", "b._Die_Regierungsgewalt.html", "c._Die_gesetzgebende_Gewalt.html"]:
    txt = (OUT / fn).read_bytes().decode("iso-8859-1", errors="replace")
    hs = re.findall(r"<h[45][^>]*>(.*?)</h[45]>", txt, re.S)
    htxt = [re.sub(r"<[^>]+>", "", h).strip() for h in hs]
    # 正文区截断
    marks = [txt.find("zenoPLBookTextMore"), txt.find("zenoTRNavBottom")]
    marks = [i for i in marks if i > 0]
    end = min(marks) if marks else len(txt)
    body = txt[:end]
    # 正文区 § 引用（段内）
    sec_refs = re.findall(r"§\s*(\d+)", re.sub(r"<[^>]+>", " ", body))
    pages = re.findall(r'name="(\d+)"', body)
    print(f"=== {fn}")
    print("   h4/h5:", [h[:40] for h in htxt[:8]])
    print("   正文区页码锚:", sorted(set(int(p) for p in pages))[:14])
    print()
