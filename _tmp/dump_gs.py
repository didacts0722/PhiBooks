# -*- coding: utf-8 -*-
"""dump §182-256 市民社会段落原文（供引文选取），输出到 _tmp/gs_s182_256.txt"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

IDX = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json")
out = Path(r"_tmp/gs_s182_256.txt")

idx = json.loads(IDX.read_text(encoding="utf-8-sig"))
lines = []
for pg in idx:
    cur = None
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            if m:
                cur = int(m.group(1))
        elif it["type"] == "p" and cur and 182 <= cur <= 256:
            txt = it["text"].replace("\n", " ")
            lines.append(f"[§{cur}|p.{it.get('page')}|{pg.get('file')}] {txt}")
out.write_text("\n\n".join(lines), encoding="utf-8")
print(f"写出 {len(lines)} 段 -> {out}")
