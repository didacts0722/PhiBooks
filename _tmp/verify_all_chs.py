# -*- coding: utf-8 -*-
"""验证四章段落流 § 顺序 + 标题"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")

m = re.search(r"<h1>(.*?)</h1>", html)
print("H1:", re.sub(r"<[^>]+>", "", m.group(1)))
m = re.search(r"<title>(.*?)</title>", html)
print("TITLE:", m.group(1))

for ch in range(1, 5):
    secs = re.findall(rf'<p class="op" id="c{ch}-p\d+"><span class="pnum">(§\d+|Vor)</span>', html)
    vals = [int(s[1:]) for s in secs if s != "Vor"]
    bad = sum(1 for a, b in zip(vals, vals[1:]) if b < a)
    print(f"c{ch}: {len(secs)} 段，§ 流逆序 {bad}（Vor 段 {secs.count('Vor')}）")
