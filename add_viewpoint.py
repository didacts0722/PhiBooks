# -*- coding: utf-8 -*-
"""
观点登记工具：讨论后把新观点入库（自动编号 + 互参校验 + 文档同步）。

用法：
  # 基础观点（普遍适用）
  python add_viewpoint.py --type base --text "观点内容" --source "2026-08-26" [--boundary "边界"] [--refs "T-P1,V3"]
  # 文献特有观点
  python add_viewpoint.py --type lit --lit 现象学 --section "第4章" --text "观点" --anchor "〔p.140〕" --refs "V1,V4" [--note "第4章"]
  # 哲学家独立库（如谢林）
  python add_viewpoint.py --type phil --phil schelling --stage "早期·同一哲学" --work "作品名" --text "观点" [--note "备注"] [--refs "S1,V20"]
  # 提升：文献观点跨文本成立 → 提升为基础观点
  python add_viewpoint.py --promote T-P9 --source "2026-08-26" [--text "高度概括版"]

说明：
- 编号自动分配（base→V{max+1}；lit→T-{文献前缀}{max+1}；phil→S{max+1}）。
- --refs 引用的 V#/T#/S# 必须已存在（自动校验）。
- 入库后自动运行 views_sync.py 同步 Markdown 文档。
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
VP = ROOT / "viewpoints"

LIT_PREFIX = {"现象学": "P", "小逻辑": "L", "中庸": "Z", "精神现象学": "P", "逻辑学": "L"}


def load(name):
    return json.loads((VP / name).read_text(encoding="utf-8"))


def save(name, data):
    (VP / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def next_id(existing, prefix):
    nums = []
    for eid in existing:
        try:
            nums.append(int(eid[len(prefix):]))
        except (ValueError, IndexError):
            pass
    return f"{prefix}{max(nums) + 1 if nums else 1}"


def validate_refs(refs, base_ids, lit_ids, phil_ids=None):
    bad = []
    for r in refs:
        if r.startswith("V") and r not in base_ids:
            bad.append(r)
        elif r.startswith("T-") and r not in lit_ids:
            bad.append(r)
        elif phil_ids is not None and r not in phil_ids and not r.startswith(("V", "T-")):
            bad.append(r)
    return bad


def main():
    ap = argparse.ArgumentParser(description="观点登记工具")
    ap.add_argument("--type", choices=["base", "lit", "phil"])
    ap.add_argument("--promote", help="提升指定 T-# 为基础观点")
    ap.add_argument("--text", help="观点内容")
    ap.add_argument("--source", help="来源（日期/讨论标识）")
    ap.add_argument("--boundary", default="", help="边界（base）")
    ap.add_argument("--refs", default="", help="互参，逗号分隔（V#/T#/S#）")
    ap.add_argument("--lit", default="", help="文献名（lit）")
    ap.add_argument("--section", default="", help="章节/主题（lit）")
    ap.add_argument("--anchor", default="", help="原文锚点（lit）")
    ap.add_argument("--note", default="—", help="笔记位置/备注")
    ap.add_argument("--prefix", default="", help="文献编号前缀，默认按文献名推断")
    ap.add_argument("--phil", default="", help="哲学家库名（phil，如 schelling）")
    ap.add_argument("--stage", default="", help="哲学家阶段（phil 必填：早期/中期/后期…）")
    ap.add_argument("--work", default="", help="哲学家作品（phil）")
    args = ap.parse_args()

    base = load("base.json")
    lit = load("lit.json")
    base_ids = {v["id"] for v in base["items"]}
    lit_ids = {v["id"] for v in lit["items"]}
    phil = None
    phil_ids = set()
    if args.type == "phil" or (args.refs and any(r.startswith("S") and r[1:].isdigit() for r in args.refs.split(","))):
        pname = args.phil or "schelling"
        ppath = VP / f"{pname}.json"
        if not ppath.exists():
            print(f"哲学家库不存在：{pname}.json（先建 viewpoints/{pname}.json）")
            sys.exit(1)
        phil = load(f"{pname}.json")
        phil_ids = {v["id"] for v in phil["items"]}
    refs = [r.strip() for r in args.refs.split(",") if r.strip()]

    # ---- 提升模式 ----
    if args.promote:
        target = next((v for v in lit["items"] if v["id"] == args.promote), None)
        if not target:
            print(f"未找到 {args.promote}")
            sys.exit(1)
        text = args.text or target["text"]
        new_v = {"id": next_id(base_ids, "V"), "text": text,
                 "source": args.source or target.get("source", ""),
                 "boundary": args.boundary or "（由 T-# 提升，待校准边界）",
                 "applies": [target["id"]]}
        base["items"].append(new_v)
        base_ids.add(new_v["id"])
        target["refs"].append(new_v["id"])  # 回指
        print(f"提升：{target['id']} → {new_v['id']}（{target['lit']}·{target['section']}）")
        save("base.json", base)
        save("lit.json", lit)
        subprocess.run([sys.executable, "views_sync.py"])
        sys.exit(0)

    if not args.type or not args.text:
        ap.print_help()
        sys.exit(1)
    if args.type == "base" and not args.source:
        print("基础观点必须提供 --source（来源/日期）")
        sys.exit(1)

    # 互参校验
    bad = validate_refs(refs, base_ids, lit_ids, phil_ids)
    if bad:
        print(f"互参校验失败，以下编号不存在：{bad}")
        sys.exit(1)

    if args.type == "phil":
        if not args.stage:
            print("哲学家观点必须提供 --stage（阶段：早期/中期/后期…）——谢林分期纪律（S2）")
            sys.exit(1)
        pname = args.phil or "schelling"
        prefix = pname[:1].upper()  # schelling→S, platon→P
        new_id = next_id(phil_ids, prefix)
        entry = {"id": new_id, "stage": args.stage, "work": args.work or "（待定作品）",
                 "text": args.text, "source": args.source or "（待补来源）",
                 "note": args.note if args.note != "—" else "",
                 "refs": [r for r in refs if r.startswith((prefix, "V"))]}
        phil["items"].append(entry)
        save(f"{pname}.json", phil)
        print(f"已入库哲学家观点：{new_id}（{entry['stage']}·{entry['work']}）")
    elif args.type == "base":
        new_id = next_id(base_ids, "V")
        # refs：V# 互参进 refs 字段；T- 进 applies（应用于文献）
        entry = {"id": new_id, "text": args.text, "source": args.source,
                 "boundary": args.boundary or "（待补边界）",
                 "refs": [r for r in refs if r.startswith("V")],
                 "applies": [r for r in refs if r.startswith("T-")]}
        base["items"].append(entry)
        save("base.json", base)
        print(f"已入库基础观点：{new_id}" + (f"（互参：{', '.join(entry['refs'])}）" if entry["refs"] else ""))
    else:
        prefix = args.prefix or LIT_PREFIX.get(args.lit, args.lit[:1].upper())
        new_id = next_id(lit_ids, f"T-{prefix}")
        entry = {"id": new_id, "lit": args.lit or "（待定文献）", "section": args.section,
                 "text": args.text, "anchor": args.anchor, "refs": [r for r in refs if r.startswith("V")],
                 "note": args.note}
        if args.source:
            entry["source"] = args.source
        lit["items"].append(entry)
        save("lit.json", lit)
        print(f"已入库文献观点：{new_id}（{entry['lit']}·{entry['section']}）")
        # 回填基础观点的「应用于」
        for r in entry["refs"]:
            for v in base["items"]:
                if v["id"] == r and new_id not in v["applies"]:
                    v["applies"].append(new_id)
        save("base.json", base)

    subprocess.run([sys.executable, "views_sync.py"])
    print("文档已同步。")


if __name__ == "__main__":
    main()
