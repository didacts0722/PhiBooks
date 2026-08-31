# -*- coding: utf-8 -*-
"""
精神现象学 第1-3章 · 原文注释版（试点）
- 左栏：zeno.org 德文原文段落（带原书页码锚点）
- 右栏：引擎框架读书笔记（无「知—行」、无「正反合」）
- 引文：笔记内引用 → 锚点链接到原文段落
- 校验：逐条引文（页码 + 德文片段）与原文对拍
输出：精神现象学_第1-3章_注释版.html
"""
import html as _html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
EX = ROOT / "原文" / "黑格尔" / "Phänomenologie_des_Geistes" / "extracted"
OUT = ROOT / "笔记" / "精神现象学_注释版.html"

import brief_pheno  # noqa: E402  编者 Brief（全书前导言）

# 各章对应的原文页面（提取后的 JSON，按原书页码顺序）
CHAPTER_FILES = {
    0: ["Vorrede.json", "Einleitung.json"],
    1: ["I._Die_sinnliche_Gewißheit_oder_das_Diese_und_das_Meinen.json"],
    2: ["II._Die_Wahrnehmung_oder_das_Ding_und_die_Täuschung.json"],
    3: ["III._Kraft_und_Verstand_Erscheinung_und_übersinnliche_Welt.json"],
    4: ["IV._Die_Wahrheit_der_Gewißheit_seiner_selbst.json",
        "A._Selbständigkeit_und_Unselbständigkeit_des_Selbstbewußtseins_Herrschaft_und_Knechtschaft.json",
        "B._Freiheit_des_Selbstbewußtseins_Stoizismus_Skeptizismus_und_das_unglückliche_Bewußtsein.json"],
    5: ["V._Gewißheit_und_Wahrheit_der_Vernunft.json",
        "A._Beobachtende_Vernunft.json",
        "a._Beobachtung_der_Natur.json",
        "b._Die_Beobachtung_des_Selbstbewußtseins_in_seiner_Reinheit_und_seiner_Beziehung_auf_äußere_Wirklichkeit_logische_und_psychologische_Gesetze.json",
        "c._Beobachtung_der_Beziehung_des_Selbstbewußtseins_auf_seine_unmittelbare_Wirklichkeit_Physiognomik_und_Schädellehre.json",
        "B._Die_Verwirklichung_des_vernünftigen_Selbstbewußtseins_durch_sich_selbst.json",
        "a._Die_Lust_und_die_Notwendigkeit.json",
        "b._Das_Gesetz_des_Herzens_und_der_Wahnsinn_des_Eigendünkels.json",
        "c._Die_Tugend_und_der_Weltlauf.json",
        "C._Die_Individualität_welche_sich_an_und_für_sich_selbst_reell_ist.json",
        "a._Das_geistige_Tierreich_und_der_Betrug_oder_die_Sache_selbst.json",
        "b._Die_gesetzgebende_Vernunft.json",
        "c._Gesetzprüfende_Vernunft.json"],
    6: ["VI._Der_Geist.json",
        "A._Der_wahre_Geist._Die_Sittlichkeit.json",
        "a._Die_sittliche_Welt._Das_menschliche_und_göttliche_Gesetz_der_Mann_und_das_Weib.json",
        "b._Die_sittliche_Handlung._Das_menschliche_und_göttliche_Wissen_die_Schuld_und_das_Schicksal.json",
        "c._Der_Rechtszustand.json",
        "B._Der_sich_entfremdete_Geist._Die_Bildung.json",
        "I._Die_Welt_des_sich_entfremdeten_Geistes.json",
        "a._Die_Bildung_und_ihr_Reich_der_Wirklichkeit.json",
        "b._Der_Glaube_und_die_reine_Einsicht.json",
        "II._Die_Aufklärung.json",
        "a._Der_Kampf_der_Aufklärung_mit_dem_Aberglauben.json",
        "b._Die_Wahrheit_der_Aufklärung.json",
        "III._Die_absolute_Freiheit_und_der_Schrecken.json",
        "C._Der_seiner_selbst_gewisse_Geist._Die_Moralität.json",
        "a._Die_moralische_Weltanschauung.json",
        "b._Die_Verstellung.json",
        "c._Das_Gewissen._Die_schöne_Seele_das_Böse_und_seine_Verzeihung.json"],
    7: ["VII._Die_Religion.json",
        "A._Die_natürliche_Religion.json",
        "a._Das_Lichtwesen.json",
        "b._Die_Pflanze_und_das_Tier.json",
        "c._Der_Werkmeister.json",
        "B._Die_Kunstreligion.json",
        "a._Das_abstrakte_Kunstwerk.json",
        "b._Das_lebendige_Kunstwerk.json",
        "c._Das_geistige_Kunstwerk.json",
        "C._Die_offenbare_Religion.json"],
    8: ["VIII._Das_absolute_Wissen.json"],
}


def norm(s: str) -> str:
    s = re.sub(r"\*", "", s)
    s = _html.unescape(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def inline(s: str) -> str:
    """笔记文本：markdown 加粗 → strong；转义其余"""
    s = _html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def load_chapter(n: int) -> list:
    paras = []
    for fname in CHAPTER_FILES[n]:
        data = json.loads((EX / fname).read_text(encoding="utf-8"))
        paras.extend(it for it in data["items"] if it["type"] == "p")
    # 给段落分配稳定 id（章内序号）
    for i, p in enumerate(paras, 1):
        p["id"] = f"c{n}-p{i}"
    return paras


NOTES_DIR = ROOT / "notes_pheno"


def load_notes(n: int) -> dict:
    """笔记数据：优先 notes_pheno/ch{n}.json，缺失时回退内嵌 NOTES（1-3 章）"""
    p = NOTES_DIR / f"ch{n}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return NOTES[n]


# ------------------------------------------------------------------ 笔记
# 每章笔记：形态列表，每形态含 界定/运动/诊断/过渡 + 引文（page, 德文片段）
NOTES = {
    1: {
        "title": "第一章 感性确定性；这一个和意谓",
        "pages": "82–91",
        "mode": "过渡模式（存在论式）",
        "gestalten": [
            {
                "name": "感性确定性",
                "position": "意识的最初形态",
                "bestimmung": "意识最初的确信：**“我知道的最真实的东西，就是眼前这个直接存在的东西。”** 其真理只含三个要素——对象作为直接的“这一个”、自我作为直接的“意谓”（Meinen）、以及“现在/这里”作为时空索引。",
                "bewegung": [
                    ("直接接受性的宣称", "p.82", "Das Wissen, welches zuerst oder unmittelbar unser Gegenstand ist",
                     "意识以为能对对象完全“接受性”地直接把握，不改变其任何东西——它把自己当作最丰富、最真实的认知（“抽象而最贫乏的真理”：对象只是“是”）。“纯有”“纯我”“纯这一个”是它的全部。"),
                    ("“这一个”的困境", "p.83", "das Allgemeine ist also in der Tat das Wahre der sinnlichen Gewißheit",
                     "写下“现在是夜晚”，中午再看它已“变味”（schal）；指着“这里”说树，转身后它是房子。“现在/这里/这一个”一经说出就变成普遍性——感性确定性的真理被证明是共相。"),
                    ("语言比意谓更真", "p.85", "Die Sprache aber ist, wie wir sehen, das Wahrhaftere",
                     "“语言是更真的东西：在语言中我们直接反驳自己的意谓。” 凡是能说出的，已是普遍；“我们意谓的个别，永远无法说出”。"),
                    ("指认的证明", "p.88", "das Aufzeigen ist das Erfahren, daß Jetzt Allgemeines ist",
                     "当意识被要求“指认”这一个时，被指认的“现在”在指认的瞬间已经消逝——指认本身是一段运动，其结果是“许多现在的复合”（Vielheit von Jetzt）；指认经验到的正是：现在是普遍的。"),
                    ("神秘仪式的反证", "p.90", "in die alten Eleusinischen Mysterien der Ceres und des Bacchus",
                     "黑格尔把坚持“感性对象的绝对真理”者打发回厄琉息斯秘仪——吃面包、喝酒这些行动恰恰否定了感性事物的独立性：对直接性的真正“真理”，是行动对它的否定。"),
                ],
                "diagnose": "**引擎的第一转（过渡模式）**：概念＝意谓中的个别；判断＝说出/指认——而判断一旦发生就自我否定（个别消逝为普遍）；推论＝共相，即“以否定与中介为本质的纯有”。引擎在意识介质中烧掉的第一样东西是“直接性”，确立的第一条真理是“普遍性”。但这是知性的抽象普遍，还不是概念本身——引擎刚点火，转速极低。",
                "uebergang": "感性确定性死于自己的指认——它一开口就背叛了自己。意识被迫承认：真理不在直接的“个别”中，而在能被说出、被固定的“事物”及其“属性”中——进入知觉。",
            },
        ],
    },
    2: {
        "title": "第二章 知觉；事物和幻觉",
        "pages": "93–105",
        "mode": "过渡模式 · 反思雏形",
        "gestalten": [
            {
                "name": "知觉",
                "position": "意识以共相把握对象",
                "bestimmung": "知觉把对象当作**共相**：事物（Ding）——一个拥有多种属性的统一体。“直接的确定性没有认识它自己的真理……知觉则把对它存在着的东西认作普遍性的东西。”",
                "bewegung": [
                    ("事物＝许多属性的“也”", "p.93", "das Ding von vielen Eigenschaften",
                     "知觉的对象被规定为“具有许多属性的事物”：属性在“普遍媒介”中彼此穿透而不相接触（Auch）；物的统一性把属性收摄为一个“一”。"),
                    ("扬弃的双重意义", "p.94", "Das Aufheben stellt seine wahrhafte gedoppelte Bedeutung dar",
                     "“扬弃显示出它的双重意义：它同时是‘否定’与‘保存’。” 感性的个别被否定，但被保存为普遍的属性——知觉第一次在环节中同时做着否定与保存两件事。"),
                    ("“也”与“一”的矛盾", "p.95", "das Eins ist das Moment der Negation",
                     "属性既通过普遍媒介彼此独立（“也”），又作为规定性彼此排斥（“一”）——知觉在“物是一”与“物是多”之间来回切换标准，陷入无限摇摆。"),
                    ("矛盾被推给对象", "p.95", "ein einfaches Zusammen von vielen",
                     "知觉把矛盾分配给对象，却不知道矛盾就在它自己的判断活动中：范畴（一/多、本质/偶性、自在/为他）是意识自己带来的。"),
                ],
                "diagnose": "**引擎第一转的延长与反思的预演**：概念＝事物（统一体）；判断＝知觉的判断活动——用范畴规定对象；推论＝“也”（杂多与统一的中介）。但推论的统一暴露出范畴本身不自洽：意识用“一”判断时对象呈现为多，用“多”判断时又必须是一。**范畴不是被动反映对象，而是主动建构对象**——这是引擎第一次显形“知性工具性”，也预告了本质论式的“反思”做功（一切通过对立面映现自身）。",
                "uebergang": "知觉的摇摆逼迫意识寻求“无条件的共相”——一个不依赖于个别事物、不再摇摆的普遍性领域。知性（Verstand）登场。",
            },
        ],
    },
    3: {
        "title": "第三章 力和知性；现象和超感官世界",
        "pages": "107–135",
        "mode": "过渡 → 反思换挡（本质论预演）",
        "gestalten": [
            {
                "name": "力和知性",
                "position": "意识篇的顶点",
                "bestimmung": "知性＝科学思维的代表：不满足于知觉对个别事物的摇摆判断，要在现象背后寻找**普遍规律**与**内在本质**。它的对象是无条件共相（Unbedingt-Allgemeine）。",
                "bewegung": [
                    ("力的概念", "p.109", "Diese Bewegung ist aber dasjenige, was Kraft genannt wird",
                     "知觉的真理＝无条件共相。知性把它把握为“力”：外化（Äußerung，展开为杂多质料）与收回（in sich zurückgedrängt，回到力本身）的往复运动。但两环节之所以能区分并关联，**本身就是知性自己的建构**——差别“实际上仅存在于思想之中”。"),
                    ("力的真理是思想", "p.114", "Die Wahrheit der Kraft bleibt also nur der Gedanke derselben",
                     "两力相互激励（Sollizitieren）的游戏表明：力的环节没有独立实体，其“存在”只是通过他者而被设定——力的真理“只是关于力的思想”。实在化同时就是实在性的丧失。"),
                    ("现象与内在", "p.116", "Es heißt darum Erscheinung, denn Schein nennen wir das Sein",
                     "力作为媒介成为“现象”（Erscheinung）——直接在其自身即是非存在的“存在”（Schein）。知性透过现象之幕“看到”内在世界（超感官世界）。"),
                    ("空的彼岸", "p.117", "im Leeren nichts erkannt wird",
                     "超感官世界最初是空洞的彼岸：“在空虚中什么也不会被认识”。它只是现象的否定，知性必须用自己的概念去填充它。"),
                    ("超感官世界即现象之现象", "p.118", "Das Übersinnliche ist also die Erscheinung als Erscheinung",
                     "“超感官世界即现象之现象”：内在核心不是现象背后独立自存的彼岸，而是**现象作为现象**的真理——现象自身运动被知性固定下来的普遍结构。世界的二重化是知性设立对立面并试图超越它的活动。"),
                    ("规律王国及其局限", "p.119", "ein ruhiges Reich von Gesetzen",
                     "知性用“规律”填充超感官世界：规律王国是“知觉世界的直接提高为普遍成分”。但规律不充分：特殊规律被并入“万有引力”式的统一时，失去一切规定性——统一一切规律的规律只表达“规律的概念”本身。"),
                    ("颠倒的世界", "p.127", "Diese zweite übersinnliche Welt ist auf diese Weise die verkehrte Welt",
                     "同一个现象世界完全可以被相反的规律体系描述：第二个超感官世界＝第一个的**颠倒的世界**。甜的变酸、磁极互换、复仇之律在颠倒世界中变成宽恕——世界的规定取决于知性采取的规范框架。"),
                    ("内在差别与无限性", "p.130", "Nur so ist sie der Unterschied als innerer oder Unterschied an sich selbst",
                     "颠倒之颠倒消解了“世界”与“颠倒的世界”的固定对立：差别不再是两个独立存在之间的外在对立，而是**内在的差别**——“自身同一者与它自身的排斥”。这个内在差别就是无限性。"),
                    ("帘幕撤消", "p.135", "Dieser Vorhang ist also vor dem Innern weggezogen",
                     "“遮蔽内在世界的帘幕撤消了，出现的是内在世界对内在世界的直观。” 知性在现象与超感官世界中“所认识的只是它自己”——“帘幕后什么也没有，除非我们自己走进去”。这个结果是自我意识。"),
                ],
                "diagnose": "**引擎在意识介质中的换挡（过渡→反思）**：概念＝无条件共相；判断＝知性设立现象/本质、内在/外在的对立；推论＝无限性——对立被收摄为内在差别，知性认出对象的内在核心就是它自己的活动。**“世界依赖于理性的构建”在这里获得第一个完整证明**：超感官世界不是被发现的，而是被知性建立的。但引擎的反思还是“对象性的”——知性把真理当作彼岸的“物”，还不知道这个真理就是它自己。",
                "uebergang": "知性认识到：它看的“对象”的核心是它自己的活动。它必须把目光从对象转向自身——不是“我知道这个物”，而是“我知道我知道这个物”。第四章自我意识（欲望）登场。",
            },
        ],
    },
}


# ------------------------------------------------------------------ 渲染
def mark_cited(text: str, snippets: list) -> str:
    """把被引用的片段在原文中用 <mark class=cited> 标出（下划线+高亮，不重叠合并）"""
    if not snippets:
        return text
    low = text.lower()
    marks = []
    for snip in snippets:
        s = snip.lower()
        start = 0
        while True:
            i = low.find(s, start)
            if i < 0:
                break
            marks.append((i, i + len(s)))
            start = i + len(s)
    if not marks:
        return text
    marks.sort()
    merged = []
    for a, b in marks:
        if merged and a < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    out, prev = [], 0
    for a, b in merged:
        out.append(text[prev:a])
        out.append(f'<mark class="cited">{text[a:b]}</mark>')
        prev = b
    out.append(text[prev:])
    return "".join(out)


def render_chain_strip(chain: dict) -> str:
    """命题链（设定→展开→重建→过渡）：章节收尾的链条摘要"""
    if not chain:
        return ""
    rows = ""
    for key, label in (("set", "设定"), ("expand", "展开"), ("rebuild", "重建"), ("next", "过渡")):
        v = chain.get(key)
        if v:
            rows += (f'<div class="chain-row"><span class="chain-row-label">{label}</span>'
                     f'<span>{inline(v)}</span></div>')
    return (f'<div class="chain-strip"><span class="chain-strip-title">⚙️ 命题链 · 设定→展开→重建</span>'
            f'{rows}</div>')


def render_glossary() -> str:
    """页面底部通栏术语表：完整主表，两列，不区分原文/笔记侧"""
    if not GLOSS:
        return ""
    items = sorted(GLOSS.values(), key=lambda x: x[0].lower())
    rows = "".join(
        f'<div class="gloss-item"><span class="gloss-de">{_html.escape(t)}</span>'
        f'<span class="gloss-zh">{_html.escape(z)}</span></div>'
        for t, z in items)
    return (f'<section class="glossary" id="gloss"><h2>术语表 · 全书通览'
            f'<span class="gloss-count">（{len(items)} 条）</span></h2>'
            f'<p class="gloss-note">译法以笔记正文为准；同一德文词跨作品译法统一（哲学家主表 '
            f'viewpoints/glossary/黑格尔.json）。</p>'
            f'<div class="gloss-grid">{rows}</div></section>')


def render_rh(pid: str) -> str:
    """未引段阅读辅助（内侧内容：首/末/难句分块 + 障碍词；外层由 para_html 包成右栏 .rh-note）"""
    rh = RH.get(pid)
    if not rh:
        return ""
    parts = []
    for key, label in (("first", "首句"), ("middle", "难句"), ("last", "末句")):
        chunks = rh.get(key)
        if not chunks:
            continue
        rows = "".join(
            f'<div class="rh-row"><span class="rh-de">{_html.escape(c["de"])}</span>'
            f'<span class="rh-zh">{_html.escape(c["zh"])}</span></div>'
            for c in chunks)
        parts.append(f'<div class="rh-sec"><span class="rh-sec-label">{label}</span>{rows}</div>')
    words = rh.get("words", [])
    wc = "".join(f'<span class="rh-w"><i>{_html.escape(w["de"])}</i> '
                 f'<b>{_html.escape(w["zh"])}</b></span>' for w in words)
    if wc:
        parts.append(f'<div class="rh-sec"><span class="rh-sec-label">障碍词</span>{wc}</div>')
    return "".join(parts)


def para_html(p: dict, pnum: int, chapter: int, snippets: list) -> str:
    nm = f'<span class="pnum">{chapter}.{pnum}</span>'
    text = mark_cited(norm(p["text"]), snippets)
    bm = (f'<button class="bm-add" type="button" data-bm="{chapter}.{pnum}" '
          f'title="书签：{chapter}.{pnum}">＋</button>')
    p_html = f'<p class="op" id="{p["id"]}">{nm} {text}{bm}</p>'
    rh = render_rh(p["id"]) if not snippets else ""
    if rh:
        # 阅读辅助归笔记侧：段落（左栏德文）+ 翻译卡（右栏），用 .pair 保证并排
        return f'<div class="pair">{p_html}<div class="rh-note">{rh}</div></div>'
    return p_html


def resolve_citation(quote: str, norm_paras: list):
    q = norm(quote)
    for pid, pno, ptext in norm_paras:
        if q.lower() in ptext.lower():
            return (pid, pno)
    return None


def _gestalt_blocks(paras: list, g: dict, start_sec: int, start_para: int) -> list:
    """单个 gestalt → 小节块序列（det + mov* + end）；小节号从 start_sec 连续；
    paras 从 start_para 开始消费（前一个 gestalt 已消费的部分不在本 gestalt 的 det 里）。"""
    norm_paras = [(p["id"], p.get("page"), norm(p["text"])) for p in paras]
    cites = []
    for item in g["bewegung"]:
        label, page, quote, explain = item[:4]
        supps = item[4] if len(item) > 4 else []
        diagram = item[5] if len(item) > 5 else None
        group = item[6] if len(item) > 6 else ""
        hit = resolve_citation(quote, norm_paras)
        idx = None
        if hit:
            for i, (pid, _, _) in enumerate(norm_paras):
                if pid == hit[0]:
                    idx = i
                    break
        cites.append({"label": label, "page": page, "quote": quote,
                      "explain": explain, "supps": supps, "diagram": diagram,
                      "group": group, "idx": idx})

    blocks = []
    # det：从 start_para 到第一个引文段（本 gestalt 的引文必须 >= start_para）
    first_idx = None
    for c in cites:
        if c["idx"] is not None and c["idx"] >= start_para:
            first_idx = c["idx"]
            break
    if first_idx is None:
        first_idx = max(start_para, len(paras) - 1)
    blocks.append({"kind": "det", "note": {"bestimmung": g["bestimmung"],
                                           "supps": g.get("supps", [])},
                   "paras": paras[start_para:first_idx]})
    prev = first_idx - 1
    for c in cites:
        idx = c["idx"]
        if idx is None or idx < start_para:
            idx = min(max(prev + 1, start_para), len(paras) - 1)
        start, end = prev + 1, max(idx, prev + 1)
        blocks.append({"kind": "mov", "note": c,
                       "paras": paras[start:end + 1]})
        prev = end
    tail = paras[prev + 1:] if prev + 1 < len(paras) else []
    blocks.append({"kind": "end", "note": {"diag": g["diagnose"], "tran": g["uebergang"],
                                           "chain": g.get("chain"),
                                           "chain_supps": g.get("chain_supps", [])},
                   "paras": tail})
    for i, b in enumerate(blocks, start_sec):
        b["sec"] = i
    return blocks


def build_blocks(paras: list, meta: dict) -> list:
    """把章节原文按 gestalt 切块（支持多 gestalt，如序言+导言同章）：
    每 gestalt = det + mov* + end；后一 gestalt 从上一 gestalt 消费尾段之后继续。"""
    n_gest = len(meta["gestalten"])
    blocks = []
    consumed = 0
    for gi, g in enumerate(meta["gestalten"]):
        gb = _gestalt_blocks(paras, g, 1, consumed)
        # 本 gestalt 消费到的最大段索引（只算 det+mov，end 是诊断块不算）
        mx = -1
        for b in gb:
            if b["kind"] in ("det", "mov") and b["paras"]:
                last = int(b["paras"][-1]["id"].rsplit("-p", 1)[1]) - 1
                mx = max(mx, last)
        # 最后一个 gestalt 的 end 拿全部剩余；非最后 gestalt 的 end 清空（段留给下一 gestalt）
        if gi == n_gest - 1:
            consumed = max(consumed, mx + 1)
        else:
            consumed = max(consumed, mx + 1)
            gb[-1]["paras"] = []
        blocks.extend(gb)
    for i, b in enumerate(blocks, 1):
        b["sec"] = i
    return blocks


def sec_label(blk: dict, chapter: int) -> str:
    if blk["kind"] == "det":
        name = "形态界定"
    elif blk["kind"] == "mov":
        name = blk["note"]["label"]
    else:
        name = "引擎诊断与过渡"
    return f"{chapter}.{blk['sec']} {name}"
def para_range(blk: dict, chapter: int) -> str:
    if not blk["paras"]:
        return ""
    first = blk["paras"][0]["id"].split("-p")[1]
    last = blk["paras"][-1]["id"].split("-p")[1]
    if first == last:
        return f"段落 {chapter}.{first}"
    return f"段落 {chapter}.{first}–{chapter}.{last}"


def chain_summary(blk: dict) -> str:
    """链路卡片的摘要：取该小节笔记的第一句"""
    if blk["kind"] == "det":
        txt = blk["note"]["bestimmung"]
    elif blk["kind"] == "mov":
        txt = blk["note"]["explain"]
    else:
        txt = blk["note"]["diag"]
    txt = re.sub(r"\*\*", "", txt)
    m = re.search(r"(.{0,64}?[。；;])", txt)
    if m:
        return m.group(1)
    return txt[:64]


def render_supps(supps: list) -> str:
    """讨论补充区块：每条 {date, title, content} 独立显示，默认展开；
    标题以 ⚙️ 开头的为「引擎标注」（die absolute Negativität 推动整体前进的关键），特别样式"""
    if not supps:
        return ""
    items = []
    for s in supps:
        date = _html.escape(s.get("date", ""))
        title = _html.escape(s.get("title", "讨论补充"))
        content = inline(s.get("content", ""))
        engine = title.startswith("⚙️")
        key = title.startswith("🔑")
        if engine:
            badge = '<span class="sup-badge">⚙️ 引擎 · die absolute Negativität</span>'
            cls = "sup-item engine"
        elif key:
            badge = '<span class="sup-badge key">🔑 关键概念</span>'
            cls = "sup-item key"
        else:
            badge = ""
            cls = "sup-item"
        items.append(
            f'<div class="{cls}">'
            f'{badge}'
            f'<span class="sup-date">{date}</span>'
            f'<span class="sup-title">{title}</span>'
            f'<p>{content}</p></div>')
    return ('<details class="sup" open><summary>📌 讨论补充'
            f'<span class="sup-count">（{len(supps)}）</span></summary>'
            f'{"".join(items)}</details>')


def render_diagram(dg: dict) -> str:
    """链路图：主人/奴隶 双节点 + 关系标注 + 底部结论条"""
    if not dg:
        return ""
    def node(n):
        return (f'<div class="dg-node"><div class="dg-label">{_html.escape(n.get("label", ""))}</div>'
                f'<div class="dg-sub">{_html.escape(n.get("sub", ""))}</div>'
                f'<ul>{"".join(f"<li>{_html.escape(p)}</li>" for p in n.get("points", []))}</ul></div>')
    mid = (f'<div class="dg-mid"><span class="dg-arrow">⇄</span>'
           f'<span>{_html.escape(dg.get("middle", ""))}</span></div>')
    bottom = (f'<div class="dg-bottom">{_html.escape(dg.get("bottom", ""))}</div>'
              if dg.get("bottom") else "")
    return (f'<div class="diagram"><div class="dg-title">{_html.escape(dg.get("title", ""))}</div>'
            f'<div class="dg-grid">{node(dg.get("left", {}))}{mid}{node(dg.get("right", {}))}</div>'
            f'{bottom}</div>')


# ── 本节术语条：德语名词翻译（照顾不熟悉德语的读者；哲学家术语主表 viewpoints/glossary/）──
GLOSS = {}
TERM_RES = {}

# 未引段阅读辅助：notes_pheno/reading_help.json（首/末/难句硬译分块 + 障碍词）
RH = {}


def load_reading_help():
    global RH
    p = NOTES_DIR / "reading_help.json"
    if p.exists():
        RH = json.loads(p.read_text(encoding="utf-8")).get("paragraphs", {})


def load_glossary(work: str = "精神现象学"):
    p = NOTES_DIR.parent / "viewpoints" / "glossary" / "黑格尔.json"
    if not p.exists():
        return
    data = json.loads(p.read_text(encoding="utf-8"))
    for e in data.get("terms", []):
        if work and work not in e.get("works", []):
            continue
        term, zh = e.get("term", ""), e.get("zh", "")
        if not term or not zh:
            continue
        key = term.lower()
        GLOSS[key] = (term, zh)
        # 词边界 + 常见名词/形容词变格后缀（s/e/en/es/n/em/er）；不匹配复合词内部
        TERM_RES[key] = re.compile(
            r"(?<![A-Za-zÄÖÜäöüß])" + re.escape(term) + r"(?:s|e|en|es|n|em|er)?"
            r"(?![A-Za-zÄÖÜäöüß])", re.IGNORECASE)


def match_gloss(q: str) -> list:
    """引文中命中的术语 [(key, 显示词, 译法)]，按引文出现顺序，上限 10；子串重复（如
    absolute Negativität 吞掉 Negativität）只留长者"""
    cands = []
    for key, (term, _) in GLOSS.items():
        m = TERM_RES[key].search(q)
        if m:
            cands.append((m.start(), m.end(), key, term))
    cands.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    kept = []
    for s, e, key, term in cands:
        if any(s >= ks and e <= ke for ks, ke, *_ in kept):
            continue
        kept.append((s, e, key, term))
    kept.sort(key=lambda x: x[0])
    return [(k, t, GLOSS[k][1]) for _, _, k, t in kept[:10]]


def render_gterms(items: list) -> str:
    """本节术语条：德文词 中文（§=全书首次出现）；items 为 (key, 显示词, 译法, 是否首次)"""
    if not items:
        return ""
    chips = []
    for key, term, zh, first in items:
        mark = ('<sup class="gt-first" title="全书首次出现">§</sup>' if first else "")
        chips.append(f'<span class="gt"><i>{_html.escape(term)}</i>{mark} '
                     f'<b>{_html.escape(zh)}</b></span>')
    return f'<div class="gterms"><span class="gt-label">本节术语</span>{"".join(chips)}</div>'


def render_group_badge(group: str) -> str:
    """序言等长章节的分组徽标（B. 真理=主体 等）"""
    if not group:
        return ""
    return f'<div class="group-badge">{_html.escape(group)}</div>'


def render_block(blk: dict, chapter: int, chapter_norm: list, cited_map: dict,
                 prev_blk: dict | None, next_blk: dict | None) -> str:
    paras = blk["paras"]
    note = blk["note"]
    is_mov = blk["kind"] == "mov"

    # 锚段（引文所在段）：mov 用引文解析；否则取末段。索引相对 blk["paras"]
    anchor_idx = None
    if is_mov:
        hit = resolve_citation(note["quote"], chapter_norm)
        if hit:
            for i, p in enumerate(paras):
                if p["id"] == hit[0]:
                    anchor_idx = i
                    break
    if anchor_idx is None:
        anchor_idx = max(len(paras) - 1, 0) if paras else 0
    anchor_num = paras[anchor_idx]["id"].split("-p")[1] if paras else ""
    pr = (f"段落 {chapter}.{anchor_num}" if is_mov and anchor_num
          else para_range(blk, chapter))

    def p_html(p):
        return para_html(p, int(p["id"].rsplit("-p", 1)[1]), chapter,
                         cited_map.get(p["id"], []))

    if blk["kind"] == "det":
        orig = "".join(p_html(p) for p in paras)
        note_html = (f'<div class="bnote det"><h4><span class="secno">小节 {chapter}.{blk["sec"]}</span> 形态界定'
                     f'<span class="prange">（{pr}）</span></h4>'
                     f'<p>{inline(note["bestimmung"])}</p>'
                     f'{render_gterms(blk.get("gterms", []))}'
                     f'{render_supps(note.get("supps"))}</div>')
    elif is_mov:
        hit = resolve_citation(note["quote"], chapter_norm)
        if hit:
            pid, pno = hit
            pnum = pid.split("-p")[1]
            tip = f'跳转到原文段落（原书 p.{pno}）' if pno else "跳转到原文段落"
            link = f'<a class="cite" href="#{pid}" title="{tip}">〔段 {pnum}〕</a>'
            qhtml = f'<span class="q">{_html.escape(norm(note["quote"]))}</span>'
        else:
            link = f'<span class="cite miss">〔p.{note["page"]}？未命中〕</span>'
            qhtml = f'<span class="q miss">{_html.escape(norm(note["quote"]))}</span>'
        note_html = (f'<div class="bnote mov"><h4><span class="secno">小节 {chapter}.{blk["sec"]}</span> '
                     f'{_html.escape(note["label"])} {link}'
                     f'<span class="prange">（{pr}）</span></h4>'
                     f'{render_group_badge(note.get("group"))}'
                     f'<p class="qwrap">“{qhtml}”</p>'
                     f'<p>{inline(note["explain"])}</p>'
                     f'{render_gterms(blk.get("gterms", []))}'
                     f'{render_diagram(note.get("diagram"))}'
                     f'{render_supps(note.get("supps"))}</div>')
        # 锚段 + 笔记放进嵌套双栏 .pair：笔记强制贴在引文所在段旁边
        pre = paras[:anchor_idx]
        anchor = paras[anchor_idx]
        pre_html = "".join(p_html(p) for p in pre)
        anchor_html = p_html(anchor)
        chain_html = render_chain(prev_blk, next_blk, chapter)
        orig = (pre_html + f'<div class="pair">{anchor_html}'
                f'<div class="b-note">{chain_html}{note_html}</div></div>')
    else:
        orig = "".join(p_html(p) for p in paras)
        note_html = (f'<div class="bnote end"><h4><span class="secno">小节 {chapter}.{blk["sec"]}</span> 引擎诊断'
                     f'<span class="prange">（{pr}）</span></h4>'
                     f'<p>{inline(note["diag"])}</p>'
                     f'<h4>失败与过渡</h4><p>{inline(note["tran"])}</p>'
                     f'{render_chain_strip(note.get("chain"))}'
                     f'{render_supps(note.get("chain_supps"))}'
                     f'{render_supps(note.get("supps"))}</div>')

    blk_id = f'ch{chapter}-s{blk["sec"]}'
    if blk["kind"] in ("det", "end"):
        # 无引文锚：笔记在右栏自动放置（rhpair 之后），不设固定行
        return (f'<div class="block" id="{blk_id}">{orig}'
                f'<div class="b-note">{render_chain(prev_blk, next_blk, chapter)}{note_html}</div></div>')
    # mov：orig 已含 .pair（锚段+笔记）
    return f'<div class="block" id="{blk_id}">{orig}</div>'


def render_chain(prev_blk: dict | None, next_blk: dict | None, chapter: int) -> str:
    """链路卡片：上一小节 / 下一小节（紧凑摘要）"""
    chain = ""
    if prev_blk:
        chain += (f'<a class="chain up" href="#ch{chapter}-s{prev_blk["sec"]}">'
                  f'<span class="chain-dir">↑ 上一小节</span>'
                  f'<span class="chain-title">{_html.escape(sec_label(prev_blk, chapter))}</span>'
                  f'<span class="chain-sum">{_html.escape(chain_summary(prev_blk))}</span></a>')
    if next_blk:
        chain += (f'<a class="chain down" href="#ch{chapter}-s{next_blk["sec"]}">'
                  f'<span class="chain-dir">↓ 下一小节</span>'
                  f'<span class="chain-title">{_html.escape(sec_label(next_blk, chapter))}</span>'
                  f'<span class="chain-sum">{_html.escape(chain_summary(next_blk))}</span></a>')
    return f'<div class="chain">{chain}</div>' if chain else ""


def available_chapters() -> list:
    """已有原文 + 已有笔记数据的章节号（含序言 ch0）"""
    chs = []
    for n in range(0, 9):
        if CHAPTER_FILES.get(n) and all((EX / f).exists() for f in CHAPTER_FILES[n]):
            np_ = NOTES_DIR / f"ch{n}.json"
            if np_.exists() or (n in NOTES):
                chs.append(n)
    return chs


def compute_gterms(blk: dict, seen_terms: set) -> None:
    """为小节计算术语条（写回 blk['gterms']）：
    - det（形态界定/引导段落）：对 bestimmung 文本匹配（术语表中有的词都要标出）
    - mov（运动环节）：对引文德文匹配
    - end（诊断）：不标
    seen_terms 跨块追踪「全书首次出现」（§ 标记）"""
    if blk["kind"] == "mov":
        q = norm(blk["note"]["quote"]).lower()
    elif blk["kind"] == "det":
        q = norm(blk["note"]["bestimmung"]).lower()
    else:
        blk["gterms"] = []
        return
    terms = match_gloss(q)
    firsts = {k for k, _, _ in terms} - seen_terms
    seen_terms |= {k for k, _, _ in terms}
    blk["gterms"] = [(k, t, z, k in firsts) for k, t, z in terms]


def build():
    load_glossary()
    load_reading_help()
    chs = available_chapters()
    pages = {n: load_chapter(n) for n in chs}

    sections = []
    toc_lis = []
    seen_terms = set()  # 全书首次出现追踪（§ 标记）
    for n in chs:
        meta = load_notes(n)
        blocks = build_blocks(pages[n], meta)
        # 每环节匹配术语 + 首次出现标记（det 引导段落也标注术语表中的词）
        for b in blocks:
            compute_gterms(b, seen_terms)
        chapter_norm = [(p["id"], p.get("page"), norm(p["text"])) for p in pages[n]]
        # 引文标注映射：段落 id → 被引片段列表
        cited_map = {p["id"]: [] for p in pages[n]}
        for item in meta["gestalten"]:
            for b_ in item["bewegung"]:
                label, page, quote, explain = b_[:4]
                hit = resolve_citation(quote, chapter_norm)
                if hit:
                    cited_map.setdefault(hit[0], []).append(norm(quote))
        sections.append(
            f'<section class="gestalt" id="ch{n}">'
            f'<div class="ghead"><h2>{_html.escape(meta["title"])}</h2>'
            f'<div class="gmeta">做功方式：{_html.escape(meta["mode"])} · '
            f'小节编号为编者所加（原书未分段）</div></div>'
            f'{"".join(render_block(b, n, chapter_norm, cited_map,
                                    blocks[i - 1] if i > 0 else None,
                                    blocks[i + 1] if i + 1 < len(blocks) else None)
                       for i, b in enumerate(blocks))}'
            f'</section>')
        # TOC 子项：group 变化时插入分组标题（序言等长章节的指引层级）
        sub_parts = []
        cur_group = None
        for b in blocks:
            gp = (b.get("note") or {}).get("group", "") if b.get("kind") == "mov" else ""
            if gp and gp != cur_group:
                sub_parts.append(f'<li class="toc-group">{_html.escape(gp)}</li>')
                cur_group = gp
            sub_parts.append(
                f'<li><a href="#ch{n}-s{b["sec"]}">{sec_label(b, n)}'
                f'<span class="toc-r">（{para_range(b, n)}）</span></a></li>')
        sub = "".join(sub_parts)
        toc_lis.append(
            f'<li class="chap"><a href="#ch{n}">{_html.escape(meta["title"])}</a><ul>{sub}</ul></li>')

    toc_items = "\n".join(toc_lis)
    # 编者 Brief 置顶（TOC 第一项 + 正文最前）
    brief_toc = ('<li class="chap brief-toc"><a href="#brief">'
                 f'{_html.escape(brief_pheno.BRIEF_TITLE)}</a></li>')
    toc_items = brief_toc + "\n" + toc_items

    html = TEMPLATE.replace("__TOC__", toc_items).replace(
        "__SECTIONS__", brief_pheno.render_brief() + "\n".join(sections) + render_glossary())
    html = html.replace("__RANGE__", "序言 + 第1-8章" if 0 in chs else
                        (f"第{chs[0]}-{chs[-1]}章" if chs else ""))
    html = html.replace("__BOOK__", "精神现象学 · 原文注释版")
    OUT.write_text(html, encoding="utf-8")

    # 校验：统计引文命中
    total = hit = 0
    for n in chs:
        for g in load_notes(n)["gestalten"]:
            for b_ in g["bewegung"]:
                label, page, quote, explain = b_[:4]
                total += 1
                q = norm(quote)
                if any(q.lower() in norm(p["text"]).lower() for p in pages[n]):
                    hit += 1
    print(f"[产物] {OUT.name}（{OUT.stat().st_size} 字节）")
    print(f"[校验] 引文对拍：{hit}/{total} 命中原文（失败 0 = 全部通过）")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__BOOK__（__RANGE__）</title>
<style>
:root{
  --bg:#faf7f1; --bg-soft:#f2ecdf; --card:#fffdf8; --text:#2e2a24; --text-soft:#6f675a;
  --border:#e4dbc9; --accent:#8c3b2e; --accent-soft:#f0e2d7;
  --quote-bg:#f6efe3; --quote-border:#b98a5a; --code-bg:#efe8da;
  --shadow:rgba(70,45,20,.10); --sidebar-bg:#f4eee2; --sidebar-text:#544c40; --sidebar-active:#8c3b2e;
  --serif:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",SimSun,STSong,Georgia,"Times New Roman",serif;
  --sans:"Source Han Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  --mono:Consolas,"JetBrains Mono",Menlo,monospace;
  color-scheme:light;
}
:root[data-theme="dark"]{
  --bg:#1d1b17; --bg-soft:#2a2620; --card:#242019; --text:#dcd4c3; --text-soft:#a09886;
  --border:#3b352b; --accent:#d08a6a; --accent-soft:#3b2b21;
  --quote-bg:#2a251f; --quote-border:#a5744f; --code-bg:#2c2720;
  --shadow:rgba(0,0,0,.35); --sidebar-bg:#201d18; --sidebar-text:#b4ab9b; --sidebar-active:#e0a585;
  --pnum-bg:#243a42; --pnum-fg:#8fc3d4; --cite-bg:#4a3c22;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--serif);font-size:16.5px;line-height:1.85;-webkit-font-smoothing:antialiased}
#progress{position:fixed;top:0;left:0;height:3px;width:0;background:var(--accent);z-index:100}
.layout{display:grid;grid-template-columns:300px minmax(0,1fr);min-height:100vh}
aside.toc{position:sticky;top:0;height:100vh;overflow-y:auto;background:var(--sidebar-bg);border-right:1px solid var(--border);padding:1.3rem 1rem 2rem;font-family:var(--sans);font-size:.82rem;line-height:1.55}
.toc-title{font-weight:700;font-size:1rem;margin:0 0 .5rem;color:var(--text);padding:0 .45rem}
.toc-pos{margin:0 0 .8rem;padding:.35rem .45rem;background:var(--accent-soft);border-radius:6px;font-family:var(--sans);font-size:.78em;color:var(--sidebar-active)}
.toc-pos #cur-pos{font-weight:700}
#toc-list ul{list-style:none;margin:0;padding:0}
#toc-list ul ul{padding-left:.85rem;margin:.1rem 0 .25rem;border-left:1px dotted var(--border)}
#toc-list li{margin:.15rem 0}
#toc-list li.chap{margin-top:.4rem}
#toc-list a{display:block;color:var(--sidebar-text);text-decoration:none;padding:.24rem .45rem;border-radius:6px;word-break:break-word}
#toc-list a:hover{background:var(--bg-soft);color:var(--text)}
#toc-list a.active{background:var(--accent-soft);color:var(--sidebar-active);font-weight:600}
.toc-r{color:var(--text-soft);font-size:.78em;margin-left:.3em}
.toc-foot{margin:1.4rem .45rem 0;color:var(--text-soft);font-size:.75rem;border-top:1px solid var(--border);padding-top:.8rem}
main{max-width:76rem;width:100%;margin:0 auto;padding:2.2rem clamp(1rem,3vw,2.5rem) 4rem}
.doc-head{margin-bottom:1.8rem;padding-bottom:1rem;border-bottom:2px solid var(--border)}
.doc-head h1{font-size:1.7rem;margin:0 0 .35rem;letter-spacing:.03em;line-height:1.3}
.doc-sub{margin:0;color:var(--text-soft);font-family:var(--sans);font-size:.92rem}
section.gestalt{margin:2.6rem 0}
.ghead h2{font-size:1.35rem;margin:0 0 .3rem;padding:.15rem 0 .15rem .7rem;border-left:5px solid var(--accent)}
.gmeta{color:var(--text-soft);font-family:var(--sans);font-size:.85rem;margin-bottom:.9rem}
.block{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:0 1.4rem;margin:1.4rem 0;scroll-margin-top:20px}
.pair{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:0 1.4rem;grid-column:1/-1}
.block p.op{position:relative;grid-column:1;margin:.55rem 0;padding:.85rem 1rem;background:var(--card);border:1px solid var(--border);border-radius:10px;box-shadow:0 1px 3px var(--shadow);font-size:.95em;line-height:1.75}
.opbox{grid-column:1}
.block .page{display:inline-block;min-width:2.6em;text-align:center;background:var(--accent-soft);color:var(--accent);border-radius:4px;font-family:var(--sans);font-size:.72em;margin-right:.4em;padding:.05em .35em}
.block .pnum{display:inline-block;background:var(--pnum-bg,#e4eef2);color:var(--pnum-fg,#2f6475);border-radius:4px;font-family:var(--sans);font-size:.72em;margin-right:.5em;padding:.05em .4em}
mark.cited{background:var(--cite-bg,#f7e8c8);color:inherit;text-decoration:underline;text-underline-offset:2px;border-radius:2px;padding:0 .12em}
.bnote .secno{display:inline-block;background:var(--accent-soft);color:var(--accent);border-radius:4px;font-size:.78em;padding:.08em .45em;margin-right:.4em;font-family:var(--sans)}
.bnote .prange{color:var(--text-soft);font-size:.78em;font-family:var(--sans);margin-left:.3em}
details.sup{margin-top:.6rem;border-top:1px dashed var(--border);padding-top:.45rem}
details.sup summary{cursor:pointer;font-family:var(--sans);font-size:.82em;color:var(--accent);font-weight:600;list-style:none}
details.sup summary::-webkit-details-marker{display:none}
details.sup summary::before{content:"▸ ";font-size:.8em}
details.sup[open] summary::before{content:"▾ "}
.sup-count{color:var(--text-soft);font-weight:400;font-size:.8em;margin-left:.3em}
.sup-item{margin:.5rem 0 0;padding:.45rem .6rem;background:var(--bg-soft);border-radius:6px}
.sup-item.engine{border-left:4px solid var(--accent);background:var(--accent-soft);padding:.55rem .7rem}
.sup-item.key{padding:.55rem .7rem}
.sup-badge{display:inline-block;background:var(--accent);color:#fff;font-family:var(--sans);font-size:.7em;font-weight:600;padding:.14em .6em;border-radius:3px;margin-right:.45em;vertical-align:middle}
.sup-badge.key{background:#b45309}
.gterms{margin:.6rem 0 .15rem;padding:.45rem .6rem;background:var(--bg-soft);border-radius:6px;font-family:var(--sans);font-size:.8em;line-height:2}
.gt-label{color:var(--text-soft);margin-right:.55em;font-size:.78em}
.gt{display:inline-block;margin-right:.6em;white-space:nowrap}
.gt i{font-style:italic;color:var(--accent)}
.gt b{font-weight:600;color:var(--text)}
.gt-first{color:#b45309;font-weight:700;margin-left:.18em;font-size:.72em}
.group-badge{display:inline-block;background:var(--accent-soft);color:var(--accent);border:1px solid var(--accent);font-family:var(--sans);font-size:.72em;font-weight:700;padding:.12em .7em;border-radius:4px;margin:.15rem 0 .4rem}
.toc-group{list-style:none;margin:.35rem 0 .1rem;padding:.1rem .4rem;font-family:var(--sans);font-size:.8em;font-weight:700;color:var(--accent);border-bottom:1px dotted var(--border)}
.rh-note{grid-column:2;align-self:start;position:sticky;top:1rem;margin:.55rem 0;padding:.5rem .6rem;background:var(--bg);border:1px dashed var(--border);border-radius:8px;font-size:.88em;line-height:1.7}
/* 辅助阅读开关：只隐藏 rh-note 卡，不改原文段排版（原文保持原 grid 位） */
body.no-rh .rh-note{display:none}
.rh-sec{margin:.15rem 0}
.rh-sec-label{display:inline-block;font-family:var(--sans);font-size:.72em;color:var(--text-soft);margin-right:.5em;min-width:3.2em}
.rh-row{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:0 .8rem;margin:.1rem 0}
.rh-de{font-style:italic;color:var(--text-soft)}
.rh-zh{color:var(--text)}
.rh-w{display:inline-block;margin-right:.6em;white-space:nowrap;font-family:var(--sans);font-size:.84em}
.rh-w i{font-style:italic;color:var(--accent);margin-right:.2em}
.rh-w b{font-weight:600}
.glossary{max-width:76rem;width:100%;margin:2.6rem auto 1rem;padding-top:1.6rem;border-top:2px solid var(--border)}
.glossary h2{font-size:1.35rem;margin:0 0 .5rem;padding-left:.7rem;border-left:5px solid var(--accent)}
.gloss-count{font-family:var(--sans);font-size:.8em;color:var(--text-soft);margin-left:.5em}
.gloss-note{color:var(--text-soft);font-size:.85rem;margin:0 0 1rem}
.gloss-grid{column-count:2;column-gap:3rem}
.gloss-item{break-inside:avoid;display:flex;gap:.6rem;padding:.22rem 0;border-bottom:1px dotted var(--border);font-size:.92em}
.gloss-de{font-style:italic;color:var(--accent);min-width:13em;flex-shrink:0}
.gloss-zh{color:var(--text)}
.chain-strip{margin:.7rem 0 .3rem;padding:.5rem .65rem;background:var(--card);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:8px;font-size:.9em}
.chain-strip-title{display:block;font-family:var(--sans);font-size:.78em;font-weight:600;color:var(--accent);margin-bottom:.3rem}
.chain-row{display:grid;grid-template-columns:3.2em minmax(0,1fr);gap:.4rem;margin:.12rem 0}
.chain-row-label{font-family:var(--sans);font-size:.78em;color:var(--text-soft)}
.chain-row>span:last-child{line-height:1.6}
.sup-date{display:inline-block;font-family:var(--sans);font-size:.72em;background:var(--pnum-bg,#e4eef2);color:var(--pnum-fg,#2f6475);border-radius:4px;padding:.04em .5em;margin-right:.4em}
.sup-title{font-weight:600;font-size:.9em}
.sup-item p{margin:.35rem 0 0;font-size:.92em}
.diagram{margin:.7rem 0 .3rem;padding:.6rem;background:var(--card);border:1px solid var(--border);border-radius:8px}
.dg-title{font-family:var(--sans);font-size:.82em;font-weight:600;color:var(--accent);margin-bottom:.45rem}
.dg-grid{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);gap:.5rem;align-items:stretch}
.dg-node{border:1px solid var(--border);border-radius:8px;padding:.5rem .6rem;background:var(--bg-soft)}
.dg-label{font-weight:700;font-size:.95em}
.dg-sub{color:var(--accent);font-size:.82em;margin:.15rem 0 .35rem;font-family:var(--sans)}
.dg-node ul{margin:.3rem 0 0;padding-left:1.1em;font-size:.85em}
.dg-node li{margin:.15rem 0}
.dg-mid{align-self:center;text-align:center;font-size:.78em;color:var(--text-soft);font-family:var(--sans);max-width:10em;line-height:1.5}
.dg-arrow{display:block;font-size:1.3em;color:var(--accent);margin-bottom:.2rem}
.dg-bottom{margin-top:.5rem;padding:.35rem .5rem;background:var(--accent-soft);border-radius:6px;font-size:.8em;font-family:var(--sans)}
.b-note{grid-column:2;align-self:start;position:sticky;top:1rem}
.chain{display:flex;flex-direction:column;gap:.4rem;margin-bottom:.6rem}
.chain a{display:block;text-decoration:none;border:1px dashed var(--border);border-radius:8px;padding:.45rem .6rem;background:var(--bg)}
.chain a:hover{border-color:var(--accent);background:var(--accent-soft)}
.chain-dir{display:block;font-family:var(--sans);font-size:.72em;color:var(--text-soft)}
.chain-title{display:block;font-size:.85em;color:var(--accent);font-weight:600}
.chain-sum{display:block;font-size:.78em;color:var(--text-soft);line-height:1.5}
.bnote{border-left:3px solid var(--quote-border);padding:.55rem .95rem;border-radius:0 8px 8px 0}
.bnote h4{margin:0 0 .4rem;font-size:.98rem;color:var(--accent);font-family:var(--sans)}
.bnote p{margin:.45rem 0;font-size:.96em}
.bnote.mov{background:var(--bg-soft)}
.bnote.det,.bnote.end{background:var(--quote-bg)}
.bnote.end h4{margin-top:.7rem}
.bnote.end h4:first-child{margin-top:0}
.bnote .qwrap{color:var(--text-soft);font-style:italic;font-size:.9em}
.bnote .q{font-style:italic}
.bnote .cite{color:var(--accent);text-decoration:none;border-bottom:1px dotted var(--accent);font-family:var(--sans);font-size:.78em}
.bnote .cite:hover{background:var(--accent-soft)}
.bnote .miss{color:#a33;border-bottom-color:#a33}
p.op:target{background:var(--accent-soft);outline:2px solid var(--accent);border-radius:6px;padding:.3rem .5rem}
p.op.flash{animation:bmflash 1.6s ease}
@keyframes bmflash{0%,60%{background:var(--accent-soft);outline:2px solid var(--accent)}100%{background:var(--card)}}
/* ══ 功能侧（明暗主题 / 辅助阅读 / 书签）══
   约定：三者作为一组固定于右侧，统一右对齐 right:1rem、圆角、同尺寸；
   top 自上而下递增（1rem / 3.4rem / 5.8rem）。调整其一必须同步三者，
   书签栏打开时整体左移 230px（bm-open 规则）。 */
.fn-btn{position:fixed;right:1rem;z-index:90;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:1rem;padding:.5rem .6rem;border-radius:10px;cursor:pointer;box-shadow:0 2px 8px var(--shadow);font-family:var(--sans);line-height:1}
#theme-btn{top:1rem}
#rh-toggle{top:3.4rem}
#bm-toggle{top:5.8rem;z-index:85}
.fn-btn:hover{color:var(--accent)}
#rh-toggle.off{opacity:.45;text-decoration:line-through}
#top-btn{position:fixed;bottom:1.2rem;right:1.2rem;z-index:90;display:none;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:1rem;padding:.5rem .65rem;border-radius:10px;cursor:pointer;box-shadow:0 2px 8px var(--shadow);font-family:var(--sans)}
#top-btn.show{display:block}
/* ── 书签栏（最右侧固定窄条）── */
#bm-wrap{position:fixed;top:0;right:0;bottom:0;width:230px;z-index:80;display:flex;flex-direction:column;background:var(--sidebar-bg);border-left:1px solid var(--border);transform:translateX(100%);transition:transform .22s ease;font-family:var(--sans)}
#bm-wrap.open{transform:translateX(0)}
#bm-head{display:flex;align-items:center;justify-content:space-between;padding:.55rem .7rem;border-bottom:1px solid var(--border)}
#bm-title{font-weight:700;font-size:.85rem;color:var(--text)}
#bm-clear{background:none;border:1px solid var(--border);color:var(--text-soft);border-radius:6px;font-size:.72rem;padding:.15rem .5rem;cursor:pointer;font-family:var(--sans)}
#bm-clear:hover{color:var(--accent);border-color:var(--accent)}
#bm-list{list-style:none;margin:0;padding:.4rem;overflow-y:auto;flex:1}
#bm-list li{display:flex;align-items:flex-start;gap:.35rem;margin:.15rem 0;padding:.3rem .4rem;border-radius:6px;cursor:pointer}
#bm-list li:hover{background:var(--bg-soft)}
#bm-list li.cur{background:var(--accent-soft)}
.bm-no{flex-shrink:0;font-family:var(--mono);font-size:.72rem;color:var(--accent);background:var(--accent-soft);border-radius:4px;padding:.06em .35em;margin-top:.1em}
.bm-txt{flex:1;font-size:.74rem;color:var(--text-soft);line-height:1.5;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.bm-del{flex-shrink:0;border:none;background:none;color:var(--text-soft);cursor:pointer;font-size:.8rem;padding:.05rem .2rem;border-radius:4px}
.bm-del:hover{color:var(--accent)}
.bm-add{position:absolute;right:.55rem;top:.35rem;opacity:0;border:1px solid var(--border);background:var(--card);color:var(--accent);font-size:.78rem;padding:.1rem .45rem;border-radius:6px;cursor:pointer;font-family:var(--sans);transition:opacity .15s}
p.op:hover .bm-add{opacity:1}
.bm-add:hover{background:var(--accent);color:#fff}
.bm-added{opacity:.85;background:var(--accent-soft);border-color:var(--accent)}
body.bm-open main,body.bm-open aside.toc{margin-right:230px}
body.bm-open #theme-btn{right:calc(1rem + 230px)}
body.bm-open #rh-toggle{right:calc(1rem + 230px)}
body.bm-open #top-btn{right:calc(1.2rem + 230px)}
body.bm-open #bm-toggle{right:calc(1rem + 230px)}
@media (max-width:1000px){
  #bm-wrap{width:min(78vw,300px)}
  .bm-add{opacity:.6;position:static;float:right;margin-left:.4rem}
  body.bm-open main{transition:margin-right .22s ease}
  body.bm-open #theme-btn{right:calc(1rem + min(78vw,300px))}
  body.bm-open #rh-toggle{right:calc(1rem + min(78vw,300px))}
  body.bm-open #top-btn{right:calc(1.2rem + min(78vw,300px))}
  body.bm-open #bm-toggle{right:calc(1rem + min(78vw,300px))}
}
@media (max-width:1000px){
  .layout{grid-template-columns:1fr}
  aside.toc{position:fixed;top:0;bottom:0;left:0;width:min(80vw,320px);transform:translateX(-102%);transition:transform .22s ease;z-index:85}
  aside.toc.open{transform:translateX(0)}
  #toc-open-btn{display:block;position:fixed;top:1rem;left:1rem;z-index:90;border:1px solid var(--border);background:var(--card);color:var(--text);padding:.5rem .65rem;border-radius:10px;cursor:pointer;font-family:var(--sans)}
  .cols{grid-template-columns:1fr}
  .block{grid-template-columns:1fr}
  .pair{grid-template-columns:1fr}
  .block p.op{grid-column:1}
  .b-note{grid-column:1;position:static}
  .rh-note{grid-column:1;position:static}
}
@media print{
  :root,:root[data-theme="dark"]{--bg:#fff;--text:#111;--text-soft:#444;--border:#bbb;--accent:#555;--accent-soft:#eee;--quote-bg:#f6f6f6;--quote-border:#999;--sidebar-bg:#fff;--card:#fff;--shadow:none;color-scheme:light}
  body{font-size:11pt;background:#fff;color:#000}
  aside.toc,#theme-btn,#top-btn,#toc-open-btn,#progress,#bm-wrap,#bm-toggle,#rh-toggle{display:none!important}
  .layout{display:block}
  main{max-width:none;padding:0}
  .block{grid-template-columns:1fr 1fr}
  p.op{break-inside:avoid}
}

/* 编者 Brief */
.brief{max-width:76rem;width:100%;margin:0 auto 2rem;padding:1.4rem 1.6rem;background:linear-gradient(180deg,var(--bg-soft),var(--bg));border:1px solid var(--border);border-left:5px solid var(--accent);border-radius:10px}
.brief .ghead{margin-bottom:.4rem}
.brief h3{margin:1.4rem 0 .5rem;font-family:var(--sans);font-size:1.02em;color:var(--accent)}
.brief p{margin:.5rem 0;line-height:1.85;font-size:.95em}
.brief ul{margin:.5rem 0 .5rem 1.2rem}
.brief li{margin:.35rem 0;line-height:1.8;font-size:.95em}
.brief .q{font-style:italic;color:var(--accent)}
.brief-note{margin-top:1.2rem;padding-top:.8rem;border-top:1px dashed var(--border);color:var(--text-soft);font-size:.85em;font-family:var(--sans)}
.brief-toc a{color:var(--accent);font-weight:700}
</style>
</head>
<body>
<div id="progress" aria-hidden="true"></div>
<div class="layout">
  <aside class="toc" aria-label="目录">
    <div class="toc-title">📖 目录（__RANGE__）</div>
    <div class="toc-pos">当前位置：<span id="cur-pos">—</span></div>
    <nav id="toc-list"><ul>
__TOC__
    </ul></nav>
    <p class="toc-foot">原文：zeno.org（1807 年版）<br>笔记：引擎框架 · 引文可点击回原文</p>
  </aside>
  <main>
    <header class="doc-head">
      <h1>__BOOK__（__RANGE__）</h1>
      <p class="doc-sub">左栏：德文原文 · 右栏：引擎框架读书笔记 · 引文“……”可点击跳回原文段落 · 试点验证整条链路</p>
    </header>
__SECTIONS__
    <footer style="margin-top:3rem;padding-top:1rem;border-top:1px solid var(--border);color:var(--text-soft);font-size:.85rem">
      <p>生成：原文抓取 → 提取（页码锚点）→ 引擎笔记 → 引文锚点 → 逐条对拍校验。下一章按同链路推进。</p>
    </footer>
  </main>
</div>
<button id="theme-btn" class="fn-btn" type="button" title="切换明暗主题">🌓</button>
<button id="rh-toggle" class="fn-btn" type="button" title="开关辅助阅读（首句/难句/末句硬译卡）">📖</button>
<button id="top-btn" type="button" title="回到顶部">↑</button>
<button id="toc-open-btn" type="button" title="打开目录">☰</button>
<button id="bm-toggle" class="fn-btn" type="button" title="书签">🔖</button>
<aside id="bm-wrap" aria-label="书签">
  <div id="bm-head">
    <span id="bm-title">🔖 书签</span>
    <button id="bm-clear" type="button" title="清空全部书签">清空</button>
  </div>
  <ul id="bm-list"></ul>
</aside>
<script>
(function(){
  'use strict';
  var tocAside=document.querySelector('aside.toc');
  var links=Array.prototype.slice.call(document.querySelectorAll('#toc-list a'));
  var tocMap={};
  links.forEach(function(a){tocMap[a.getAttribute('href')]=a;});
  var curPos=document.getElementById('cur-pos');
  function offsetTopIn(el,container){var top=0,node=el;while(node&&node!==container){top+=node.offsetTop;node=node.offsetParent;}return top;}
  /* 当前小节块：视口上沿所在/最近的块；完全滑出视口时取下一个小节（章节边界/无段落块） */
  function currentBlock(){
    var y=window.scrollY, bs=document.querySelectorAll('.block'), cur=null;
    for(var i=0;i<bs.length;i++){
      var r=bs[i].getBoundingClientRect();
      if(r.top+window.scrollY<=y){cur=bs[i];}else{break;}
    }
    if(cur){
      if(cur.getBoundingClientRect().bottom<-20){
        var arr=Array.prototype.slice.call(bs),idx=arr.indexOf(cur);
        if(idx+1<arr.length){cur=arr[idx+1];}
      }
    }else if(bs.length){cur=bs[0];}
    return cur;
  }
  /* 块内当前段落（仅用于段号显示） */
  function currentParaIn(blk){
    var y=window.scrollY+40,cur=null,ps=blk.querySelectorAll('p.op');
    for(var i=0;i<ps.length;i++){
      var t=ps[i].getBoundingClientRect().top+window.scrollY;
      if(t<=y){cur=ps[i];}else{break;}
    }
    return cur;
  }
  var tick=false;
  function spy(){
    tick=false;
    links.forEach(function(a){a.classList.remove('active');});
    var blk=currentBlock();
    if(!blk){return;}
    var p=currentParaIn(blk);
    if(p){
      var m=/c(\d+)-p(\d+)/.exec(p.id);
      if(m){curPos.textContent=m[1]+'.'+m[2];}
    }
    /* 高亮当前小节 + 所在章 */
    var activeEls=[];
    if(blk.id){var b=tocMap['#'+blk.id];if(b){activeEls.push(b);}}
    var ch=blk.closest?blk.closest('section.gestalt'):null;
    if(ch&&ch.id){var c=tocMap['#'+ch.id];if(c){activeEls.push(c);}}
    activeEls.forEach(function(a){a.classList.add('active');});
    /* 侧栏滚动以当前小节为准 */
    if(activeEls.length){
      var first=activeEls[0];
      var t=offsetTopIn(first,tocAside);
      if(t<tocAside.scrollTop||t>tocAside.scrollTop+tocAside.clientHeight-60){
        tocAside.scrollTop=Math.max(0,t-tocAside.clientHeight/2);
      }
    }
  }
  window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(spy);}},{passive:true});
  window.addEventListener('resize',spy);
  spy();
  var rootEl=document.documentElement,themeBtn=document.getElementById('theme-btn');
  var saved=null;try{saved=localStorage.getItem('hegel-theme');}catch(e){}
  if(saved)rootEl.setAttribute('data-theme',saved);
  else if(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)rootEl.setAttribute('data-theme','dark');
  themeBtn.addEventListener('click',function(){var next=rootEl.getAttribute('data-theme')==='dark'?'light':'dark';rootEl.setAttribute('data-theme',next);try{localStorage.setItem('hegel-theme',next);}catch(e){}});
  var bar=document.getElementById('progress'),topBtn=document.getElementById('top-btn');
  function onScroll(){var h=document.documentElement,max=h.scrollHeight-h.clientHeight;bar.style.width=(max>0?(h.scrollTop/max)*100:0)+'%';if(h.scrollTop>500)topBtn.classList.add('show');else topBtn.classList.remove('show');}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  topBtn.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  var openBtn=document.getElementById('toc-open-btn');
  openBtn.addEventListener('click',function(){tocAside.classList.add('open');});
  links.forEach(function(a){a.addEventListener('click',function(){if(window.innerWidth<=1000)tocAside.classList.remove('open');});});
  /* ── 书签：段落级定位，localStorage 持久化 ── */
  var bmWrap=document.getElementById('bm-wrap'),bmList=document.getElementById('bm-list'),
      bmToggle=document.getElementById('bm-toggle'),bmClear=document.getElementById('bm-clear');
  var BM_KEY='hegel-bookmarks-'+location.pathname.split('/').pop();
  var bms=[];
  try{bms=JSON.parse(localStorage.getItem(BM_KEY)||'[]');}catch(e){bms=[];}
  function bmStore(){try{localStorage.setItem(BM_KEY,JSON.stringify(bms));}catch(e){}}
  function bmGo(no){
    var el=document.querySelector('p.op[data-bmno="'+no+'"]');
    if(!el){ /* 兼容旧定位：按编号找 */
      var ps=document.querySelectorAll('p.op');
      for(var i=0;i<ps.length;i++){
        var t=ps[i].querySelector('.pnum');
        if(t&&t.textContent.trim()===no){el=ps[i];break;}
      }
    }
    if(el){el.scrollIntoView({behavior:'smooth',block:'center'});highlightPara(el);}
  }
  function highlightPara(el){
    el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');
  }
  function bmText(el){
    var t=el.textContent.replace(/\s+/g,' ').trim();
    var idx=t.indexOf('＋');
    if(idx>-1)t=t.slice(0,idx);
    return t.slice(0,42);
  }
  function renderBm(){
    bmList.innerHTML='';
    bms.forEach(function(b,ix){
      var li=document.createElement('li');
      li.setAttribute('data-no',b.no);
      var noEl=document.createElement('span');noEl.className='bm-no';noEl.textContent=b.no;
      var tx=document.createElement('span');tx.className='bm-txt';tx.textContent=b.txt;
      var del=document.createElement('button');del.className='bm-del';del.type='button';del.title='删除书签';del.textContent='✕';
      del.addEventListener('click',function(e){e.stopPropagation();bms.splice(ix,1);bmStore();renderBm();});
      li.appendChild(noEl);li.appendChild(tx);li.appendChild(del);
      li.addEventListener('click',function(){bmGo(b.no);});
      bmList.appendChild(li);
    });
    /* 段落按钮状态：已收藏的显示高亮 */
    document.querySelectorAll('.bm-add').forEach(function(btn){
      var no=btn.getAttribute('data-bm');
      btn.classList.toggle('bm-added',bms.some(function(b){return b.no===no;}));
      btn.textContent=bms.some(function(b){return b.no===no;})?'★':'＋';
    });
  }
  bmToggle.addEventListener('click',function(){
    var open=!bmWrap.classList.contains('open');
    bmWrap.classList.toggle('open',open);
    document.body.classList.toggle('bm-open',open);
    bmToggle.textContent=open?'✕':'🔖';
    bmToggle.title=open?'收起书签':'书签';
  });
  bmClear.addEventListener('click',function(){if(bms.length&&confirm('清空全部书签？')){bms=[];bmStore();renderBm();}});
  document.addEventListener('click',function(e){
    var btn=e.target.closest?e.target.closest('.bm-add'):null;
    if(!btn)return;
    var no=btn.getAttribute('data-bm');
    var ix=bms.findIndex(function(b){return b.no===no;});
    var p=btn.closest('p.op');
    if(ix>-1){bms.splice(ix,1);}
    else{bms.push({no:no,txt:p?bmText(p):''});}
    bmStore();renderBm();
  });
  /* 滚动时高亮当前书签项 */
  var bmTick=false;
  window.addEventListener('scroll',function(){
    if(bmTick)return;bmTick=true;
    requestAnimationFrame(function(){
      bmTick=false;
      var y=window.scrollY+120,cur=null,ps=document.querySelectorAll('p.op');
      for(var i=0;i<ps.length;i++){if(ps[i].getBoundingClientRect().top+window.scrollY<=y)cur=ps[i];else break;}
      if(!cur)return;
      var pn=cur.querySelector('.pnum');
      var no=pn?pn.textContent.trim():'';
      bmList.querySelectorAll('li').forEach(function(li){li.classList.toggle('cur',li.getAttribute('data-no')===no);});
    });
  },{passive:true});
  renderBm();
  /* ── 辅助阅读开关（rh-note 显隐，localStorage 持久化）── */
  var rhToggle=document.getElementById('rh-toggle');
  var RH_KEY='hegel-no-rh';
  var noRh=false;
  try{noRh=localStorage.getItem(RH_KEY)==='1';}catch(e){}
  function applyRh(){
    document.body.classList.toggle('no-rh',noRh);
    rhToggle.classList.toggle('off',noRh);
    rhToggle.title=noRh?'开启辅助阅读（当前：关）':'关闭辅助阅读（当前：开）';
  }
  rhToggle.addEventListener('click',function(){noRh=!noRh;try{localStorage.setItem(RH_KEY,noRh?'1':'0');}catch(e){}applyRh();});
  applyRh();
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
