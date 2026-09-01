# -*- coding: utf-8 -*-
"""最终验证大纲文档：节结构 + 引文覆盖"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

doc = Path("docs/法哲学_国家_大纲_概念链演绎链.md").read_text(encoding="utf-8")
print("=== 小节结构 ===")
for s in re.findall(r"^## (.+)$", doc, re.M):
    print(" ", s)

# 引文覆盖统计（含附录）
q_secs = set()
for line in doc.splitlines():
    if "*" in line and "§" in line:
        m = re.findall(r"§\s*(\d+)", line)
        if m:
            q_secs.add(int(m[0]))
q_secs = {s for s in q_secs if 257 <= s <= 360}
print(f"\n含德文引文的 §：{len(q_secs)}/104 = {len(q_secs)/104*100:.0f}%（目标 ≥70%）")
missing = [s for s in range(257, 361) if s not in q_secs]
print(f"未覆盖：{missing}")
print(f"总行数：{doc.count(chr(10))}")
