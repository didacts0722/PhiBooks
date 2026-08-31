# -*- coding: utf-8 -*-
"""普查原文全部 <p> 的 class 分布（定位正文段落 class 白名单缺口）— 单遍扫描版"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "原文"

P_RE = re.compile(r'<p\b([^>]*)>', re.S)


def main():
    total = Counter()       # 全部 <p>
    body_total = Counter()  # zenoCOMain 之后的 <p>
    n_files = 0
    n_body = 0
    for f in RAW.rglob("*.html"):
        n_files += 1
        txt = f.read_bytes().decode("iso-8859-1", errors="replace")
        for attrs in P_RE.findall(txt):
            m = re.search(r'class="([^"]*)"', attrs)
            cls = m.group(1) if m else "(无class)"
            total[cls] += 1
        i = txt.find('class="zenoCOMain"')
        if i >= 0:
            n_body += 1
            seg = txt[i:i + 200000]
            for attrs in P_RE.findall(seg):
                m = re.search(r'class="([^"]*)"', attrs)
                cls = m.group(1) if m else "(无class)"
                body_total[cls] += 1
    print(f"文件数：{n_files}，含 zenoCOMain 页面：{n_body}")
    print("\n全部 <p> class（前 25）：")
    for cls, cnt in total.most_common(25):
        print(f"  {cls!r}: {cnt}")
    print("\n正文区（zenoCOMain 之后）<p> class（前 25）：")
    for cls, cnt in body_total.most_common(25):
        print(f"  {cls!r}: {cnt}")


if __name__ == "__main__":
    main()
