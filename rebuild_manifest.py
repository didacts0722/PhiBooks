# -*- coding: utf-8 -*-
"""
文献清单重建：按磁盘实况统计（页数 = 目录内 *.html 数，含脚注页），
补上清单缺失的早期目录（如 Enzyklopädie_Logik），保留原作品显示名。
输出：原文/文献清单.json（供 gen_文献清单.py 生成 docs/文献清单.md）
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "原文"
MANIFEST = RAW / "文献清单.json"


def main():
    old = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_dir = {}
    for w in old.get("works", []):
        by_dir.setdefault(w.get("dir"), w)

    entries = []
    for phil in sorted(p for p in RAW.iterdir() if p.is_dir()):
        for work in sorted(p for p in phil.iterdir() if p.is_dir() and p.name != "extracted"):
            htmls = list(work.glob("*.html"))
            if not htmls:
                continue
            rel = str(work.relative_to(ROOT))
            prev = by_dir.get(rel)
            entries.append({
                "phil": phil.name,
                "work": (prev or {}).get("work", work.name),
                "dir": rel,
                "pages": len(htmls),
                "status": "ok",
            })
    manifest = {"updated": old.get("updated", ""), "source": old.get("source", "zeno.org"),
                "works": entries}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(w["pages"] for w in entries)
    print(f"已重建 文献清单.json：{len(entries)} 部 / {total} 页（按磁盘实况）")


if __name__ == "__main__":
    main()
