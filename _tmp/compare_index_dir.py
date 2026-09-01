# -*- coding: utf-8 -*-
"""对比 index JSON 收录的页面 vs extracted 目录实际 JSON 文件"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EX = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted")
idx = json.loads((EX / "Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))

idx_files = [p.get("file") for p in idx]
dir_files = sorted(f.name for f in EX.glob("*.json") if "index" not in f.name)

print(f"index 收录: {len(idx_files)} 页 | extracted 目录: {len(dir_files)} 个 JSON")
missing_in_idx = [f for f in dir_files if f not in idx_files]
extra_in_idx = [f for f in idx_files if f not in dir_files]
print(f"\n目录有但 index 缺（{len(missing_in_idx)}）：")
for f in missing_in_idx:
    print("  ", f)
print(f"\nindex 有但目录缺（{len(extra_in_idx)}）：")
for f in extra_in_idx:
    print("  ", f)
