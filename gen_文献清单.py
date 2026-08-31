# -*- coding: utf-8 -*-
"""
文献清单生成：原文/文献清单.json → docs/文献清单.md（统一管理视图）
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "原文"


def main():
    manifest = json.loads((RAW / "文献清单.json").read_text(encoding="utf-8"))
    works = manifest.get("works", [])
    lines = [
        "# 文献清单（模块①：原始资料下载 · 统一管理）",
        "",
        f"> 来源：zeno.org（{manifest.get('source', '')}）· 更新：{manifest.get('updated', '')}",
        "> 原始资料按哲学家分类存放于 `原文/<哲学家>/<作品>/`，提取文本在 `<作品>/extracted/`。",
        "> 本清单由 `docs/gen_文献清单.py` 从 `原文/文献清单.json` 生成。",
        "",
    ]
    by_phil = {}
    for w in works:
        by_phil.setdefault(w["phil"], []).append(w)
    total_pages = 0
    for phil in sorted(by_phil):
        items = by_phil[phil]
        lines += [f"## {phil}", "", "| 作品 | 页数 | 状态 | 位置 |", "|---|---|---|---|"]
        for w in sorted(items, key=lambda x: x["work"]):
            total_pages += w.get("pages", 0)
            lines.append(f"| {w['work']} | {w.get('pages', 0)} | {w.get('status', '')} | `{w.get('dir', '')}` |")
        lines += [""]
    lines.append(f"**合计**：{len(works)} 部作品，约 {total_pages} 页。")
    (ROOT / "docs" / "文献清单.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 docs/文献清单.md（{len(works)} 部作品）")


if __name__ == "__main__":
    main()
