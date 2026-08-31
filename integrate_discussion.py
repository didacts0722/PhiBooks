# -*- coding: utf-8 -*-
"""
讨论整合工具：把新的文本讨论追加为指定环节的「📌 讨论补充」。

用法：
  python integrate_discussion.py <章号> <关键词> "<日期>|<主题>|<要点...>"
  python integrate_discussion.py 5 哈姆雷特 "2026-08-26|哈姆雷特的延宕|延宕是概念不敢进入判断……"

说明：
- 关键词用于在 notes_pheno/ch<章号>.json 的环节标题中定位（首个包含者）。
- 内容格式：用 | 分隔 日期/主题/要点；要点可含 **加粗**。
- 追加后自动重建 HTML 并跑引文对拍校验。
- --dry-run：只显示将要追加的内容，不写入。
"""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NOTES = Path(__file__).resolve().parent / "notes_pheno"


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if len(args) != 3:
        print("用法：python integrate_discussion.py <章号> <关键词> \"<日期>|<主题>|<要点...>\" [--dry-run]")
        sys.exit(1)
    ch, keyword, content = args
    try:
        ch = int(ch)
    except ValueError:
        print("章号必须是数字")
        sys.exit(1)
    parts = content.split("|", 2)
    if len(parts) != 3:
        print("内容须为 <日期>|<主题>|<要点> 三段，用 | 分隔")
        sys.exit(1)
    date, title, body = [p.strip() for p in parts]

    path = NOTES / f"ch{ch}.json"
    if not path.exists():
        print(f"不存在：{path}")
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    g = data["gestalten"][0]
    for it in g["bewegung"]:
        if keyword in it[0]:
            supps = it[4] if len(it) > 4 else []
            supps.append({"date": date, "title": title, "content": body})
            while len(it) < 5:
                it.append([])
            it[4] = supps
            print(f"定位：第{ch}章 环节「{it[0]}」（{it[1]}）")
            print(f"追加补充：{date} | {title}")
            if dry:
                print("[dry-run] 未写入。")
                sys.exit(0)
            json.dump(data, path.open("w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"已写入 {path.name}，重建 HTML 并校验…")
            r = subprocess.run([sys.executable, "build_pheno_ch123.py"])
            sys.exit(r.returncode)
    print(f"第{ch}章未找到标题包含「{keyword}」的环节。可用标题：")
    for it in g["bewegung"]:
        print("  -", it[0])
    sys.exit(1)


if __name__ == "__main__":
    main()
