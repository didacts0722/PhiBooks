# -*- coding: utf-8 -*-
"""验证修复后：c4 段落流 § 顺序 + 各小节块的段落区间"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")

# 段落流：p.op 中的 pnum（§ 号）
secs = re.findall(r'<p class="op" id="c4-p(\d+)"><span class="pnum">(§\d+|Vor)</span>', html)
nums = [(int(i), s) for i, s in secs]
ids = [n for n, _ in nums]
good = all(a + 1 == b for a, b in zip(ids, ids[1:]))
print(f"c4 段落数: {len(nums)}，id 连续: {good}")
# § 流是否递增（书序）
seq = [s for _, s in nums]
vals = [int(s[1:]) for s in seq if s != "Vor"]
bad = [(vals[i - 1], vals[i]) for i in range(1, len(vals)) if vals[i] < vals[i - 1]]
print(f"§ 流逆序对: {len(bad)}（应为 0）")
if bad[:5]:
    print("  前 5 个:", bad[:5])

# 各小节块的代表段：找 id="ch4-sN" 后的第一个 pnum
print()
print("--- 伦理编小节块（id → 首段 §） ---")
for m in re.finditer(r'id="ch4-s(\d+)"', html):
    seg = html[m.end():m.end() + 400]
    pm = re.search(r'<span class="pnum">(§\d+|Vor)</span>', seg)
    t = re.search(r'<h3[^>]*>(.*?)</h3>', seg)
    title = re.sub(r"<[^>]+>", "", t.group(1)) if t else "?"
    print(f"  4.{m.group(1)} {title} → 首段 {pm.group(1) if pm else '?'}")
