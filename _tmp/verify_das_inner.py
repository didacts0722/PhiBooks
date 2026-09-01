# -*- coding: utf-8 -*-
"""验证 Das_Innere_Staatsrecht.html 正文区提取 + 检查正文区是否有 § 锚点"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")
from extract_zeno import extract_page  # noqa: E402

OUT = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")

# 1) extract_page 提取
d = extract_page(OUT / "Das_Innere_Staatsrecht.html")
items = d["items"]
ps = [it for it in items if it["type"] == "p"]
hs = [it for it in items if it["type"] in ("h4", "h5")]
print(f"Das_Innere_Staatsrecht.html: items={len(items)}（h={len(hs)} p={len(ps)}）")
for it in items[:3]:
    print(f"   {it['type']}: {it['text'][:80]}")
print(f"   末段: {ps[-1]['text'][:80]}（p.{ps[-1].get('page')}）")

# 2) 正文区 § 锚点检查（name= 锚 / § 号段首）
txt = (OUT / "Das_Innere_Staatsrecht.html").read_bytes().decode("iso-8859-1", errors="replace")
marks = [txt.find("zenoPLBookTextMore"), txt.find("zenoTRNavBottom")]
marks = [i for i in marks if i > 0]
end = min(marks) if marks else len(txt)
body = txt[:end]
anchors = re.findall(r'<a\b[^>]*\bname="([^"]+)"', body)
print(f"\n正文区 <a name> 锚点（前 20）: {anchors[:20]}")
bold_sec = re.findall(r"<b[^>]*>\s*§\s*(\d+)", body)
print(f"正文区 <b>§N</b>: {bold_sec[:10]}")
para_heads = re.findall(r"<p[^>]*>(.{0,80}?)</p>", body, re.S)
print(f"正文区段落数: {len(para_heads)}")
for p in para_heads[:6]:
    t = re.sub(r"<[^>]+>", " ", p)
    print("   ", " ".join(t.split())[:85])
