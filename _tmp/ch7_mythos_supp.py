# -*- coding: utf-8 -*-
"""ch7 悲剧环节补讨论补充：希腊神话=诸神在人间演绎的戏剧 + 欧赫梅尔式广采 + 谢林对照（本地原文）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CH7 = Path("notes_pheno/ch7.json")
d = json.loads(CH7.read_text(encoding="utf-8"))

SUPP = {
    "date": "2026-08-29",
    "title": "希腊神话=诸神在人间演绎的戏剧 + 欧赫梅尔式广采 + 谢林「颠倒的欧赫梅尔主义」",
    "content": (
        "**①命题（用户）**：希腊神话=诸神在人间演绎的一系列戏剧——不是故事集/文献，是行动：诸神（实体/普遍）在人间（特殊性）"
        "演绎（展开）=概念的判断环节；「一系列」=推论连续——「实体即主体」的叙事版。这正对应艺术宗教的本质：共同体把诸神做进作品"
        "（演绎=内容与形式的合一）。\n"
        "**②欧赫梅尔式广采（Euhemerismus——本地无原文，经谢林本地原文转述）**：欧赫梅尔（Euemeros）：神话=被神化的历史事件"
        "（神话是真实历史的传说化）——**被谢林反转**。\n"
        "**③谢林《神话哲学·历史批判导论》（本地原文）**：*Ein umgekehrter Euemerismus ist die richtige Ansicht. Nicht wie Euemeros lehrte, "
        "enthält die Mythologie die Begebenheiten der ältesten Geschichte, sondern umgekehrt die Mythologie im Entstehen, also eigentlich der Prozeß, "
        "durch den sie entsteht – dieser ist der wahre und einzige Inhalt jener ältesten Geschichte*——**不是神话=历史事件，而是神话的生成过程"
        "（意识的内在运动）=真正的历史内容**——史前时代=*innern Vorgängen und Bewegungen des Bewußtseins*（伴随神话体系生成的意识内在过程与运动）。"
        "**神话=意识自我运动产生的宗教**（*natürlich sich erzeugende Religion*——自然的、必然过程中产生的、因此是*unfreie, ungeistige* 的宗教）。\n"
        "**④谢林的历史观（直接支撑命题）**：*Homer ist von solcher Größe, daß keine spätere Zeit ihm Ähnliches hervorzubringen imstande war, "
        "dagegen würde auch eine Sophokleische Tragödie im homerischen Zeitalter eine Unmöglichkeit gewesen sein*——**荷马时代不可能有索福克勒斯式悲剧**"
        "——神话（荷马）与悲剧（索福克勒斯）是性质不同时代原则的产物——*Der mythologische Prozeß erreicht im hellenischen Bewußtsein sein Ende "
        "und die letzte Krisis*（神话过程在希腊意识中达到终点与最后危机）；*Dies ist der tragische Zug, der durch das ganze Heidentum geht*"
        "（这是贯穿整个异教的悲剧性特征）——**悲剧=神话过程的危机形态**（神话中的神人关系成为必然的、同时又要求更高的扬弃）。\n"
        "**⑤交叉对比（谢林×黑格尔×命题）**：都拒绝「神话=历史记录」（欧赫梅尔——谢林明确反转；黑格尔：神话=精神自我直观；命题：神话=演绎非档案）；"
        "都把神话当作意识/精神的运动过程（谢林=意识史；黑格尔=精神自我直观；命题=演绎/展开）。差异：谢林=神话的意识史定位（潜能阶次——人类学/历史），"
        "黑格尔=精神自我直观（逻辑/系统），命题=神话的戏剧形式（审美）。互补点：**悲剧=神话过程的危机（谢林）× 悲剧=行动即罪/两种正当伦理（黑格尔 ch7）"
        "——同一现象的神话学定位与结构分析**。\n"
        "**⑥引擎判读**：诸神（概念/实体）在人间（判断/特殊性）演绎（展开/推论）——悲剧=判断的冲突（神话的危机）→通向天启（推论/和解）——"
        "与 ch7 演绎链（史诗叙述→悲剧行动→喜剧解构→天启和解）完全吻合——命题=艺术宗教阶段的本质表述。"
    ),
}

target = None
for g in d["gestalten"]:
    for b in g["bewegung"]:
        if b[0].startswith("B.艺术宗教·悲剧：更高的语言"):
            target = b
            break
    if target:
        break

if target:
    supps = target[4] if len(target) > 4 else []
    if not any("希腊神话=诸神在人间演绎" in s.get("title", "") for s in supps):
        supps.append(SUPP)
        if len(target) > 4:
            target[4] = supps
        else:
            target.append(supps)
        CH7.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        json.loads(CH7.read_text(encoding="utf-8"))
        print("ch7 悲剧环节已补讨论补充（命题+欧赫梅尔广采+谢林对照）")
    else:
        print("已存在")
else:
    print("未找到悲剧环节")
