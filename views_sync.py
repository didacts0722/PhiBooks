# -*- coding: utf-8 -*-
"""
观点库同步：viewpoints/base.json + lit.json → docs/基础观点库.md + docs/文献观点库.md
JSON 是唯一权威源，Markdown 为可读视图（由本脚本生成，勿手改）。
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
VP = ROOT / "viewpoints"
DOCS = ROOT / "docs"


def load(name):
    return json.loads((VP / name).read_text(encoding="utf-8"))


def render_base(data) -> str:
    lines = [
        "# 基础观点库（模块②：超出特定文献的内容讨论）",
        "",
        "> **定位**：沉淀**超出任何特定文献具体性**的普遍观点（元工具、方法论、判定标准）。观点写在**相当高度**上，作为**生成笔记摘要的指示框架**：加工任何文献的阅读笔记时，以其相关观点为指示，不把文献特有的内容拔高为普遍观点、也不把普遍观点硬塞进不适用的文本（防串文）。",
        "> **权威源**：`viewpoints/base.json`（本 md 由 `views_sync.py` 生成，勿手改）。扩充：讨论后由助手调用 `add_viewpoint.py --type base` 登记。",
        f"> **更新**：{data.get('updated', '—')}",
        "",
        "---",
        "",
    ]
    for i, v in enumerate(data["items"], 1):
        lines += [
            f"### {v['id']}",
            f"- **观点**：{v['text']}",
            f"- **来源**：{v['source']}",
            f"- **边界**：{v['boundary']}",
            f"- **应用于**：{('、'.join(v['applies'])) if v['applies'] else '—'}",
            "",
        ]
    lines += [
        "## 使用规则（防串文 + 摘要指示）",
        "",
        "1. **防串文**：写任何文献的笔记时，内容必须能追溯到——①该文献在「文献观点库」的文本特有观点（T-#），或②本库的普遍观点（V#，显式标注编号）。追溯不到的观点不得进入笔记；某文献特有的观点不得移植到其他文献（除非在该文献中重新推导并登记）。",
        "2. **摘要指示**：生成笔记摘要时，以本库相关观点为指示框架——先定位适用的 V#，再据此组织该章节的诊断与要点；摘要不得超出指示所允许的边界。",
        "3. **登记**：本库观点一旦被某文献笔记引用，在「应用于」列补记文献观点编号；文献观点库新增观点时，在「关联基础观点」列指回本库。",
    ]
    return "\n".join(lines)


def render_lit(data) -> str:
    lines = [
        "# 文献观点库（模块③：针对特定文献的文本讨论登记）",
        "",
        "> **定位**：登记**每个文本特有**的观点（只适用于该文本、锚定其原文），与基础观点库互参。写笔记时：文本特有观点必须能在这里找到；普遍观点必须能追溯到基础观点库编号——**追溯不到的观点不得进入笔记**（防串文）。",
        "> **权威源**：`viewpoints/lit.json`（本 md 由 `views_sync.py` 生成，勿手改）。扩充：讨论或笔记加工中形成文本特有观点时，由助手调用 `add_viewpoint.py --type lit` 登记。",
        f"> **更新**：{data.get('updated', '—')}",
        "",
        "---",
        "",
    ]
    # 按文献分组
    groups = {}
    for v in data["items"]:
        groups.setdefault(v["lit"], []).append(v)
    for lit, items in groups.items():
        lines += [f"## {lit}", "", "| 编号 | 章节/主题 | 观点概要 | 原文锚点 | 关联基础观点 | 笔记位置 |", "|---|---|---|---|---|---|"]
        for v in items:
            lines.append(
                f"| {v['id']} | {v['section']} | {v['text']} | {v['anchor'] or '—'} | "
                f"{'、'.join(v['refs'])} | {v['note']} |")
        lines += ["", "---", ""]
    lines += [
        "## 使用规则",
        "",
        "1. **登记**：在对话或笔记加工中形成的、锚定某文本原文的观点，登记到对应文献分组；标注原文锚点（页码/§）与关联基础观点（V#）。",
        "2. **防串文**：A 文献的 T-# 不得用于 B 文献的笔记；若某观点确实跨文本成立，先提升为基础观点（V#，高度概括）再引用。",
        "3. **摘要指示**：生成某文献笔记摘要时，先查本库该文献的 T-# 列表 + 基础观点库的适用 V#，两者共同构成摘要的框架。",
    ]
    return "\n".join(lines)


def render_phil(data) -> str:
    name = data.get("philosopher", "哲学家")
    lines = [
        f"# {name}观点库（哲学家独立库）",
        "",
        f"> **定位**：按哲学家独立登记的{name}观点库（与黑格尔库 base/lit 分开）。",
        f"> **权威源**：`viewpoints/` 下对应 json（本 md 由 `views_sync.py` 生成，勿手改）。",
        f"> **更新**：{data.get('updated', '—')}",
        "",
        "---",
        "",
    ]
    discipline = data.get("discipline", "")
    if discipline:
        lines.insert(4, f"> **⚠️ 纪律**：{discipline}")
        lines.insert(5, "")
    for v in data["items"]:
        lines += [
            f"### {v['id']}",
            f"- **阶段/作品**：{v.get('stage', '—')} · {v.get('work', '—')}",
            f"- **观点**：{v['text']}",
            f"- **来源**：{v['source']}",
            f"- **关联**：{('、'.join(v['refs'])) if v.get('refs') else '—'}",
            f"- **备注**：{v.get('note', '—')}",
            "",
        ]
    return "\n".join(lines)


PHIL_FILES = {
    "schelling": ("谢林观点库.md", render_phil),
    "platon": ("柏拉图观点库.md", render_phil),
}


def main():
    (DOCS / "基础观点库.md").write_text(render_base(load("base.json")), encoding="utf-8")
    (DOCS / "文献观点库.md").write_text(render_lit(load("lit.json")), encoding="utf-8")
    synced = ["docs/基础观点库.md", "docs/文献观点库.md"]
    for key, (mdname, renderer) in PHIL_FILES.items():
        p = VP / f"{key}.json"
        if p.exists():
            (DOCS / mdname).write_text(renderer(load(f"{key}.json")), encoding="utf-8")
            synced.append(f"docs/{mdname}")
    print("已同步：" + "、".join(synced))


if __name__ == "__main__":
    main()
