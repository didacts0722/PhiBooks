# -*- coding: utf-8 -*-
"""
术语主表校验：viewpoints/glossary/<哲学家>.json
- 键唯一、术语非空、译法非空
- 跨作品冲突：同一德文词在多个作品里译法不一致 → 报告（规范性检查）
- 重复术语（拼写变体）提示
用法：python validate_glossary.py [哲学家名]，默认全部
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
DIR = ROOT / "viewpoints" / "glossary"


def check(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    terms = data.get("terms", [])
    errors = 0
    keys = Counter(t.get("term", "").lower() for t in terms)
    for k, c in keys.items():
        if c > 1:
            print(f"  ✗ 重复术语键：{k} ×{c}")
            errors += 1
    # 跨作品译法冲突：同一 key 在不同作品 zh 不同
    by_key = {}
    for t in terms:
        k = t.get("term", "").lower()
        if not t.get("term") or not t.get("zh"):
            print(f"  ✗ 术语或译法为空：{t}")
            errors += 1
            continue
        by_key.setdefault(k, {})[tuple(sorted(t.get("works", [])))] = t["zh"]
    for k, ws in by_key.items():
        zh_set = set(ws.values())
        if len(zh_set) > 1:
            print(f"  ✗ 跨作品译法冲突：{k} → {ws}")
            errors += 1
    n = len(terms)
    print(f"[{data.get('philosopher', path.stem)}] {n} 条术语"
          f"{'，全部通过' if errors == 0 else f'，{errors} 处问题'}")
    return errors


def main():
    files = list(DIR.glob("*.json"))
    if not files:
        print("无术语主表")
        return
    total = 0
    for f in sorted(files):
        total += check(f)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
