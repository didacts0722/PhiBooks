# -*- coding: utf-8 -*-
"""沉淀 V28：欲望的再生产机制三层显现（个体层小a/自我意识层大他者欲望/市民社会层机制揭示）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1) V28 入库
B = Path("viewpoints/base.json")
base = json.loads(B.read_text(encoding="utf-8"))
if not any(t.get("id") == "V28" for t in base["items"]):
    V28 = {
        "id": "V28",
        "text": ("欲望的再生产机制的三层显现（2026-08-29 关键解读，V27 的机制学深化）：精神分析下手的对象=**欲望的再生产机制**"
                 "——这个机制**不由个体掌握**（无意识=不被主体掌握的结构），但它的真身不在个体心理："
                 "①**个体层**：机制显现为**对象小 a**（匮乏的对象化——个体只感到「永远差一点」——神秘）；"
                 "②**自我意识层**：「欲望是大他者的欲望」——但发生学机制仍不可理解（被驱动而不知机制——**拉康停在此：揭示现象不揭示机制**）；"
                 "③**市民社会层**：机制被**完全揭示**——个体欲望=被市民社会的运作/生产机制所结构化、支配（V23：承认被制度化生产——"
                 "需要的体系 §199 欲望经劳动相互承认/绩效/履历/点赞——制度化匮乏=小 a 的机制版）。"
                 "**精确化**：拉康的「无意识」=市民社会欲望再生产机制的**个体内化**（个体不知道被什么驱动）；"
                 "精神分析=判断环节的现象学（小 a/大他者欲望的展开与失败），V23=判断环节的机制学（承认被制度化生产）；"
                 "**机制的揭示在市民社会层，但揭示≠解决**——市民社会本身=尚待消解环节（贱民/承认失败）——机制揭示=判断的自我认识，"
                 "重建（推论）在市民社会之外（国家/伦理——承认的完成）"),
        "source": "2026-08-29 讨论（精神分析对象=欲望再生产机制/三层显现）",
        "boundary": "三层为结构判读非拉康原文本等同；「机制在市民社会层揭示」为我们的层面对接（V23）；临床不展开",
        "refs": ["V27", "V23", "V21", "V24"],
        "applies": [],
    }
    base["items"].append(V28)
    base["updated"] = "2026-08-29"
    B.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
    print("V28 已入库")
else:
    print("V28 已存在")

# 2) 精神分析整理补充（八、对项目的意义）
G = Path("docs/精神分析_引擎深度整理.md")
doc = G.read_text(encoding="utf-8")
anchor = "**V23=展开的完成形态（承认制度化），拉康=展开的病理形态（制度化承认缺席）——同一展开，两种结果**。"
add = (anchor + "\n"
       "6. **欲望的再生产机制三层显现（V28，2026-08-29）**：精神分析下手的对象=欲望的再生产机制（不由个体掌握）——"
       "个体层显现为小 a（神秘：永远差一点）/自我意识层=「欲望是大他者的欲望」（机制不可理解——拉康停在此）/"
       "**市民社会层=机制完全揭示**（个体欲望被生产结构结构化、支配——V23 承认被制度化生产）——"
       "拉康的「无意识」=市民社会欲望再生产机制的个体内化；精神分析=判断环节的现象学，V23=判断环节的机制学；"
       "机制的揭示在市民社会层，但揭示≠解决（市民社会=尚待消解环节——重建在推论/国家）。")
if anchor in doc and "欲望的再生产机制三层显现" not in doc:
    doc = doc.replace(anchor, add)
    G.write_text(doc, encoding="utf-8")
    print("精神分析整理已补 V28")
else:
    print("精神分析整理锚点未找到或已存在")

# 3) 法哲学需要的体系环节补充（V28 对接）
R = Path("项目/法哲学/notes/sittlichkeit.json")
d = json.loads(R.read_text(encoding="utf-8"))
target = None
for g in d["gestalten"]:
    for b in g["bewegung"]:
        if b[1] == "§199":  # 需要的体系环节
            target = b
            break
    if target:
        break
if target:
    supps = target[4] if len(target) > 4 else []
    if not any("欲望的再生产机制" in s.get("title", "") for s in supps):
        supps.append({
            "date": "2026-08-29",
            "title": "需要的体系=欲望的再生产机制（V28 对接）",
            "content": ("**V28 对接**：需要的体系（§199 主观利己→他人贡献）正是**欲望的再生产机制**的市民社会形态——"
                        "个体欲望（需要）经劳动被结构化（§189-208），绩效/交换/司法=制度化承认生产（V23）——"
                        "「我总觉得缺什么」（小 a）的机制真身在此：**个体欲望被市民社会的生产结构结构化、支配**。"
                        "个体层只见小 a（永远差一点——神秘）；自我意识层只见「欲望是大他者的欲望」（被驱动而不知机制——拉康停此）；"
                        "市民社会层=机制完全揭示（V23 承认被制度化生产）。精神分析=判断环节的现象学，V23=判断环节的机制学——"
                        "机制揭示在市民社会层，但揭示≠解决（市民社会=尚待消解——贱民/承认失败——重建在推论/国家）。")
        })
        if len(target) > 4:
            target[4] = supps
        else:
            target.append(supps)
        R.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        json.loads(R.read_text(encoding="utf-8"))
        print("法哲学需要的体系环节已补 V28 对接")
    else:
        print("法哲学环节已存在")
else:
    print("未找到需要的体系环节")
