# -*- coding: utf-8 -*-
"""最终验证 v2：贱民块/同业公会块内容 + TOC"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")

# 所有块定义位置
blocks = [(m.start(), m.group(1)) for m in re.finditer(r'<div class="block" id="ch4-s(\d+)"', html)]
print("伦理编块数:", len(blocks))

for pos, sid in blocks:
    seg = html[pos:pos + 900]
    pm = re.search(r'<span class="pnum">(§\d+|Vor)</span>', seg)
    cited = re.search(r'<mark class="cited">([^<]{0,70})', seg)
    # 找到该块内的 h4 小节标题
    h4 = re.search(r'<h4[^>]*><span class="secno">小节 4\.\d+</span>\s*([^<]{0,40})', seg)
    title = h4.group(1) if h4 else "?"
    print(f"  4.{sid}: 首段 {pm.group(1) if pm else '?'} | 引文: {cited.group(1) + '…' if cited else '-'} | {title}")

# TOC 第三编（章节 4）小节顺序
i_ch4 = html.find('<a href="#ch4">')
seg = html[i_ch4:i_ch4 + 3500]
items = re.findall(r'<li><a href="#ch4-s(\d+)">([^<]+)</a>', seg)
print("\nTOC 第三编小节顺序:")
for s, t in items:
    print(f"  4.{s} {t}")

# 贱民块是否含 §241-246
pos, _ = next((p, s) for p, s in blocks if s == "12")
seg12 = html[pos:html.find('<div class="block" id="ch4-s13"')]
print("\n4.12 贱民块含 §241 引文:", "zur Armut herunterbringen" in seg12)
print("4.12 贱民块含 §244 Pöbel:", "Erzeugung des Pöbels" in seg12)
