# -*- coding: utf-8 -*-
"""检查 4.8 市民社会块与 4.12 贱民块的笔记渲染"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")

for sid in ("8", "12"):
    i = html.find(f'<div class="block" id="ch4-s{sid}">')
    j = html.find('<div class="block" id="ch4-s', i + 10)
    seg = html[i:j if j > 0 else i + 6000]
    # 笔记右栏
    note = re.search(r'<div class="b-note">(.*?)</div>\s*</div>', seg, re.S)
    txt = re.sub(r"<[^>]+>", "", note.group(1)) if note else seg[:300]
    txt = re.sub(r"\s+", " ", txt)
    print(f"=== 4.{sid} 笔记（前 600 字）===")
    print(txt[:600])
    print()
