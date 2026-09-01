# -*- coding: utf-8 -*-
"""验证 §257-360 段落流：§260-329 是否完整连续存在"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
secs = re.findall(r'<p class="op" id="c4-p\d+"><span class="pnum">(§\d+)</span>', html)
vals = [int(s[1:]) for s in secs]

# §257-360 覆盖检查
missing = [n for n in range(257, 361) if n not in vals]
print(f"§257-360 覆盖：{360-257+1} 个 §，缺失 {len(missing)}：{missing}")

# §260-329 是否有段落
in_260_329 = [v for v in vals if 260 <= v <= 329]
print(f"§260-329 段落数：{len(in_260_329)}（应为 122）")

# 抽样：§260/272/275/298/321 各有多少段
for s in (260, 272, 275, 298, 321, 329):
    print(f"  §{s}: {vals.count(s)} 段")
