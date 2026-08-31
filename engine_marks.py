# -*- coding: utf-8 -*-
"""在绝对否定性（die absolute Negativität）推动整体前进的关键处加「⚙️ 引擎标注」。
位置：ch3 无限性（引擎第一次点火）、ch4 欲望（从看到做的换挡）、ch5 事情本身（原文点名 p.300）、
ch6 启蒙（原文点名 p.404）、ch8 时间（终点自我认识）。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
D = "2026-08-26"

MARKS = [
    ("ch3.json", "内在差别与无限性", {
        "date": D,
        "title": "⚙️ die absolute Negativität：引擎第一次点火",
        "content": "**这里就是引擎本身第一次登场的地方。** 我们的引擎，其名就是 die absolute Negativität（绝对否定性）：它不是主观的否定动作，也不是对象的属性，而是让一切形态自行瓦解、又自行重建的那个力。知性在「内在差别」里完成的整个循环——做出差别、揭穿差别、收回差别——正是绝对否定性第一次完整做功：它推动知性从「看对象」转向「看我」。此后所有换挡（观察→实践→审核→伦理→教化→道德→宗教→绝对知识）都是同一个力在不同层级上的展开。**此处是推动整体前进的关键：没有这一次点火，就没有后面任何一次换挡。**"
    }),
    ("ch4.json", "自我意识即欲望", {
        "date": D,
        "title": "⚙️ die absolute Negativität：从「看」到「做」的换挡",
        "content": "绝对否定性在这里完成第一次形态升级：此前它只在知性的思想里区分与收回（ch3 无限性），现在它成为**生存行动**——欲望否定对象、消灭对象的独立性，以此确证自我。推动的力没有变，做功方式变了：从「过渡」（看）进入「反思」（做）。**此处是推动整体前进的关键**：否定性一旦进入行动，承认、主奴、劳动、斯多亚—怀疑—苦恼的整条第四章链条都从这里放出。"
    }),
    ("ch5.json", "C.个体性：精神动物的王国和欺骗；事情自身", {
        "date": D,
        "title": "⚙️ die absolute Negativität：原文点名（p.300）",
        "content": "黑格尔在这里逐字点名引擎：*es ist die absolute Negativität oder das Tun in diesem Gegensatze*（它就是这个对立中的绝对否定性或行动）——意识从它的作品退回自身，成为绝对否定性，作品作为「事情本身」被保留下来。审核理性的全部自欺（把各环节轮流当作事情本身来崇拜）正是绝对否定性在个别性层面的做功：**它推动理性从「办事情」走向「精神」**——此处是理性章通向第六章的机关。"
    }),
    ("ch6.json", "启蒙只能审判自己", {
        "date": D,
        "title": "⚙️ die absolute Negativität：原文点名（p.404）",
        "content": "黑格尔在这里再次逐字点名引擎：*ihr Wesen als die absolute Negativität ist dieses, das Anderssein an ihr selbst zu haben*（纯粹识见的本质作为绝对否定性，就是把他在性保持在自身之内）——启蒙批判信仰，却只能审判它自己之所是，因为它否定的内容，就是它收回自身的内容。**此处是推动整体前进的关键**：绝对否定性没有外在对象，它的斗争即自我实现——启蒙由此把「有用性」确立为真理，把世界推入绝对自由的恐怖，再从恐怖逼出道德。"
    }),
    ("ch8.json", "外在化的肯定意义①：时间＝概念之定在", {
        "date": D,
        "title": "⚙️ die absolute Negativität：终点处的自我认识",
        "content": "全书最后，引擎终于认识自己：*Die Zeit ist der Begriff selbst, der da ist*（时间就是存在着的概念本身）——时间不过是绝对否定性的定在形式，精神在时间中显现，直到它把握住纯粹概念、扬弃时间形式。整部现象学是绝对否定性在不同层级的展开（概念—判断—推论），到这里它把全部形态回忆（Er-Innerung）进自身，从形态的次第过渡到纯粹概念的自我展开。**此处是推动整体前进的关键**：不是终点前的最后一次换挡，而是引擎认出自己就是全部运动的根源。"
    }),
    # ── 尚待消解的环节：坏的无限性 / 片面的否定性 ──
    ("ch4.json", "欲望的满足即空虚", {
        "date": D,
        "title": "⚙️ die absolute Negativität：坏的无限——尚待消解的环节",
        "content": "欲望的循环（否定对象→对象消失→新的欲望）就是**坏的无限性（schlechte Unendlichkeit）**：否定不断重复，却永远收不回一个肯定的结果——绝对否定性在这里只显示了它的一半：**只会否定，不会重建**。这是绝对否定性扬弃自身过程中的一个**尚待消解的环节**：它要等另一个自我意识来打破循环（p.143「自我意识只能在另一个自我意识中得到满足」），把空转的否定变成真正的承认。"
    }),
    ("ch4.json", "怀疑主义", {
        "date": D,
        "title": "⚙️ die absolute Negativität：片面的否定性——尚待消解的环节",
        "content": "怀疑主义是**片面的否定性**：它把斯多葛的概念变成实在的否定行动，能破一切却不能立任何东西——「绝对的辩证不安」（absolute dialektische Unruhe）、「无意识的胡言乱语」（bewußtlose Faselei）。这正是绝对否定性扬弃自身过程中的一个**尚待消解的环节**：dialektisch 的解构力全开，spekulativ 的重建力缺席；它必须再被否定一次（苦恼意识把分裂内化），才能把否定收进自身。"
    }),
    ("ch5.json", "形态界定：理性宣称「我就是一切实在」", {
        "date": D,
        "title": "⚙️ die absolute Negativität：坏的无限（引子 p.184）——尚待消解的环节",
        "content": "引子部分，黑格尔点名批判主观观念论**「陷入了坏的、即感性的无限」**——德文原文（p.184）：*in die schlechte, nämlich in die sinnliche Unendlichkeit geraten ist*。空唯心主义摇摆于纯粹意识与感性经验之间，反复肯定又反复否认，永远到不了概念——这是绝对否定性扬弃自身过程中的一个**尚待消解的环节**：否定只在外围空转（坏的无限），还没有进入事情本身（好的无限＝内在差别，见 ch3 无限性环节）。"
    }),
    ("ch6.json", "消失的狂怒：只剩否定的行动", {
        "date": D,
        "title": "⚙️ die absolute Negativität：片面的否定性——尚待消解的环节",
        "content": "绝对自由的恐怖是**片面的否定性**的极致：绝对否定性在这里只剩纯粹的否定行动（Furie des Verschwindens），连死亡都被抽空意义（见菜头之喻）——解构烧尽了一切内容，重建却完全缺席。这是绝对否定性扬弃自身过程中的一个**尚待消解的环节**：它把自己否定到空，反而逼出下一步——精神从外部清除转回内心立法（道德世界观），spekulativ 的重建在道德与良心里重新出场。"
    }),
    # ── 关键概念：Bildung（双向塑造，从不显现的镜子）──
    ("ch4.json", "奴隶：恐惧与劳动", {
        "date": D,
        "title": "🔑 关键概念：Bildung——双向塑造的第一次出场",
        "content": "劳动即教化：*Die Arbeit hingegen ist gehemmte Begierde, aufgehaltenes Verschwinden, oder sie bildet*（劳动是被节制的欲望……它塑造/陶铸）。Bildung 在这里第一次出场，而且一出场就是**双向的**：奴隶**改造外物**（把物塑造成作品），同时这场改造**在他自己的意识里留下痕迹**——他通过塑造对象返回自身，第一次获得持久的自为存在。这痕迹是一面**从不显现的镜子**：它不在对象上、也不直接可见，却潜移默化地改变着思维本身——人怎么干活，就怎么想问题。"
    }),
    ("ch6.json", "教化：获得承认与现实的通道", {
        "date": D,
        "title": "🔑 关键概念：Bildung——从不显现的镜子",
        "content": "教化（Bildung）是本章的关键概念：**塑造是双向的**——一方面改造外物（在世界上留下作品，由此获得承认与现实的通道），另一方面这场改造同时在思维上留下痕迹：**你塑造世界的方式，反过来塑造你思考的方式**。这痕迹是一面**从不显现的镜子**：它从不作为对象出现，却潜移默化地规定着思维的结构——教化的深浅，就是这面镜子被打磨的程度。按引擎表述：对外改造是判断（否定并塑造对象），对内留痕是推论的沉淀（概念在主体中成形），两者互为条件——这就是「有多少教化，就有多少现实与权力」的深层含义。"
    }),
]


def main():
    by_file = {}
    for fname, title, mark in MARKS:
        by_file.setdefault(fname, []).append((title, mark))
    for fname, items in by_file.items():
        p = ROOT / "notes_pheno" / fname
        data = json.loads(p.read_text(encoding="utf-8"))
        n = 0
        for title, mark in items:
            hit = False
            for g in data["gestalten"]:
                for b in g["bewegung"]:
                    if b[0] == title:
                        if len(b) < 5 or b[4] is None:
                            while len(b) < 5:
                                b.append(None)
                            b[4] = []
                        b[4] = [s for s in b[4] if s.get("title") != mark["title"]]
                        b[4].append(mark)
                        hit = True
                        n += 1
                        break
                if hit:
                    break
            if not hit:
                raise SystemExit(f"未找到环节：{fname} / {title}")
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                     encoding="utf-8", newline="\n")
        print(f"{fname} 引擎标注 {n} 处")
    print("完成。")


if __name__ == "__main__":
    main()
