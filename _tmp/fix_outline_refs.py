# -*- coding: utf-8 -*-
"""更新引用路径：docs/XXX_大纲 → docs/大纲/XXX_大纲"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FILES = [
    "docs/三书关系_引擎三介质.md",
    "docs/运行简报.md",
    "docs/法哲学_导言_血肉展开.md",
    "docs/项目全流程.md",
    "docs/对话档案.md",
    "docs/注释规范.md",
]
NAMES = [
    "精神现象学_大纲_概念链演绎链.md",
    "法哲学_国家_大纲_概念链演绎链.md",
    "法哲学_伦理_大纲_家庭市民社会.md",
    "法哲学_导言_大纲.md",
    "法哲学_抽象法_大纲.md",
    "法哲学_道德_大纲.md",
    "法哲学原理_大纲.md",
    "黑格尔哲学引擎_大纲.md",
    "小逻辑_大纲.md",
]
for fn in FILES:
    f = Path(fn)
    txt = f.read_text(encoding="utf-8")
    n = 0
    for name in NAMES:
        old = f"docs/{name}"
        new = f"docs/大纲/{name}"
        c = txt.count(old)
        if c:
            txt = txt.replace(old, new)
            n += c
    if n:
        f.write_text(txt, encoding="utf-8")
        print(f"{fn}: 更新 {n} 处")
    else:
        print(f"{fn}: 无引用")
