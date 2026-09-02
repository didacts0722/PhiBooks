# -*- coding: utf-8 -*-
"""抽查法哲学 HTML 完整性"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
print("四帝国出现:", "四帝国" in html)
groups = re.findall(r'<li class="toc-group">([^<]+)</li>', html)
print("TOC 分组:", groups)
print("块数(ch4):", len(re.findall(r'<div class="block" id="ch4-s', html)))
print("引文高亮:", html.count('mark class="cited"'))
print("术语条:", html.count('<span class="gt">'))
# 书签按钮
print("书签按钮:", html.count('bm-add'))
# 章节数
print("章节:", html.count('class="gestalt" id="ch'))
