# -*- coding: utf-8 -*-
"""dump §257-360 国家部分原文（书序），输出到 _tmp/gs_s257_360.txt"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

IDX = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json")
out = Path(r"_tmp/gs_s257_360.txt")

idx = json.loads(IDX.read_text(encoding="utf-8-sig"))
raw = []
for pg in idx:
    cur = None
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            if m:
                cur = int(m.group(1))
        elif it["type"] == "p" and cur and 257 <= cur <= 360:
            raw.append({"sec": cur, "page": it.get("page"), "text": it["text"].replace("\n", " ")})
raw.sort(key=lambda p: p["sec"])  # 书序
lines = []
for p in raw:
    lines.append(f"[§{p['sec']}|p.{p['page']}] {p['text']}")
out.write_text("\n\n".join(lines), encoding="utf-8")
print(f"写出 {len(raw)} 段（§{raw[0]['sec']}-§{raw[-1]['sec']}） -> {out}")
