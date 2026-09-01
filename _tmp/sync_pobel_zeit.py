# -*- coding: utf-8 -*-
"""同步「时代差异准确表述」到 notes_recht/sittlichkeit.json 贱民环节（马克思对接尾部）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
g = d["gestalten"][0]

# 贱民环节（§244）
b = next(x for x in g["bewegung"] if x[1] == "§244")
txt = b[3]

anchor = "马克思把「扬弃」读成「消灭」，黑格尔的「扬弃」=「纳入更高统一（国家）」。"
addition = ("\n**时代差异的准确表述（纠偏）**：黑格尔并没有把贫困当偶然——§243-244 明确结构性"
            "（*vermehrt sich die Anhäufung der Reichtümer ... auf der einen Seite, wie auf der andern Seite "
            "die Vereinzelung und Beschränktheit der besonderen Arbeit und damit die Abhängigkeit und Not "
            "der an diese Arbeit gebundenen Klasse*——财富积累与劳动阶级的依附、贫困**同时增长**；§244 "
            "*bringt die Erzeugung des Pöbels hervor*——市民社会在自己内部**产生**贱民）；§241 的「偶然」"
            "只是**个体致贫**层面（*zufällige ... Umstände Individuen zur Armut herunterbringen*——偶然因素把"
            "**个体**打入贫困），不是贱民存在的根据——**两个层次：个体致贫偶然（§241），贱民产生结构必然（§243-244）**。"
            "黑格尔在德国工业化之前（1821）**纯靠演绎**已推出结构性贫困。真实差异在两点：①**机制**——黑格尔只说"
            "「同时增长」（§243）没解释为什么；马克思的剩余价值/资本积累规律回答为什么——论据更扎实处在此；"
            "②**出路**——黑格尔=补救性方案（救济 §245/殖民 §246/同业公会 §253/国家扬弃）=结构性问题的非结构性解法；"
            "马克思=结构性出路（消灭私有制/革命）——黑格尔的经验样本只有英国早期工业贫困（§245 引英格兰），无大规模"
            "无产阶级化运动的直接经验。**继承点**：§243「财富积累与贫困同时增长」=马克思**无产阶级贫困化规律**的雏形；"
            "§198「劳动机械化到人可被机器取代」=**资本有机构成**的前身——**马克思不是从零发现结构，是把黑格尔的结构直觉"
            "机制化（剩余价值）+主体化（无产阶级）+政治化（革命）**。")
assert anchor in txt, "锚点未找到"
b[3] = txt.replace(anchor, anchor + addition)

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print("已同步，JSON 校验通过")
