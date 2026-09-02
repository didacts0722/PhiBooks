# -*- coding: utf-8 -*-
"""
术语表差异审计（原构建脚本，2026-08-27 起**不再写主表**）：
主表 viewpoints/glossary/黑格尔.json 已综合两个笔记（现象学 ch1-8 + 小逻辑 四编）
并固定——改术语请直接编辑该 json，validate_glossary.py 校验。
本脚本只扫描两个笔记的行内德文注释，与主表比对，报告：
  - 主表缺失（笔记有、主表无 → 考虑补录）
  - 主表多余（主表有、笔记扫不到 → 结构性补充词，正常）
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
NOTES_PHENO = ROOT / "项目/现象学/notes"
NOTES_LP = ROOT / "项目/小逻辑/notes"
MASTER = ROOT / "viewpoints" / "glossary" / "黑格尔.json"

# 行内注释：中文/标点 + （德文）
PAIR_RE = re.compile(
    r"([\u4e00-\u9fffA-Za-z0-9*＊「」·+＝=…—-]{0,24}?)[（(]([A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\s\-·]*?)[）)]"
)

# 结构性核心词补充（笔记里可能只写中文未带德文括号的）
SUPPLEMENT = [
    ("Begriff", "概念"), ("Urteil", "判断"), ("Schluß", "推论"),
    ("Negativität", "否定性"), ("absolute Negativität", "绝对否定性"),
    ("Aufheben", "扬弃"), ("Geist", "精神"), ("Vernunft", "理性"),
    ("Verstand", "知性"), ("Bewußtsein", "意识"), ("Selbstbewußtsein", "自我意识"),
    ("Wesen", "本质"), ("Wahrheit", "真理"), ("Erscheinung", "现象"),
    ("Schein", "假象"), ("Anerkennung", "承认"), ("Sittlichkeit", "伦理"),
    ("Bildung", "教化"), ("Ding", "物"), ("Sache selbst", "事情本身"),
    ("Fürsichsein", "自为存在"), ("Ansichsein", "自在存在"),
    ("Anundfürsichsein", "自在自为存在"), ("Unendlichkeit", "无限性"),
    ("Kategorie", "范畴"), ("Gesetz", "规律"), ("Kraft", "力"),
    ("Leben", "生命"), ("Begierde", "欲望"), ("Herr", "主人"), ("Knecht", "奴仆"),
    ("Arbeit", "劳动"), ("Furcht", "恐惧"), ("Tod", "死亡"),
    ("Moralität", "道德"), ("Gewissen", "良心"), ("schöne Seele", "优美灵魂"),
    ("Verzeihung", "宽恕"), ("Religion", "宗教"), ("Kunstreligion", "艺术宗教"),
    ("offenbare Religion", "天启宗教"), ("Naturreligion", "自然宗教"),
    ("absolutes Wissen", "绝对知识"), ("Er-Innerung", "回忆"),
    ("Zeit", "时间"), ("Vorstellung", "表象"), ("Weltlauf", "世界进程"),
    ("Tugend", "德行"), ("Gesetz des Herzens", "本心的规律"),
    ("Furie des Verschwindens", "消失的狂怒"), ("schlechte Unendlichkeit", "坏的无限性"),
    # 2026-08-26 高频审计补充（译法按笔记用法）
    ("Wirklichkeit", "现实性"), ("Sprache", "语言"), ("Wissen", "知识"), ("Welt", "世界"),
    ("Form", "形式"), ("Bewegung", "运动"), ("Unterschied", "差别"), ("Gestalt", "形态"),
    ("Dasein", "定在"), ("Element", "元素"), ("Bedeutung", "意义"), ("Freiheit", "自由"),
    ("Denken", "思维"), ("Substanz", "实体"), ("Versöhnung", "和解"), ("Gott", "上帝（神）"),
    ("Reich", "王国"), ("Realität", "实在性"), ("Moment", "环节"), ("Glückseligkeit", "幸福"),
    ("Einheit", "统一性"), ("Natur", "自然"), ("Subjekt", "主体"), ("Person", "人格"),
    ("Glaube", "信仰"), ("Einsicht", "识见"), ("Wille", "意志"), ("Anschauung", "直观"),
    ("Pflicht", "义务"), ("Handlung", "行动"), ("Volk", "民族"), ("Kunst", "艺术"),
    ("Gemeinde", "团契"), ("Selbst", "自我"), ("Jenseits", "彼岸"), ("Allgemeinheit", "普遍性"),
    ("Einzelheit", "个别性"), ("Besonderheit", "特殊性"), ("Vermittlung", "中介"),
    ("Unmittelbarkeit", "直接性"), ("Maßstab", "尺度"), ("Selbständigkeit", "独立性"),
    ("Wort", "言词"), ("Kunstwerk", "艺术作品"), ("Lethe", "忘川"), ("Jetzt", "现在"),
    ("Hier", "这里"), ("Befriedigung", "满足"),
    # 2026-08-26 四条选词标准补充：①逻辑三一体/存在论 ②德语形态（分词/名词化）
    # ③引擎推演词 ④历史文化强相关
    ("Sein", "存在"), ("Nichts", "虚无"), ("Werden", "变易"), ("Anderssein", "他在"),
    ("das Seiende", "存在者"), ("das Allgemeine", "普遍者"), ("das Einzelne", "个别者"),
    ("das Andere", "他者"), ("das Lebendige", "有生命者"), ("das Übersinnliche", "超感官者"),
    ("das Wesentliche", "本质者"), ("das Unwesentliche", "非本质者"), ("das Absolute", "绝对者"),
    ("das Unendliche", "无限者"), ("das Endliche", "有限者"), ("das Wirkliche", "现实者"),
    ("das Sittliche", "伦理者"), ("das Schöne", "美（美者）"), ("das Aufgehobene", "被扬弃者"),
    ("Widerspruch", "矛盾"), ("Entzweiung", "分裂"), ("Identität", "同一性"),
    ("Negation", "否定"), ("Individualität", "个体性"), ("Reflexion", "反思"),
    ("Bestimmung", "规定"), ("Übergang", "过渡"), ("Entwicklung", "发展"),
    ("Grund", "根据"), ("Bedingung", "条件"), ("Zweck", "目的"), ("Verhältnis", "关系"),
    ("Meinen", "意谓"), ("Aufzeigen", "指认"), ("Setzen", "设定"),
    ("Stoizismus", "斯多亚主义"), ("Skeptizismus", "怀疑主义"),
    ("unglückliche Bewußtsein", "苦恼意识"), ("Aufklärung", "启蒙"), ("Recht", "法权"),
    ("Weltgeist", "世界精神"), ("Antigone", "安提戈涅"), ("Ödipus", "俄狄浦斯"),
    ("Sphinx", "斯芬克斯"), ("Orakel", "神谕"), ("Erinnyen", "复仇女神"),
    ("Reformation", "宗教改革"), ("Judentum", "犹太民族"), ("Christentum", "基督教"),
    ("Homer", "荷马"), ("Sokrates", "苏格拉底"), ("Faust", "浮士德"),
    ("Bacchus", "巴克科斯（酒神）"), ("Ceres", "刻瑞斯（谷神）"),
    ("das Spekulative", "思辨者（思辨的东西）"),
]

TEXT_FIELDS = ("bestimmung", "explain", "diag", "uebergang")

STOPWORDS = {
    "a", "auch", "und", "ist", "als", "das", "die", "der", "den", "dem", "sich",
    "nicht", "ein", "eine", "eines", "einer", "in", "im", "mit", "von", "zu",
    "für", "auf", "an", "aus", "bei", "des", "wie", "so", "es", "sie", "er",
    "ich", "wir", "ihr", "sein", "ihre", "diese", "dieser", "dieses", "dass",
    "was", "wenn", "dann", "nur", "noch", "schon", "immer", "ob", "oder",
    "aber", "weil", "indem", "welcher", "welche", "welches", "werden", "wird",
    "haben", "hat", "sind", "um", "über", "unter", "nach", "vor", "bis",
}

# 人工修正：自动抽取的 zh 若是语境片段，这里给干净的译法（key=小写术语）
MANUAL_FIX = {
    "schuld": "罪责",
    "dialektisch": "解构的力",
    "spekulativ": "思辨的（思维中推演）",
    "unbedingt-allgemeine": "无条件共相",
    "sollizitieren": "相互激励",
    "bildet": "塑造（陶铸）",
    "gewißheit": "确定性",
    "erfahrung": "经验",
    "sache": "事情",
    "charakter": "性格",
    "hervorbringen": "产生",
    "aufgehen": "升起",
    "wahrnehmung": "知觉",
    "kultus": "崇拜",
    "chor": "歌队",
    "pathos": "情致",
    "außer sich": "在自身之外",
    "angeschaut": "被直观",
    "gewesensein": "曾在",
    "abfallen": "背离",
    "an sich": "自在",
    "entäußerung": "自我外化",
    "zweckbegriff": "目的概念",
    "dingheit": "物性",
    "gnade": "恩典",
    "wort der versöhnung": "和解之词",
    "absolute dialektische unruhe": "绝对的辩证不安",
    "musikalisches denken": "音乐式的思想",
    "mysterien von eleusis": "厄琉息斯秘仪",
    "mitleid": "怜悯",
    "gelächter": "笑",
    "dialektik": "解构",
    "spekulation": "思辨",
    "schicksal": "命运",
    "leere worte": "空话",
    "fremder anstoß": "外在的推动",
    "menschliches gesetz": "人的规律",
    "göttliches gesetz": "神的规律",
    "das wort der versöhnung": "和解之词",
    "hymnus": "赞歌",
    "sänger": "歌者",
    "klang": "声响",
    "tonlose gestalt": "无音调的形态",
    "werkmeister": "工匠",
    "sohn": "圣子",
    "das selbst ein ding ist": "自我=物",
    "leerer idealismus": "空洞的唯心主义",
    "bewußtlose faselei": "无意识的胡言乱语",
}

# 替代释义（alt）：主译法 zh 之外，对某些语境更贴切的补充译法（key=小写术语）。
# 输出时附在条目 "alt" 字段，渲染/校验均不依赖它。
ALT_FIX = {
    "fürsichsein": "为自存在（Für-sich-sein：为着自己而存在；自为存在有时更宜释作「为自存在」——强调「为（für）自己」的指向性，而不是「自己作为」的自足性）",
}


def norm_term(t: str) -> str:
    t = t.strip(" *·-")
    return re.sub(r"\s+", " ", t)


def collect_texts(data: dict):
    texts = []
    for g in data.get("gestalten", []):
        for f in TEXT_FIELDS:
            v = g.get(f)
            if v:
                texts.append(v)
        for b in g.get("bewegung", []):
            texts.append(b[3] if len(b) > 3 else "")
            if len(b) > 4 and isinstance(b[4], list):
                for s in b[4]:
                    texts.append(s.get("content", ""))
            if len(b) > 5 and isinstance(b[5], dict):
                dg = b[5]
                texts.append(dg.get("title", ""))
                for k in ("left", "right"):
                    node = dg.get(k) or {}
                    texts.append(node.get("label", ""))
                    texts.append(node.get("sub", ""))
                    texts.extend(node.get("points", []))
    return [t for t in texts if t]


def main():
    # ── 1) 主表现状 ──
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    have = {e["term"].lower(): e for e in master.get("terms", [])}
    print(f"[主表] {master.get('philosopher','')} 共 {len(have)} 条"
          f"（已固定：{master.get('updated','')}；不再自动重建）")

    # ── 2) 扫描两个笔记的行内术语 ──
    combined = defaultdict(Counter)   # key -> 拼写计数
    src = defaultdict(set)            # key -> {作品}
    zh_first = {}

    def scan_file(path: Path, work: str):
        if not path.exists():
            return
        data = json.loads(path.read_text(encoding="utf-8"))
        for t in collect_texts(data):
            for m in PAIR_RE.finditer(t):
                zh = m.group(1).strip(" *＊「」·")
                term = norm_term(m.group(2))
                if not term or not re.search(r"[A-Za-z]", term):
                    continue
                if re.fullmatch(r"p\.?\d+[–\-–]?\d*", term):
                    continue
                key = term.lower()
                spell[key][term] += 1
                if key in STOPWORDS or len(term) < 3 or len(term) > 60 \
                        or term.count(" ") > 5:
                    continue
                zh = re.sub(r"\*\*?|[＊「」]", "", zh).strip()
                if not zh or len(zh) > 14 or any(c in zh for c in "（）：;'"):
                    continue
                if zh[0] in "是而但就并这那" or any(w in zh for w in
                        ("我们", "他们", "这里", "就是", "这是", "那是", "于是", "因此", "观察理性")):
                    continue
                combined[key] += Counter({term: 1})
                src[key].add(work)
                if key not in zh_first:
                    zh_first[key] = zh

    spell = defaultdict(Counter)
    for n in range(1, 9):
        scan_file(NOTES_PHENO / f"ch{n}.json", "精神现象学")
    for f in ("sein", "essence", "begriff", "vorbegriff"):
        scan_file(NOTES_LP / f"{f}.json", "小逻辑")

    # ── 3) 差异报告 ──
    missing = {k: (max(combined[k].values()), src[k], zh_first[k])
               for k in combined if k not in have}
    print(f"[扫描] 两笔记行内术语 {len(combined)} 个 | 主表缺失 {len(missing)} 个"
          f"（含语境短语，仅核心词值得补录）")
    for k in sorted(missing, key=lambda x: -missing[x][0]):
        print(f"  ✗ {k:<36} ×{missing[k][0]}  {('/'.join(sorted(missing[k][1]))):<6} 例:{missing[k][2][:12]}")
    # 主表有、笔记未扫到（结构性补充词，正常）
    extra = [k for k in have if k not in combined]
    print(f"[主表] 结构性补充/未在行内注释出现: {len(extra)} 条（正常，无需处理）")
    print("提示：补录术语请直接编辑 viewpoints/glossary/黑格尔.json，然后 python validate_glossary.py")


if __name__ == "__main__":
    main()
