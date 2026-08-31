# -*- coding: utf-8 -*-
"""打印 ch1-8 各环节：[标题] p.德文页码 德文引文前 70 字 + 已有补充数"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent


def main():
    for n in range(1, 9):
        p = ROOT / "notes_pheno" / f"ch{n}.json"
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        print(f"\n===== ch{n} {data.get('title','')} [{data.get('pages','')}] =====")
        for g in data["gestalten"]:
            for b in g["bewegung"]:
                title, page = b[0], b[1]
                quote = (b[2] or "")[:70].replace("\n", " ")
                nsupp = len(b[4]) if len(b) > 4 and isinstance(b[4], list) else 0
                print(f"  [{title}] p.{page} | {quote}… | supps={nsupp}")


if __name__ == "__main__":
    main()
