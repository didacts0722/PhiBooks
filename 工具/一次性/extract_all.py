# -*- coding: utf-8 -*-
"""
全量提取：原文/<哲学家>/<作品>/ 下所有作品 → extracted/（复用 extract_zeno.process_book）。
- 跳过 extracted/ 目录本身
- 两个早期作品保留规范命名（phenomenologie / enzyklopaedie_logik），其余用目录名
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "原文"

SPECIAL = {
    "Phänomenologie_des_Geistes": "phenomenologie",
    "Enzyklopädie_Logik": "enzyklopaedie_logik",
}

from extract_zeno import process_book  # noqa: E402


def main():
    works = []
    for phil in sorted(p for p in RAW.iterdir() if p.is_dir()):
        for work in sorted(p for p in phil.iterdir() if p.is_dir() and p.name != "extracted"):
            htmls = list(work.glob("*.html"))
            if not htmls:
                continue
            works.append(work)
    print(f"待提取作品：{len(works)} 部")
    for work in works:
        out_name = SPECIAL.get(work.name, work.name)
        process_book(work, out_name)
    print(f"完成：{len(works)} 部作品全部提取。")


if __name__ == "__main__":
    main()
