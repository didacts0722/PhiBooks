# -*- coding: utf-8 -*-
"""补充：①现象学大纲 ch7 神话命题+谢林对照 ②ch7 天启共同体环节补谢林「神话→启示→哲学宗教」"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1) 大纲补充
G = Path("docs/大纲/精神现象学_大纲_概念链演绎链.md")
doc = G.read_text(encoding="utf-8")
anchor = "   自然宗教→艺术宗教→天启宗教（精神在表象中直观自身）"
if anchor in doc and "诸神在人间演绎" not in doc:
    doc = doc.replace(
        anchor,
        anchor + "\n"
        "  （用户命题+谢林对照：希腊神话=诸神在人间演绎的一系列戏剧——神话=行动非故事集（「实体即主体」的叙事版）；"
        "谢林《神话哲学》「颠倒的欧赫梅尔主义」：不是神话=历史事件，是神话的生成=意识的内在过程——神话=自然产生的宗教；"
        "悲剧=神话过程的危机（*der tragische Zug, der durch das ganze Heidentum geht*——荷马时代不可能有索福克勒斯式悲剧）；"
        "谢林「神话→启示→哲学宗教」=黑格尔「艺术宗教→天启→绝对知识」同构）")
    G.write_text(doc, encoding="utf-8")
    print("大纲已补神话命题+谢林对照")
else:
    print("大纲锚点未找到或已存在")

# 2) ch7 天启共同体未完成环节补谢林对照
CH7 = Path("notes_pheno/ch7.json")
d = json.loads(CH7.read_text(encoding="utf-8"))
SUPP = {
    "date": "2026-08-29",
    "title": "谢林「神话→启示→哲学宗教」=黑格尔「艺术宗教→天启→绝对知识」（对照）",
    "content": (
        "**谢林《神话哲学·历史批判导论》（本地原文）**：*Die philosophische Religion ist demnach durch die geoffenbarte geschichtlich vermittelt*"
        "——**哲学宗教通过启示历史地中介**——神话宗教（必然/不自由/非精神的：*unfreie, ungeistige Religion*）→启示（*das Bewußtsein gegen sie in "
        "Freiheit setzt*——把意识从神话中解放）→自由的宗教（*nur als philosophische sich vollkommen verwirklichen kann*——哲学宗教）。"
        "**与黑格尔 ch7→ch8 同构**：谢林的「神话→启示→哲学」=黑格尔的「艺术宗教→天启→绝对知识」——神话/艺术宗教=必然过程（表象/不自由），"
        "启示/天启=解放的中介（表象中的和解），哲学/绝对知识=自由（概念把握）。"
        "**差异**：谢林=神话的意识史/人类学定位（神话=人类最古老的宗教形态，先于启示——*die erste Form, in der Religion überhaupt existiert*）；"
        "黑格尔=精神自我直观（逻辑/系统定位）。共同点：都拒绝把神话当历史记录（欧赫梅尔），都把神话看作必然过程的产物、且必然被更高的形态扬弃。"
        "**引擎判读**：谢林的「神话→启示→哲学」=设定（必然/不自由）→展开（解放中介）→重建（自由/概念）——与引擎三段同构——"
        "ch7 共同体的未完成（表象中的和解）正是谢林说的「启示之后、哲学之前」的中介环节。"
    ),
}
target = None
for g in d["gestalten"]:
    for b in g["bewegung"]:
        if b[0].startswith("C.天启宗教·共同体的未完成"):
            target = b
            break
    if target:
        break
if target:
    supps = target[4] if len(target) > 4 else []
    if not any("谢林「神话→启示→哲学宗教」" in s.get("title", "") for s in supps):
        supps.append(SUPP)
        if len(target) > 4:
            target[4] = supps
        else:
            target.append(supps)
        CH7.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        json.loads(CH7.read_text(encoding="utf-8"))
        print("ch7 共同体未完成环节已补谢林对照")
    else:
        print("已存在")
else:
    print("未找到共同体环节")
