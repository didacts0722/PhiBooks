# -*- coding: utf-8 -*-
"""验证生成的 HTML：小节标题/TOC/引文锚点/术语"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
print("--- 第三编（伦理）相关小节 ---")
for m in re.findall(r"<h3[^>]*>(.*?)</h3>", html):
    t = re.sub(r"<[^>]+>", "", m)
    if any(k in t for k in ("家庭", "市民", "需要", "司法", "警察", "同业", "贱民", "过渡")):
        print(" ", t)
print()
print("--- 4.8 市民社会小节正文渲染 ---")
i = html.find('id="ch4-s8"')
print(html[i:i + 1200] if i > 0 else "not found")
