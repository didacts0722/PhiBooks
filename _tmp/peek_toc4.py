# -*- coding: utf-8 -*-
"""打印 TOC 第四编原始片段"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
i = html.find('href="#ch4"')
seg = html[i:i + 4500]
print(seg)
