# -*- coding: utf-8 -*-
"""检查 §257-360 各段落在 index 的分布（找 §260-329 缺失原因）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

idx = json.loads(Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))

counts = {}
files_secs = {}
for pg in idx:
    cur = None
    n = 0
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            if m:
                cur = int(m.group(1))
        elif it["type"] == "p" and cur and 257 <= cur <= 360:
            counts[cur] = counts.get(cur, 0) + 1
            files_secs.setdefault(pg.get("file"), []).append(cur)
            n += 1

secs = sorted(counts)
print(f"覆盖 §: {secs[0]}-{secs[-1]}，共 {len(counts)} 个 §，{sum(counts.values())} 段")
missing = [s for s in range(257, 361) if s not in counts]
print(f"缺失 §: {missing}")

print("\n按页面统计（含 §260-329 的页面）：")
for f, ss in sorted(files_secs.items()):
    if any(260 <= s <= 329 for s in ss):
        print(f"  {f}: {min(ss)}-{max(ss)}（{len(ss)} 段）")
