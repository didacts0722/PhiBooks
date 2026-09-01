# -*- coding: utf-8 -*-
"""检查正文区内嵌 § 号标记（段首加粗 § NNN）与 A._Das_Innere_Staatsrecht 的正文位置"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")


def decode(data: bytes) -> str:
    return data.decode("iso-8859-1", errors="replace")


def find_end(txt: str) -> int:
    marks = [txt.find("zenoPLBookTextMore"), txt.find("zenoTRNavBottom")]
    marks = [i for i in marks if i > 0]
    return min(marks) if marks else len(txt)


# 1) a._fürstliche 正文段首是否嵌 §
txt = decode((OUT / "a._Die_fürstliche_Gewalt.html").read_bytes())
end = find_end(txt)
body = txt[:end]
bold_secs = re.findall(r"<b[^>]*>\s*§\s*(\d+)", body)
print("a._fürstliche 正文区 <b>§N</b> 出现:", bold_secs[:15])
# 段落开头文本（前 5 个 p）
paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)
print("前 5 段开头（纯文本）:")
for p in paras[:5]:
    t = re.sub(r"<[^>]+>", " ", p)
    t = re.sub(r"\s+", " ", t).strip()
    print("   ", t[:90])

# 2) A._Das_Innere_Staatsrecht：正文区是否含 §260 文本
txt2 = decode((OUT / "A._Das_Innere_Staatsrecht.html").read_bytes())
end2 = find_end(txt2)
body2 = txt2[:end2]
for probe in ["konkreten Freiheit", "§ 260", "Hegel", "Staatsrecht"]:
    print(f"A._Das_Innere_Staatsrecht 含 '{probe}':", probe in body2)
# 找正文区起点标记
for mark in ["zenoCOMain", "zenoPL", "Innere Staatsrecht"]:
    i = txt2.find(mark)
    print(f"  '{mark}' at {i}")
