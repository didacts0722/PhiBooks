# -*- coding: utf-8 -*-
"""
观点库校验：编号唯一、互参存在、双向一致（lit.refs ↔ base.applies）。
作为重建/验证链的一部分（verify_ch123.py 会调用）。
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VP = Path(__file__).resolve().parent / "viewpoints"


def main():
    base = json.loads((VP / "base.json").read_text(encoding="utf-8"))
    lit = json.loads((VP / "lit.json").read_text(encoding="utf-8"))
    base_ids = [v["id"] for v in base["items"]]
    lit_ids = [v["id"] for v in lit["items"]]
    ok = True

    def fail(msg):
        nonlocal ok
        ok = False
        print("  [FAIL]", msg)

    # 编号唯一
    if len(set(base_ids)) != len(base_ids):
        fail(f"base 编号重复: {[i for i in set(base_ids) if base_ids.count(i) > 1]}")
    if len(set(lit_ids)) != len(lit_ids):
        fail(f"lit 编号重复: {[i for i in set(lit_ids) if lit_ids.count(i) > 1]}")

    # 互参存在性
    for v in base["items"]:
        for r in v.get("applies", []):
            if r not in lit_ids:
                fail(f"{v['id']}.applies 引用不存在的 {r}")
    for v in lit["items"]:
        for r in v.get("refs", []):
            if r not in base_ids:
                fail(f"{v['id']}.refs 引用不存在的 {r}")

    # 双向一致：lit.refs 中的 V# 应在其 applies 中回指（反向：base.applies 中的 T# 应在其 refs 中）
    base_by_id = {v["id"]: v for v in base["items"]}
    lit_by_id = {v["id"]: v for v in lit["items"]}
    for v in lit["items"]:
        for r in v.get("refs", []):
            if r in base_by_id and v["id"] not in base_by_id[r].get("applies", []):
                fail(f"{v['id']}.refs={r}，但 {r}.applies 未回指 {v['id']}")
    for v in base["items"]:
        for r in v.get("applies", []):
            if r in lit_by_id and v["id"] not in lit_by_id[r].get("refs", []):
                fail(f"{v['id']}.applies={r}，但 {r}.refs 未回指 {v['id']}")

    print(f"观点库校验：{'PASS' if ok else 'FAIL'}（base {len(base_ids)} 条 / lit {len(lit_ids)} 条）")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
