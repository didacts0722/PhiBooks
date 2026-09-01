# -*- coding: utf-8 -*-
"""验证 TOC 第四编分组 + 小节标题"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
i = html.find('href="#ch4"')
seg = html[html.find("<ul>", i):html.find("<ul>", i) + 9000]
# 分组与条目
for m in re.finditer(r'<li class="toc-group">([^<]+)</li>|<li><a href="#ch4-s(\d+)">([^<]+)</a>', seg):
    if m.group(1):
        print(f"  [组] {m.group(1)}")
    else:
        print(f"   4.{m.group(2)} {m.group(3)[:40]}")
