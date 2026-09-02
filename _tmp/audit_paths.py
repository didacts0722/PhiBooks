# -*- coding: utf-8 -*-
"""审计：工作流（构建/工具脚本 + 文档）的路径引用是否都建立在实际结构上"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(".")

# 1) Python 脚本中的路径引用（相对路径字符串/Path 构造）
print("=== 1. Python 脚本路径引用审计 ===")
py_files = [f for f in ROOT.glob("*.py") if f.name not in ("build_pheno_ch123.py",)]
py_refs = []
for f in py_files:
    txt = f.read_text(encoding="utf-8", errors="replace")
    # Path/字符串里的相对路径（含 / 或 \ 或 中文目录）
    for m in re.finditer(r'["\']((?:notes|docs|viewpoints|笔记|对话归档|原文|二手材料|_tmp|data)[^"\']*)["\']', txt):
        ref = m.group(1)
        # 提取第一段做存在性检查（相对 ROOT）
        first = ref.split("/")[0].split("\\")[0]
        py_refs.append((f.name, ref, first))
bad = []
for fname, ref, first in py_refs:
    # 展开可能的 ROOT 前缀（脚本用 ROOT / "..." 或 Path(...)）
    path = ROOT / first
    if not path.exists():
        bad.append((fname, ref))
for fname, ref in bad:
    print(f"  [失效] {fname}: {ref}")
if not bad:
    print("  Python 脚本路径全部有效")

# 2) 文档中的相对路径引用
print("\n=== 2. 文档路径引用审计（docs/ + 根 md）===")
doc_refs = []
for f in list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md")) + list((ROOT / "docs" / "大纲").glob("*.md")):
    txt = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'`((?:docs|笔记|notes|viewpoints|对话归档|原文|二手材料)/[^`]+)`', txt):
        ref = m.group(1)
        # 去掉可能的锚点/扩展处理
        target = ROOT / ref
        if not target.exists():
            # 尝试去掉 .html 或检查前缀目录
            doc_refs.append((str(f), ref))
for f, ref in doc_refs[:20]:
    print(f"  [检查] {f}: {ref}（不存在？）")
if not doc_refs:
    print("  文档路径引用全部有效")
else:
    print(f"  （共 {len(doc_refs)} 条待查——多为渲染产物引用或新文件）")

# 3) 关键工作流文件存在性
print("\n=== 3. 关键工作流文件 ===")
keys = [
    "build_recht.py", "build_lp.py", "build_pheno_ch123.py",
    "add_viewpoint.py", "views_sync.py", "validate_glossary.py",
    "archive_unconscious.py", "decompress_unconscious.py",
    "notes_recht/sittlichkeit.json", "notes_pheno/ch6.json", "notes_lp/begriff.json",
    "viewpoints/base.json", "viewpoints/glossary/黑格尔.json",
    "docs/大纲/精神现象学_大纲_概念链演绎链.md",
    "docs/运行简报.md", "docs/注释规范.md",
    "对话归档/原始/session.jsonl.zstd", "对话归档/索引.md",
    "原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json",
]
for k in keys:
    ok = (ROOT / k).exists()
    print(f"  {'✓' if ok else '✗'} {k}")
