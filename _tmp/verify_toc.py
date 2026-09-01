# -*- coding: utf-8 -*-
"""检查 TOC 第三编小节"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
i = html.find('href="#ch4"')
print("href#ch4 at:", i)
j = html.find("<ul>", i)
seg = html[j:j + 4000]
for s, t in re.findall(r'<li><a href="#ch4-s(\d+)">([^<]+)</a>', seg):
    print(f"  4.{s} {t}")
