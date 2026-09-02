# -*- coding: utf-8 -*-
"""解包 epub：按 spine 顺序提取文本 + 目录结构（健壮属性解析）"""
import re
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EPUB = ROOT / "二手材料" / "庄振华_精神现象学义解_上下卷.epub"
OUT_DIR = ROOT / "二手材料" / "extracted"
OUT_DIR.mkdir(exist_ok=True)

with zipfile.ZipFile(EPUB) as z:
    names = z.namelist()
    opf = z.read("content.opf").decode("utf-8", errors="replace")

    # 解析 manifest：提取每个 item 的 id 与 href（属性顺序不定）
    idmap = {}
    for m in re.finditer(r"<item\b[^>]*>", opf):
        tag = m.group(0)
        i = re.search(r'\bid="([^"]+)"', tag)
        h = re.search(r'\bhref="([^"]+)"', tag)
        if i and h:
            idmap[i.group(1)] = h.group(1)
    spine = re.findall(r'<itemref\b[^>]*\bidref="([^"]+)"', opf)
    print(f"manifest items: {len(idmap)}，spine 文档: {len(spine)}")

    # 目录：尝试多种 nav/toc 源
    nav_text = ""
    for n in names:
        if "nav" in n.lower() or n.endswith(".ncx"):
            try:
                nav_text += z.read(n).decode("utf-8", errors="replace")
            except Exception:
                pass
    if nav_text:
        print("===== 目录（nav/ncx） =====")
        # ncx 格式
        for m in re.finditer(r"<text>(.*?)</text>", nav_text, re.S):
            label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if label:
                print(f"  {label[:60]}")
        # nav xhtml 格式
        if "navPoint" not in nav_text:
            for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', nav_text, re.S):
                label = re.sub(r"<[^>]+>", "", m.group(2)).strip()
                if label:
                    print(f"  {label[:60]:62s} {m.group(1)[:40]}")

    # 按 spine 顺序提取正文
    all_text = []
    doc_info = []
    for rid in spine:
        href = idmap.get(rid)
        if not href:
            continue
        fname = href if href in names else f"text/{href}" if f"text/{href}" in names else None
        if not fname:
            continue
        try:
            raw = z.read(fname).decode("utf-8", errors="replace")
        except KeyError:
            continue
        title_m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S)
        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else fname
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
        body = re.sub(r"<[^>]+>", "", body)
        body = re.sub(r"&nbsp;?", " ", body)
        body = re.sub(r"&#\d+;", " ", body)
        body = re.sub(r"[ \t]+", " ", body)
        body = re.sub(r"\n\s*\n+", "\n", body).strip()
        if len(body) < 30 and "part" in fname:
            pass  # 可能是空壳页
        doc_info.append((fname, title, len(body)))
        all_text.append(f"===== {title} [{fname}] =====\n{body}")

    full = "\n\n".join(all_text)
    (OUT_DIR / "庄振华_义解_全文.txt").write_text(full, encoding="utf-8")
    print(f"\n已提取 {len(all_text)} 个文档 -> 庄振华_义解_全文.txt（{len(full)} 字符）")
    print("\n各文档标题与长度（前 60）：")
    for fname, title, ln in doc_info[:60]:
        print(f"  {title[:55]:57s} {ln:6d}")
