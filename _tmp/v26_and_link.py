# -*- coding: utf-8 -*-
"""入库 V26（爱=无条件承认尚且/宗教=无条件性的实体化）+ 现象学 ch7/ch8 关联补充 + 大纲补充"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1) V26 入库 base.json
B = Path("viewpoints/base.json")
base = json.loads(B.read_text(encoding="utf-8"))
ids = [t.get("id") for t in base["items"] if isinstance(t, dict) and t.get("id", "").startswith("V")]
vmax = max(int(i[1:]) for i in ids)
print(f"观点库当前最大 V 编号：V{vmax}")

V26 = {
    "id": "V26",
    "text": ("爱=无条件承认尚且（V24 应用）：理性/标准（观察理性，ch5 面相学式：从状态读价值）给不出无条件——"
             "无条件承认（她将会是，不因现状）超出理性论证，是对尚且在理性之外的承诺——爱有信仰成分。"
             "宗教=无条件性的实体化：社会运行法则的无条件层（伦理实体——家庭的爱/共同体的信任/道德的底层，无此层社会无法再生产）"
             "被体验、被实体化为神圣者——道成肉身=无条件承认的实体化（神降卑到人=承认人的尚且）；三位一体=爱的关系的实体化；"
             "「上帝是爱」=把爱实体化为神的本质。实体化是必然（无条件性太抽象须有可见形态，表象=概念的必经之路）但不是终点："
             "ch8 把神内在化（上帝死了=表象的自我扬弃）——无条件性的概念形式=相互承认（ch6 和解之词=绝对精神），不是神像——"
             "宗教=无条件性的表象，伦理/哲学=无条件性的概念（§270 同一内容两种形式）。"
             "判断框架纪律：标准（筛选）用于关系结构（会不会互相消耗），不用于价值评分（她值多少）——后者=观察理性，会杀死爱"),
    "source": "2026-08-29 讨论（爱/信仰/宗教链条）",
    "boundary": "「无条件」指承认结构（不因现状而给承认），非无边界（结构判断仍有效）；宗教=实体化的必然阶段非终点；临床不展开",
    "refs": ["V24", "V23", "V22", "V21"],
    "applies": [],
}
if not any(t.get("id") == "V26" for t in base["items"]):
    base["items"].append(V26)
    base["updated"] = "2026-08-29"
    B.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
    print("V26 已入库")
else:
    print("V26 已存在")

# 2) ch7 道成肉身环节 supps 追加
CH7 = Path("notes_pheno/ch7.json")
d7 = json.loads(CH7.read_text(encoding="utf-8"))
for g in d7["gestalten"]:
    for b in g["bewegung"]:
        if b[0].startswith("C.天启宗教·道成肉身"):
            supps = b[4] if len(b) > 4 else []
            if not any(s.get("title", "").startswith("道成肉身=无条件承认的实体化") for s in supps):
                supps.append({
                    "date": "2026-08-29",
                    "title": "道成肉身=无条件承认的实体化（V26）",
                    "content": ("**V26 应用**：道成肉身=无条件性的实体化——神降卑到人（*als ein wirklicher einzelner Mensch*）=无条件承认尚且的宗教表象："
                                "不因人的现状而给承认，正因人是人。这是社会运行法则的无条件层（伦理实体——家庭的爱/共同体的信任）被体验后被实体化为神圣者："
                                "无条件性太抽象须有可见形态（表象=概念的必经之路）。但实体化不是终点——ch8 把它去实体化，无条件性回到相互承认（ch6 和解之词）。"
                                "三位一体（父-子-灵）=爱的关系的实体化（自在-自为-自在自为）。")
                })
                if len(b) > 4:
                    b[4] = supps
                else:
                    b.append(supps)
                print("ch7 道成肉身环节已补 V26 补充")
        elif b[0].startswith("C.天启宗教·共同体的未完成"):
            supps = b[4] if len(b) > 4 else []
            if not any(s.get("title", "").startswith("表象中的和解=无条件性的实体化形态") for s in supps):
                supps.append({
                    "date": "2026-08-29",
                    "title": "表象中的和解=无条件性的实体化形态（V26）",
                    "content": ("**V26 应用**：天启宗教的「表象中的和解」=无条件性以实体形态（神圣事件）被拥有——共同体把和解当作外在发生的事件"
                                "（*es als ein Geschehen ... sich vorstellt*），即无条件承认被实体化为「神完成了的和解」。"
                                "这正是实体化的必然与局限：内容（和解）真实，形式（表象/事件）未升——去实体化（把「神完成的和解」还原为「人-人相互承认」）"
                                "正是 ch8 绝对知识的任务。")
                })
                if len(b) > 4:
                    b[4] = supps
                else:
                    b.append(supps)
                print("ch7 共同体未完成环节已补 V26 补充")
CH7.write_text(json.dumps(d7, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(CH7.read_text(encoding="utf-8"))

# 3) ch8 形态界定 supps 追加
CH8 = Path("notes_pheno/ch8.json")
d8 = json.loads(CH8.read_text(encoding="utf-8"))
for g in d8["gestalten"]:
    for b in g["bewegung"]:
        if b[0].startswith("形态界定") and len(b) > 3:
            supps = b[4] if len(b) > 4 else []
            if not any(s.get("title", "").startswith("去实体化=无条件性回到相互承认") for s in supps):
                supps.append({
                    "date": "2026-08-29",
                    "title": "去实体化=无条件性回到相互承认（V26）",
                    "content": ("**V26 应用**：ch8 的「扬弃表象形式」=无条件性的去实体化——把神像（道成肉身/三位一体/上帝死了的实体化表象）"
                                "还原为概念：无条件承认的最终形态不是神（实体），是相互承认（关系，ch6 和解之词）。"
                                "宗教=无条件性的表象，绝对知识=无条件性的概念——同一内容两种形式（§270）。"
                                "这与 ch7 诊断（内容已满、形式未升）闭环：实体化是为了被扬弃。")
                })
                if len(b) > 4:
                    b[4] = supps
                else:
                    b.append(supps)
                print("ch8 形态界定已补 V26 补充")
CH8.write_text(json.dumps(d8, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(CH8.read_text(encoding="utf-8"))

# 4) 现象学大纲补充一句（概念链 ch7 行）
G = Path("docs/大纲/精神现象学_大纲_概念链演绎链.md")
doc = G.read_text(encoding="utf-8")
anchor = "ch7 宗教 ＝ 推论①（表象式统一——回顾—扬弃模式）"
if anchor in doc and "无条件性的实体化" not in doc:
    doc = doc.replace(anchor, anchor + "\n  （V26：宗教=无条件性的实体化——道成肉身=无条件承认的表象；实体化非终点，ch8 去实体化回相互承认）")
    G.write_text(doc, encoding="utf-8")
    print("现象学大纲已补 V26 关联")
print("全部完成")
