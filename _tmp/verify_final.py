# -*- coding: utf-8 -*-
"""最终验证：贱民块内容/引文高亮/TOC 顺序/术语"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")

# 4.12 贱民块：引文段（mark.cited）
i = html.find('id="ch4-s12"')
seg = html[i:i + 2000]
m = re.search(r'<span class="pnum">(§\d+)</span>\s*<mark class="cited">([^<]{0,80})', seg)
print("4.12 贱民块引文段:", m.group(1) if m else "?", "|", (m.group(2) + "…") if m else "")
print("  块内是否含 §244 Pöbel 段:", "Pöbels hervor" in seg or "Erzeugung des Pöbels" in seg)

# TOC 第三编小节（顺序）
i = html.find('法哲学 · 第三编')
seg = html[html.find('<ul>', html.find('id="ch4"')):]
toc_items = re.findall(r'<li><a href="#ch4-s(\d+)">([^<]+)</a>', seg[:4000])
print("\nTOC 第三编小节顺序:")
for s, t in toc_items:
    print(f"  4.{s} {t}")

# 术语条数
print("\n术语标记数:", html.count("gterm"))
print("文件大小:", len(html), "| 章节:", html.count('class="chap"'))
