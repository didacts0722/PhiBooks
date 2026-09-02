# -*- coding: utf-8 -*-
"""解包 epub：列出结构 + 提取 XHTML 文本"""
import json
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EPUB = ROOT / "二手材料" / "庄振华_精神现象学义解_上下卷.epub"
OUT = ROOT / "二手材料" / "extracted"

with zipfile.ZipFile(EPUB) as z:
    names = z.namelist()
    print(f"epub 内文件数: {len(names)}")
    # 找 OPF 清单
    opf = next((n for n in names if n.endswith(".opf")), None)
    print("OPF:", opf)
    if opf:
        opf_text = z.read(opf).decode("utf-8", errors="replace")
        # 找 manifest items
        items = re.findall(r'<item[^>]*href="([^"]+)"', opf_text)
        print(f"manifest items: {len(items)}")
        # 找 spine 顺序
        spine = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf_text)
        idrefs = re.findall(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf_text)
        idmap = dict(idrefs)
        print(f"spine: {len(spine)} 个文档")
        # 保存 spine 顺序文档清单
        ordered = [idmap.get(r, r) for r in spine]
        (OUT.parent / "spine_order.txt").write_text("\n".join(ordered), encoding="utf-8")
        print("前 20 个 spine 文档：")
        for o in ordered[:20]:
            print("  ", o)
    # 统计 xhtml 文件
    xhtmls = [n for n in names if n.endswith((".xhtml", ".html", ".htm"))]
    print(f"xhtml 文件: {len(xhtmls)}")
