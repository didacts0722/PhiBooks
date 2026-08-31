# -*- coding: utf-8 -*-
"""验证注释版 HTML：标签配平 + 结构计数 + 观点库互参校验"""
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

txt = Path("笔记/精神现象学_注释版.html").read_text(encoding="utf-8")
VOID = {"hr", "br", "img", "meta", "link", "input", "wbr"}


class Chk(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errs = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errs.append(f"extra </{tag}>")
        elif self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errs.append(f"mismatch </{tag}> vs <{self.stack[-1]}>")


c = Chk()
c.feed(txt)
print("标签配平:", "PASS" if not c.errs and not c.stack else f"FAIL {c.errs[:5]} {c.stack[-10:]}")
print("原文段落数:", len(re.findall(r'class="op"', txt)))
print("引文链接数:", len(re.findall(r'class="cite" href="#c\d', txt)))
print("引文未命中标记:", len(re.findall(r"cite miss|q miss", txt)))
print("章节数:", len(re.findall(r'<section class="gestalt"', txt)))
print("文件大小:", len(txt.encode("utf-8")), "字节")

# 观点库互参校验（与 HTML 校验并列）
r = subprocess.run([sys.executable, "validate_viewpoints.py"])
