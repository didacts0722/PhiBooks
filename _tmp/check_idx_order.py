# -*- coding: utf-8 -*-
"""检查 index JSON 的页面顺序与 § 段落的实际顺序"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

idx = json.loads(Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))
print("页面数:", len(idx))
print("--- 页面顺序（前 30） ---")
for pg in idx[:30]:
    print(" ", pg.get("file"))
# 检查 § 段实际顺序（伦理部分 142-360）
secs = []
for pg in idx:
    cur = None
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            if m:
                cur = int(m.group(1))
        elif it["type"] == "p" and cur and 142 <= cur <= 360:
            secs.append(cur)
print(f"伦理 §142-360 段落流（前 40 个 sec）:")
print(secs[:40])
bad = sum(1 for a, b in zip(secs, secs[1:]) if b < a)
print(f"逆序次数: {bad} / {len(secs)}")
