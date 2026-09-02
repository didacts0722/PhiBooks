# -*- coding: utf-8 -*-
"""沉淀关键解读：①V27 入库（为他存在的展开）②ch4 承认环节补讨论补充"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1) V27 入库
B = Path("viewpoints/base.json")
base = json.loads(B.read_text(encoding="utf-8"))
if not any(t.get("id") == "V27" for t in base["items"]):
    V27 = {
        "id": "V27",
        "text": ("为他存在的展开（Sein-für-Anderes 的对象必然社会化，2026-08-29 关键解读）：个别自我意识的为他存在，"
                 "最初是对**另一个个别自我意识**（ch4：*ein Selbstbewußtsein für ein Selbstbewußtsein*——我=我们，具体的「你」），"
                 "但必然展开——从「另一个个别自我意识」到「**另一个承载着社会结构的自我意识**」（大他者：法/绩效/制度/共同体——"
                 "制度化承认位置），再到伦理实体（国家/普遍承认，§331 被承认=第一权利）。"
                 "**为什么必须展开**：个别他者的承认是有限/偶然的（会消失/会变），停留=恶的无限（个别承认永远不够——斯多亚/怀疑/苦恼的循环）；"
                 "承认要稳固，他者必须承载结构——制度化=承认可重复/可检验（V23：绩效/履历/点赞替代了 ch4 的「另一个自我意识」）。"
                 "**拉康=ch4 在市民社会（ch6 精神）层面的投影**（无意识版本）：小 a=制度化匮乏剩余（绩效永远差一点），"
                 "大他者=承载结构的他者（但空洞——制度化承认缺席）；欲望（需要的体系）→匮乏（制度化）→大他者（符号位置）。"
                 "**V23=展开的完成形态（承认制度化），拉康=展开的病理形态（制度化承认缺席）——同一展开，两种结果**；"
                 "拉康「大他者不存在」=制度化承认位置无主体的精确解释（V23：承认被生产但承认缺席）"),
        "source": "2026-08-29 讨论（ch4→市民社会投影/拉康对接）",
        "boundary": "三阶段展开为结构判断非历史必然的严格证明；拉康对应为层面投影非文本等同；「大他者不存在」为拉康晚期命题",
        "refs": ["V23", "V26", "V21", "V24"],
        "applies": [],
    }
    base["items"].append(V27)
    base["updated"] = "2026-08-29"
    B.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
    print("V27 已入库")
else:
    print("V27 已存在")

# 2) ch4 承认环节补讨论补充
CH4 = Path("项目/现象学/notes/ch4.json")
d4 = json.loads(CH4.read_text(encoding="utf-8"))
SUPP = {
    "date": "2026-08-29",
    "title": "为他存在的展开：从「你」到「法/制度」（Sein-für-Anderes 的对象必然社会化）",
    "content": ("**核心命题（V27）**：个别自我意识的为他存在（Sein-für-Anderes），最初是对**另一个个别自我意识**（*ein Selbstbewußtsein "
                "für ein Selbstbewußtsein*——我=我们，具体的「你」），但必然展开：从「另一个个别自我意识」→「**另一个承载着社会结构的自我意识**」"
                "（大他者：法/绩效/制度/共同体——制度化承认位置）→伦理实体（国家/普遍承认）。\n"
                "**为什么必须展开**：个别他者的承认是有限/偶然的（会消失/会变）——停留=恶的无限（个别承认永远不够——斯多亚/怀疑/苦恼的循环）；"
                "承认要稳固，他者必须承载结构（§192：*die Allgemeinheit als Anerkanntsein*——承认=需要成为社会需要的中介——承认的普遍化）。\n"
                "**拉康对照**：拉康的无意识=ch4 在市民社会（ch6 精神）层面的投影——小 a=制度化匮乏剩余（绩效永远差一点），"
                "大他者=承载结构的他者（但空洞——制度化承认缺席）；「大他者不存在」=制度化承认位置无主体的精确解释（V23：承认被生产但承认缺席）。\n"
                "**V23=展开的完成形态（承认制度化），拉康=展开的病理形态（制度化承认缺席）——同一展开，两种结果**。\n"
                "**引擎判读**：为他存在的展开=判断环节的普遍化——他者从特殊（个别）升为普遍（承载结构）——ch4→ch6/市民社会的必然过渡"
                "（引擎在个体层→社会层的重演）——个别自我意识想要稳固的承认，就必须把自己投入一个承载结构的他者。")
}
target = None
for g in d4["gestalten"]:
    for b in g["bewegung"]:
        if b[0] == "我＝我们（承认的概念）":
            target = b
            break
    if target:
        break
if target:
    supps = target[4] if len(target) > 4 else []
    if not any("为他存在的展开" in s.get("title", "") for s in supps):
        supps.append(SUPP)
        if len(target) > 4:
            target[4] = supps
        else:
            target.append(supps)
        CH4.write_text(json.dumps(d4, ensure_ascii=False, indent=1), encoding="utf-8")
        json.loads(CH4.read_text(encoding="utf-8"))
        print("ch4 承认环节已补讨论补充")
    else:
        print("已存在")
else:
    print("未找到承认环节")
