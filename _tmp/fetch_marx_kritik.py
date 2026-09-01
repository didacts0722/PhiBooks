# -*- coding: utf-8 -*-
"""抓取马克思《法哲学批判》§296-298 部分，确认 §297 的内容归属"""
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}
url = "http://web.archive.org/web/20060901001445/http://pedagogie.ac-toulouse.fr/philosophie/textes/marxzurkritik261313.htm"
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=60) as resp:
    data = resp.read()
txt = data.decode("latin-1", errors="replace")
if "§ 296" not in txt and "296" not in txt:
    txt = data.decode("utf-8", errors="replace")
print(f"大小 {len(txt)}B")
# 找 § 295-300 附近的文本
plain = re.sub(r"<[^>]+>", " ", txt)
plain = re.sub(r"\s+", " ", plain)
for s in range(295, 301):
    i = plain.find(f"§ {s}.")
    if i < 0:
        i = plain.find(f"§ {s} ")
    if i >= 0:
        print(f"\n--- §{s} 附近（{i}）---")
        print(plain[i:i + 220])
    else:
        print(f"\n--- §{s} 未找到")
