# -*- coding: utf-8 -*-
"""从 HTML 提取法哲学（ch1-ch4）标记的术语（主表已有，需补 works=法哲学）+ 首次标记"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")

# 提取所有 gt 术语条：<span class="gt"><i>TERM</i>[<sup...>§</sup>] <b>ZH</b></span>
terms = []
for m in re.finditer(r'<span class="gt"><i>([^<]+)</i>(<sup class="gt-first"[^>]*>§</sup>)?\s*<b>([^<]+)</b></span>', html):
    terms.append((m.group(1), bool(m.group(2)), m.group(3)))

# 法哲学部分（从 ch1 section 开始到结尾）——全文件都是法哲学（含导言/抽象法/道德/伦理）
firsts = {t for t, f, _ in terms if f}
print(f"总术语标记：{len(terms)} 条，首次出现：{len(firsts)} 个")

# 输出首次出现的术语（法哲学全书首次）
print("\n=== 法哲学首次出现术语（107 个中前 60）===")
seen = []
for t, f, zh in terms:
    if f and t not in seen:
        seen.append(t)
for t in seen[:60]:
    print(" ", t)
print(f"...共 {len(seen)} 个首次术语")

# 保存全部术语（去重）
all_t = sorted({t for t, _, _ in terms})
Path("_tmp/recht_terms_all.txt").write_text("\n".join(all_t), encoding="utf-8")
print(f"\n全部术语 {len(all_t)} 个 -> _tmp/recht_terms_all.txt")
