# -*- coding: utf-8 -*-
"""
从提取数据生成两本书的【实际目录】（数据驱动：标题/§区间/页码区间均取自原文提取结果）。
输出：docs/黑格尔哲学引擎_实际目录.md
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs" / "黑格尔哲学引擎_实际目录.md"

ENZ_IDX = ROOT / "原文" / "黑格尔" / "Enzyklopädie_Logik" / "extracted" / "enzyklopaedie_logik_index.json"
PHENO_IDX = ROOT / "原文" / "黑格尔" / "Phänomenologie_des_Geistes" / "extracted" / "phenomenologie_index.json"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def secs_of(page):
    out = []
    for it in page["items"]:
        if it["type"] == "h5":
            m = re.match(r"§\s*(\d+)", it["text"])
            if m:
                out.append(int(m.group(1)))
    return out


def page_range(page):
    nums = [it["page"] for it in page["items"] if it.get("page")]
    if not nums:
        return None
    return (min(nums), max(nums))


def sec_range(page):
    s = secs_of(page)
    return (s[0], s[-1]) if s else None


def fmt_range(r):
    return f"§{r[0]}–{r[1]}" if r and r[0] != r[1] else (f"§{r[0]}" if r else "")


def main():
    enz = load(ENZ_IDX)
    pheno = load(PHENO_IDX)
    by_file = {p["file"]: p for p in enz}
    pby_file = {p["file"]: p for p in pheno}

    lines = []
    lines.append("# 黑格尔哲学引擎 · 实际目录（取自 zeno.org 原文）\n")
    lines.append("> 标题、§ 区间、页码区间均由原文页面提取生成，非凭记忆。\n")

    # ============ 精神现象学 ============
    lines.append("## 一、精神现象学（Phänomenologie des Geistes, 1807）\n")
    lines.append("| 结构 | 标题（德文原文） | 页码区间 |\n|---|---|---|")

    def prow(level, cn, fname):
        p = pby_file.get(fname)
        if not p:
            return
        title = ""
        for it in p["items"]:
            if it["type"] in ("h4", "h5"):
                title = it["text"]
                break
        if not title and p["items"]:
            title = p["items"][0]["text"]
        r = page_range(p)
        rng = f"[{r[0]}–{r[1]}]" if r else ""
        indent = "  " * level
        lines.append(f"| {indent}{cn} | {title} | {rng} |")

    prow(0, "序言", "Vorrede.html")
    prow(0, "导言", "Einleitung.html")
    prow(1, "A. 意识", "A._Bewußtsein.html")
    prow(2, "I. 感性确定性；这一个和意谓", "I._Die_sinnliche_Gewißheit_oder_das_Diese_und_das_Meinen.html")
    prow(2, "II. 知觉；事物和幻觉", "II._Die_Wahrnehmung_oder_das_Ding_und_die_Täuschung.html")
    prow(2, "III. 力和知性；现象和超感官世界", "III._Kraft_und_Verstand_Erscheinung_und_übersinnliche_Welt.html")
    prow(1, "B. 自我意识", "B._Selbstbewußtsein.html")
    prow(2, "IV. 自我意识自身确定性的真理性", "IV._Die_Wahrheit_der_Gewißheit_seiner_selbst.html")
    prow(3, "A. 自我意识的独立与依赖；主人与奴隶", "A._Selbständigkeit_und_Unselbständigkeit_des_Selbstbewußtseins_Herrschaft_und_Knechtschaft.html")
    prow(3, "B. 自我意识的自由；斯多葛主义、怀疑主义和苦恼意识", "B._Freiheit_des_Selbstbewußtseins_Stoizismus_Skeptizismus_und_das_unglückliche_Bewußtsein.html")
    prow(1, "C. 理性", "C._AA_Vernunft.html")
    prow(2, "V. 理性的确定性和真理性", "V._Gewißheit_und_Wahrheit_der_Vernunft.html")
    prow(3, "A. 观察的理性", "A._Beobachtende_Vernunft.html")
    prow(4, "a. 对自然的观察", "a._Beobachtung_der_Natur.html")
    prow(4, "b. 对自我意识的观察；逻辑规律与心理学规律", "b._Die_Beobachtung_des_Selbstbewußtseins_in_seiner_Reinheit_und_seiner_Beziehung_auf_äußere_Wirklichkeit_logische_und_psychologische_Gesetze.html")
    prow(4, "c. 面相学与头盖骨相学", "c._Beobachtung_der_Beziehung_des_Selbstbewußtseins_auf_seine_unmittelbare_Wirklichkeit_Physiognomik_und_Schädellehre.html")
    prow(3, "B. 理性的自我意识通过其自身的活动而实现", "B._Die_Verwirklichung_des_vernünftigen_Selbstbewußtseins_durch_sich_selbst.html")
    prow(4, "a. 快乐与必然性", "a._Die_Lust_und_die_Notwendigkeit.html")
    prow(4, "b. 本心的规律和自大狂", "b._Das_Gesetz_des_Herzens_und_der_Wahnsinn_des_Eigendünkels.html")
    prow(4, "c. 德行与世界进程", "c._Die_Tugend_und_der_Weltlauf.html")
    prow(3, "C. 自在自为地实在的个体性", "C._Die_Individualität_welche_sich_an_und_für_sich_selbst_reell_ist.html")
    prow(4, "a. 精神动物的王国和欺骗；事情自身", "a._Das_geistige_Tierreich_und_der_Betrug_oder_die_Sache_selbst.html")
    prow(4, "b. 立法的理性", "b._Die_gesetzgebende_Vernunft.html")
    prow(4, "c. 审核法律的理性", "c._Gesetzprüfende_Vernunft.html")
    prow(1, "D. 精神", "C._BB_Der_Geist.html")
    prow(2, "VI. 精神", "VI._Der_Geist.html")
    prow(3, "A. 真实的精神；伦理", "A._Der_wahre_Geist._Die_Sittlichkeit.html")
    prow(4, "a. 伦理世界：人的规律与神的规律，男人与女人", "a._Die_sittliche_Welt._Das_menschliche_und_göttliche_Gesetz_der_Mann_und_das_Weib.html")
    prow(4, "b. 伦理行为：人的规律与神的规律，罪责与命运", "b._Die_sittliche_Handlung._Das_menschliche_und_göttliche_Wissen_die_Schuld_und_das_Schicksal.html")
    prow(4, "c. 法权状态", "c._Der_Rechtszustand.html")
    prow(3, "B. 自身异化了的精神；教化", "B._Der_sich_entfremdete_Geist._Die_Bildung.html")
    prow(4, "I. 异化了的精神的世界", "I._Die_Welt_des_sich_entfremdeten_Geistes.html")
    prow(5, "a. 教化及其现实性王国", "a._Die_Bildung_und_ihr_Reich_der_Wirklichkeit.html")
    prow(5, "b. 信仰与纯粹识见", "b._Der_Glaube_und_die_reine_Einsicht.html")
    prow(4, "II. 启蒙", "II._Die_Aufklärung.html")
    prow(5, "a. 启蒙与迷信的斗争", "a._Der_Kampf_der_Aufklärung_mit_dem_Aberglauben.html")
    prow(5, "b. 启蒙的真理", "b._Die_Wahrheit_der_Aufklärung.html")
    prow(4, "III. 绝对自由与恐怖", "III._Die_absolute_Freiheit_und_der_Schrecken.html")
    prow(3, "C. 对其自身具有确定性的精神；道德", "C._Der_seiner_selbst_gewisse_Geist._Die_Moralität.html")
    prow(4, "a. 道德世界观", "a._Die_moralische_Weltanschauung.html")
    prow(4, "b. 倒置", "b._Die_Verstellung.html")
    prow(4, "c. 良心；优美灵魂、恶及其宽恕", "c._Das_Gewissen._Die_schöne_Seele_das_Böse_und_seine_Verzeihung.html")
    prow(1, "E. 宗教", "C._CC_Die_Religion.html")
    prow(2, "VII. 宗教", "VII._Die_Religion.html")
    prow(3, "A. 自然宗教", "A._Die_natürliche_Religion.html")
    prow(4, "a. 光明本质", "a._Das_Lichtwesen.html")
    prow(4, "b. 植物与动物", "b._Die_Pflanze_und_das_Tier.html")
    prow(4, "c. 工匠", "c._Der_Werkmeister.html")
    prow(3, "B. 艺术宗教", "B._Die_Kunstreligion.html")
    prow(4, "a. 抽象的艺术作品", "a._Das_abstrakte_Kunstwerk.html")
    prow(4, "b. 有生命的艺术作品", "b._Das_lebendige_Kunstwerk.html")
    prow(4, "c. 精神的艺术作品", "c._Das_geistige_Kunstwerk.html")
    prow(3, "C. 天启宗教", "C._Die_offenbare_Religion.html")
    prow(1, "F. 绝对知识", "C._DD_Das_absolute_Wissen.html")
    prow(2, "VIII. 绝对知识", "VIII._Das_absolute_Wissen.html")

    lines.append("\n---\n")

    # ============ 百科全书·逻辑学 ============
    lines.append("## 二、逻辑学（小逻辑）（Enzyklopädie I: Die Wissenschaft der Logik, 1830）\n")
    lines.append("| 结构 | 标题（德文原文） | §区间 |\n|---|---|---|")

    def row(level, cn, fname, fmt=None):
        p = by_file.get(fname)
        if not p:
            return
        title = ""
        for it in p["items"]:
            if it["type"] == "h4":
                title = it["text"]
                break
        if not title and p["items"]:
            title = p["items"][0]["text"]
        r = sec_range(p)
        rng = fmt_range(r) if fmt is None else fmt
        indent = "  " * level
        lines.append(f"| {indent}{cn} | {title} | {rng} |")

    row(0, "（卷首）", "Vorreden.html")
    row(1, "· 第一版序言", "Vorrede_zur_ersten_Ausgabe.html")
    row(1, "· 第二版序言", "Vorrede_zur_zweiten_Ausgabe.html")
    row(1, "· 第三版序言", "Vorwort_zur_dritten_Ausgabe.html")
    row(0, "导言", "Einleitung.html")
    row(0, "第一编 逻辑学", "Erster_Teil._Die_Wissenschaft_der_Logik..html")
    row(1, "前概念（Vorbegriff）", "Vorbegriff.html")
    row(2, "· 逻辑学的较确切概念与划分", "Näherer_Begriff_und_Einteilung_der_Logik.html")
    row(2, "· A. 思想对客观性的第一种态度：形而上学", "A._Erste_Stellung_des_Gedankens_zur_Objektivität._Metaphysik.html")
    row(2, "· B. 第二种态度：经验主义与批判哲学", "B._Zweite_Stellung_des_Gedankens_zur_Objektivität.html")
    row(3, "· I. 经验主义", "I._Empirismus.html")
    row(3, "· II. 批判哲学", "II._Kritische_Philosophie.html")
    row(2, "· C. 第三种态度：直接知识", "C._Dritte_Stellung_des_Gedankens_zur_Objektivität._Das_unmittelbare_Wissen.html")
    row(1, "第一篇 存在论", "1._Abteilung_Die_Lehre_vom_Sein.html")
    row(2, "A. 质", "A._Qualität.html")
    row(3, "a. 存在", "a._Sein.html")
    row(3, "b. 定在", "b._Dasein.html")
    row(3, "c. 自为存在", "c._Fürsichsein.html")
    row(2, "B. 量", "B._Quantität.html")
    row(3, "a. 纯量", "a._Die_reine_Quantität.html")
    row(3, "b. 定量", "b._Das_Quantum.html")
    row(3, "c. 程度", "c._Der_Grad.html")
    row(2, "C. 尺度", "C._Das_Maß.html")
    row(1, "第二篇 本质论", "2._Abteilung_Die_Lehre_vom_Wesen.html")
    row(2, "A. 本质作为实存的根据", "A._Das_Wesen_als_Grund_der_Existenz.html")
    row(3, "a. 纯反思规定", "a._Die_reinen_Reflexionsbestimmungen.html")
    row(4, "aa. 同一", "aa._Identität.html")
    row(4, "bb. 差别", "bb._Der_Unterschied.html")
    row(4, "cc. 根据", "cc._Der_Grund.html")
    row(3, "b. 实存", "b._Die_Existenz.html")
    row(3, "c. 物", "c._Das_Ding.html")
    row(2, "B. 现象", "B._Die_Erscheinung.html")
    row(3, "a. 现象界", "a._Die_Welt_der_Erscheinung.html")
    row(3, "b. 内容与形式", "b._Inhalt_und_Form.html")
    row(3, "c. 关系", "c._Das_Verhältnis.html")
    row(2, "C. 现实", "C._Die_Wirklichkeit.html")
    row(3, "a. 实体关系", "a._Substantialitätsverhältnis.html")
    row(3, "b. 因果关系", "b._Kausalitätsverhältnis.html")
    row(3, "c. 相互作用", "c._Die_Wechselwirkung.html")
    row(1, "第三篇 概念论", "3._Abteilung_Die_Lehre_vom_Begriff.html")
    row(2, "A. 主观概念", "A._Der_subjektive_Begriff.html")
    row(3, "a. 概念本身", "a._Der_Begriff_als_solcher.html")
    row(3, "b. 判断", "b._Das_Urteil.html")
    row(4, "aa. 质的判断", "aa._Qualitatives_Urteil.html")
    row(4, "bb. 反思判断", "bb._Das_Reflexionsurteil.html")
    row(4, "cc. 必然判断", "cc._Urteil_der_Notwendigkeit.html")
    row(4, "dd. 概念判断", "dd._Das_Urteil_des_Begriffs.html")
    row(3, "c. 推论", "c._Der_Schluß.html")
    row(4, "aa. 质的推论", "aa._Qualitativer_Schluß.html")
    row(4, "bb. 反思推论", "bb._Reflexionsschluß.html")
    row(4, "cc. 必然推论", "cc._Schluß_der_Notwendigkeit.html")
    row(2, "B. 客体", "B._Das_Objekt.html")
    row(3, "a. 机械性", "a._Der_Mechanismus.html")
    row(3, "b. 化学性", "b._Der_Chemismus.html")
    row(3, "c. 目的性", "c._Teleologie.html")
    row(2, "C. 理念", "C._Die_Idee.html")
    row(3, "a. 生命", "a._Das_Leben.html")
    row(3, "b. 认识", "b._Das_Erkennen.html")
    row(4, "aa. 认识（理论理念）", "aa._Das_Erkennen.html")
    row(4, "bb. 意志（实践理念）", "bb._Das_Wollen.html")
    row(3, "c. 绝对理念", "c._Die_absolute_Idee.html")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成: {OUT}")


if __name__ == "__main__":
    main()
