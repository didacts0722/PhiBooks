# -*- coding: utf-8 -*-
"""打印 TOC 第三编附近原始 HTML"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
i = html.find('href="#ch4"')
print(html[i - 100:i + 2500])
