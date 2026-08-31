# -*- coding: utf-8 -*-
"""导出指定章节的未引段清单（供子代理写阅读辅助）。
用法：python dump_uncited.py ch2 ch3 ch4
输出：_tmp/ch{N}_uncited.json = [{id, page, text}]（只含未被引用的段）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
TMP = ROOT / "_tmp"
TMP.mkdir(exist_ok=True)

import build_pheno_ch123 as b  # noqa: E402


def main():
    chs = [int(a[2:]) for a in sys.argv[1:]] or [2, 3, 4]
    for n in chs:
        if n not in b.available_chapters():
            print(f"ch{n} 不可用")
            continue
        pages = b.load_chapter(n)
        meta = b.load_notes(n)
        np_ = [(p["id"], b.norm(p["text"]).lower()) for p in pages]
        cited = set()
        for g in meta["gestalten"]:
            for b_ in g["bewegung"]:
                q = b.norm(b_[2]).lower()
                if not q:
                    continue
                for pid, txt in np_:
                    if q in txt:
                        cited.add(pid)
                        break
        uncited = [{"id": p["id"], "page": p.get("page"),
                    "text": b.norm(p["text"])} for p in pages if p["id"] not in cited]
        out = TMP / f"ch{n}_uncited.json"
        out.write_text(json.dumps(uncited, ensure_ascii=False, indent=1),
                       encoding="utf-8", newline="\n")
        print(f"ch{n}: 未引段 {len(uncited)} -> {out}")


if __name__ == "__main__":
    main()
