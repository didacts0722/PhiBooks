# -*- coding: utf-8 -*-
"""生成附录 A：§257-360 逐 § 核心引文速查（补足 70%+ 覆盖），校验每条是原文 norm 子串"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")
import build_pheno_ch123 as P  # noqa: E402

idx = json.loads(Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))
sec_map = json.loads(Path("notes_recht/staat_sec_map.json").read_text(encoding="utf-8"))

# § -> 全部段落文本
sec_texts = {}
for pg in idx:
    cur = None
    mapped = sec_map.get(pg.get("file"))
    mi = 0
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            cur = int(m.group(1)) if m else cur
        elif it["type"] == "p":
            sec_use = mapped[mi] if mapped and mi < len(mapped) else cur
            if mapped:
                mi += 1
            if sec_use:
                sec_texts.setdefault(sec_use, []).append(it["text"])

# 每条引文：§ -> 德文引文（从原文逐字）
QUOTES = {
    262: "Die wirkliche Idee, der Geist, der sich selbst in die zwei ideellen Sphären seines Begriffs, die Familie und die bürgerliche Gesellschaft, als in seine Endlichkeit scheidet, um aus ihrer Idealität für sich unendlicher wirklicher Geist zu sein",
    263: "In diesen Sphären, in denen seine Momente, die Einzelheit und Besonderheit, ihre unmittelbare und reflektierte Realität haben, ist der Geist als ihre in sie scheinende objektive Allgemeinheit, als die Macht des Vernünftigen in der Notwendigkeit (§ 184), nämlich als die im Vorherigen betrachteten Institutionen",
    264: "Die Individuen der Menge, da sie selbst geistige Naturen und damit das gedoppelte Moment, nämlich das Extrem der für sich wissenden und wollenden Einzelheit und das Extrem der das Substantielle wissenden und wollenden Allgemeinheit in sich enthalten",
    265: "Diese Institutionen machen die Verfassung, d. i. die entwickelte und verwirklichte Vernünftigkeit, im Besonderen aus und sind darum die feste Basis des Staats sowie des Zutrauens und der Gesinnung der Individuen für denselben",
    266: "Aber der Geist ist nicht nur als diese Notwendigkeit und als ein Reich der Erscheinung, sondern als die Idealität derselben und als ihr Inneres sich objektiv und wirklich",
    267: "Die Notwendigkeit in der Idealität ist die Entwicklung der Idee innerhalb ihrer selbst; sie ist als subjektive Substantialität die politische Gesinnung, als objektive in Unterscheidung von jener der Organismus des Staats, der eigentlich politische Staat und seine Verfassung",
    268: "Die politische Gesinnung, der Patriotismus überhaupt, als die in Wahrheit stehende Gewißheit (bloß subjektive Gewißheit geht nicht aus der Wahrheit hervor und ist nur Meinung) und das zur Gewohnheit gewordene Wollen ist nur Resultat der im Staate bestehenden Institutionen",
    269: "Ihren besonders bestimmten Inhalt nimmt die Gesinnung aus den verschiedenen Seiten des Organismus des Staats. Dieser Organismus ist die Entwicklung der Idee zu ihren Unterschieden und zu deren objektiver Wirklichkeit",
    270: "Es ist hier der Ort, das Verhältnis des Staats zur Religion zu berühren, da in neueren Zeiten so oft wiederholt worden ist, daß die Religion die Grundlage des Staates sei",
    274: "Da der Geist nur als das wirklich ist, als was er sich weiß, und der Staat, als Geist eines Volkes, zugleich das alle seine Verhältnisse durchdringende Gesetz, die Sitte und das Bewußtsein seiner Individuen ist, so hängt die Verfassung eines bestimmten Volkes überhaupt von der Weise und Bildung des Selbstbewußtseins desselben ab",
    277: "Die besonderen Geschäfte und Wirksamkeiten des Staats sind als die wesentlichen Momente desselben ihm eigen und an die Individuen, durch welche sie gehandhabt und betätigt werden, nicht nach deren unmittelbarer Persönlichkeit, sondern nur nach ihren allgemeinen und objektiven Qualitäten geknüpft",
    281: "Beide Momente in ihrer ungetrennten Einheit, das letzte grundlose Selbst des Willens und die damit ebenso grundlose Existenz, als der Natur anheimgestellte Bestimmung, – diese Idee des von der Willkür Unbewegten macht die Majestät des Monarchen aus",
    282: "Aus der Souveränität des Monarchen fließt das Begnadigungsrecht der Verbrecher, denn ihr nur kommt die Verwirklichung der Macht des Geistes zu, das Geschehene ungeschehen zu machen",
    283: "Das zweite in der Fürstengewalt Enthaltene ist das Moment der Besonderheit oder des bestimmten Inhalts und der Subsumtion desselben unter das Allgemeine",
    284: "die eigentümliche Majestät des Monarchen, als die letzte entscheidende Subjektivität, ist aber über alle Verantwortlichkeit für die Regierungshandlungen erhoben",
    285: "Das dritte Moment der fürstlichen Gewalt betrifft das an und für sich Allgemeine, welches in subjektiver Rücksicht in dem Gewissen des Monarchen, in objektiver Rücksicht im Ganzen der Verfassung und in den Gesetzen besteht",
    286: "Die monarchische Verfassung zur erblichen, nach Primogenitur festbestimmten Thronfolge herausgearbeitet zu haben, so daß sie hiermit zum patriarchalischen Prinzip, von dem sie geschichtlich ausgegangen ist, aber in der höheren Bestimmung als die absolute Spitze eines organisch entwickelten Staats zurückgeführt worden, ist eines der späteren Resultate der Geschichte",
    288: "Die gemeinschaftlichen besonderen Interessen, die in die bürgerliche Gesellschaft fallen und außer dem an und für sich seienden Allgemeinen des Staats selbst liegen (§ 256), haben ihre Verwaltung in den Korporationen (§ 251) der Gemeinden und sonstiger Gewerbe und Stände und deren Obrigkeiten",
    289: "Die Festhaltung des allgemeinen Staatsinteresses und des Gesetzlichen in diesen besonderen Rechten und die Zurückführung derselben auf jenes erfordert eine Besorgung durch Abgeordnete der Regierungsgewalt, die exekutiven Staatsbeamten",
    290: "In dem Geschäfte der Regierung findet sich gleichfalls die Teilung der Arbeit (§ 198)",
    291: "Die Regierungsgeschäfte sind objektiver, für sich ihrer Substanz nach bereits entschiedener Natur (§ 287) und durch Individuen zu vollführen und zu verwirklichen",
    292: "diese Verknüpfung des Individuums und des Amtes, als zweier für sich gegeneinander immer zufälliger Seiten, kommt der fürstlichen als der entscheidenden und souveränen Staatsgewalt zu",
    293: "Die besonderen Staatsgeschäfte, welche die Monarchie den Behörden übergibt, machen einen Teil der objektiven Seite der dem Monarchen innewohnenden Souveränität aus",
    294: "Das Individuum, das durch den souveränen Akt (§ 292) einem amtlichen Berufe verknüpft ist, ist auf seine Pflichterfüllung, das Substantielle seines Verhältnisses, als Bedingung dieser Verknüpfung angewiesen",
    295: "Die Sicherung des Staats und der Regierten gegen den Mißbrauch der Gewalt von selten der Behörden und ihrer Beamten liegt einerseits unmittelbar in ihrer Hierarchie und Verantwortlichkeit, andererseits in der Berechtigung der Gemeinden, Korporationen",
    296: "Daß aber die Leidenschaftslosigkeit, Rechtlichkeit und Milde des Benehmens Sitte werde, hängt teils mit der direkten sittlichen und Gedankenbildung zusammen",
    297: "Die Mitglieder der Regierung und die Staatsbeamten machen den Hauptteil des Mittelstandes aus, in welchen die gebildete Intelligenz und das rechtliche Bewußtsein der Masse eines Volkes fällt",
    299: "Diese Gegenstände bestimmen sich in Beziehung auf die Individuen näher nach den zwei Seiten: α) was durch den Staat ihnen zugute kommt und sie zu genießen und β) was sie demselben zu leisten haben",
    300: "In der gesetzgebenden Gewalt als Totalität sind zunächst die zwei anderen Momente wirksam, das monarchische, als dem die höchste Entscheidung zukommt, – die Regierungsgewalt als das mit der konkreten Kenntnis und Übersicht des Ganzen in seinen vielfachen Seiten und den darin festgewordenen wirklichen Grundsätzen sowie mit der Kenntnis der Bedürfnisse der Staatsgewalt insbesondere beratende Moment, – endlich das ständische Element",
    301: "Das ständische Element hat die Bestimmung, daß die allgemeine Angelegenheit nicht nur an sich, sondern auch für sich, d. i. daß das Moment der subjektiven formellen Freiheit, das öffentliche Bewußtsein als empirische Allgemeinheit der Ansichten und Gedanken der Vielen, darin zur Existenz komme",
    302: "Als vermittelndes Organ betrachtet, stehen die Stände zwischen der Regierung überhaupt einerseits und dem in die besonderen Sphären und Individuen aufgelösten Volke andererseits",
    303: "in dem ständischen Elemente der gesetzgebenden Gewalt kommt der Privatstand zu einer politischen Bedeutung und Wirksamkeit",
    304: "Den in den früheren Sphären bereits vorhandenen Unterschied der Stände enthält das politisch-ständische Element zugleich in seiner eigenen Bestimmung",
    305: "Der eine der Stände der bürgerlichen Gesellschaft enthält das Prinzip, das für sich fähig ist, zu dieser politischen Beziehung konstituiert zu werden, der Stand der natürlichen Sittlichkeit nämlich, der das Familienleben und, in Rücksicht der Subsistenz, den Grundbesitz zu seiner Basis, somit in Rücksicht seiner Besonderheit ein auf sich beruhendes Wollen und die Naturbestimmung, welche das fürstliche Element in sich schließt, mit diesem gemein hat",
    306: "Für die politische Stellung und Bedeutung wird er näher konstituiert, insofern sein Vermögen ebenso unabhängig vom Staatsvermögen als von der Unsicherheit des Gewerbes, der Sucht des Gewinns und der Veränderlichkeit des Besitzes überhaupt – wie von der Gunst der Regierungsgewalt so von der Gunst der Menge – und selbst gegen die eigene Willkür dadurch festgestellt ist",
    307: "Das Recht dieses Teils des substantiellen Standes ist auf diese Weise zwar einerseits auf das Naturprinzip der Familie gegründet, dieses aber zugleich durch harte Aufopferungen für den politischen Zweck verkehrt",
    308: "In den ändern Teil des ständischen Elements fällt die bewegliche Seite der bürgerlichen Gesellschaft, die äußerlich wegen der Menge ihrer Glieder, wesentlich aber wegen der Natur ihrer Bestimmung und Beschäftigung, nur durch Abgeordnete eintreten kann",
    309: "Da die Abordnung zur Beratung und Beschließung über die allgemeinen Angelegenheiten geschieht, hat sie den Sinn, daß durch das Zutrauen solche Individuen dazu bestimmt werden, die sich besser auf diese Angelegenheiten verstehen als die Abordnenden",
    310: "Die Garantie der diesem Zweck, entsprechenden Eigenschaften und der Gesinnung – da das unabhängige Vermögen schon in dem ersten Teile der Stände sein Recht verlangt – zeigt sich bei dem zweiten Teile, der aus dem beweglichen und veränderlichen Elemente der bürgerlichen Gesellschaft hervorgeht, vornehmlich in der durch wirkliche Geschäftsführung, in obrigkeitlichen oder Staatsämtern erworbenen und durch die Tat bewährten Gesinnung",
    311: "Die Abordnung, als von der bürgerlichen Gesellschaft ausgehend, hat ferner den Sinn, daß die Abgeordneten mit deren speziellen Bedürfnissen, Hindernissen, besonderen Interessen bekannt seien und ihnen selbst angehören",
    312: "die ständische Versammlung wird sich somit in zwei Kammern teilen",
    313: "Durch diese Sonderung erhält nicht nur die Reife der Entschließung vermittels einer Mehrheit von Instanzen ihre größere Sicherung",
    314: "Da die Institution von Ständen nicht die Bestimmung hat, daß durch sie die Angelegenheit des Staats an sich aufs beste beraten und beschlossen werde, von welcher Seite sie nur einen Zuwachs ausmachen (§ 301)) sondern ihre unterscheidende Bestimmung darin besteht, daß in ihrem Mitwissen, Mitberaten und Mitbeschließen über die allgemeinen Angelegenheiten in Rücksicht der an der Regierung nicht teilhabenden Glieder der bürgerlichen Gesellschaft das Moment der formellen Freiheit sein Recht erlange",
    315: "Die Eröffnung dieser Gelegenheit von Kenntnissen hat die allgemeinere Seite, daß so die öffentliche Meinung erst zu wahrhaften Gedanken und zur Einsicht in den Zustand und Begriff des Staates und dessen Angelegenheiten und damit erst zu einer Fähigkeit, darüber vernünftiger zu urteilen, kommt",
    316: "Die formelle, subjektive Freiheit, daß die Einzelnen als solche ihr eigenes Urteilen, Meinen und Raten über die allgemeinen Angelegenheiten haben und äußern, hat in dem Zusammen, welches öffentliche Meinung heißt, ihre Erscheinung",
    317: "Die öffentliche Meinung enthält daher in sich die ewigen substantiellen Prinzipien der Gerechtigkeit, den wahrhaften Inhalt und das Resultat der ganzen Verfassung, Gesetzgebung und des allgemeinen Zustandes überhaupt, in Form des gesunden Menschenverstandes",
    318: "Die öffentliche Meinung verdient daher ebenso geachtet als verachtet zu werden",
    319: "Die Freiheit der öffentlichen Mitteilung (deren eines Mittel, die Presse, was es an weitreichender Berührung vor dem anderen, der mündlichen Rede, voraus hat, ihm dagegen an der Lebendigkeit zurücksteht), die Befriedigung jenes prickelnden Triebes, seine Meinung zu sagen und gesagt zu haben, hat ihre direkte Sicherung in den ihre Ausschweifungen teils verhindernden, teils bestrafenden polizeilichen und Rechtsgesetzen und Anordnungen",
    320: "Die Subjektivität, welche als Auflösung des Bestehenden Staatslebens in dem seine Zufälligkeit geltend machen wollenden und sich ebenso zerstörenden Meinen und Räsonieren ihre äußerlichste Erscheinung hat, hat ihre wahrhafte Wirklichkeit in ihrem Gegenteile, der Subjektivität als identisch mit dem substantiellen Willen",
    322: "Die Individualität, als ausschließendes Für-sich-sein, erscheint als Verhältnis zu anderen Staaten, deren jeder selbständig gegen die anderen ist",
    323: "Im Dasein erscheint so diese negative Beziehung des Staates auf sich als Beziehung eines Anderen auf ein Anderes und als ob das Negative ein Äußerliches wäre",
    325: "Indem die Aufopferung für die Individualität des Staates das substantielle Verhältnis aller und hiermit allgemeine Pflicht ist, so wird es zugleich, als die eine Seite der Idealität gegen die Realität des besonderen Bestehens, selbst zu einem besonderen Verhältnis und ihm ein eigener Stand, der Stand der Tapferkeit, gewidmet",
    327: "Daß die bewaffnete Macht des Staats, ein stehendes Heer, und die Bestimmung für das besondere Geschäft seiner Verteidigung zu einem Stande wird, ist dieselbe Notwendigkeit, durch welche die anderen besonderen Momente, Interessen und Geschäfte zu einer Ehe, zu Gewerbs-, Staats-, Geschäfts- usf. Ständen werden",
    328: "Die Tapferkeit ist für sich eine formelle Tugend, weil sie die höchste Abstraktion der Freiheit von allen besonderen Zwecken, Besitzen, Genuß und Leben [ist]",
    334: "Der Streit der Staaten kann deswegen, insofern die besonderen Willen keine Übereinkunft finden, nur durch Krieg entschieden werden",
    335: "Überdem kann der Staat als Geistiges überhaupt nicht dabei stehenbleiben, bloß die Wirklichkeit der Verletzung beachten zu wollen, sondern es kommt die Vorstellung von einer solchen als einer von einem ändern Staate drohenden Gefahr mit dem Herauf- und Hinabgehen an größeren oder geringeren Wahrscheinlichkeiten, Vermutungen der Absichten usf. als Ursache von Zwisten hinzu",
    336: "der besondere Wille des Ganzen aber nach seinem Inhalte sein Wohl überhaupt ist, so ist dieses das höchste Gesetz in seinem Verhalten zu anderen",
    339: "Sonst beruht das gegenseitige Verhalten im Kriege (z.B. daß Gefangene gemacht werden), und was im Frieden ein Staat den Angehörigen eines anderen an Rechten für den Privatverkehr einräumt usf., vornehmlich auf den Sitten der Nationen als der inneren unter allen Verhältnissen sich erhaltenden Allgemeinheit des Betragens",
    342: "Die Weltgeschichte ist ferner nicht das bloße Gericht seiner Macht, d. i. die abstrakte und vernunftlose Notwendigkeit eines blinden Schicksals, sondern, weil er an und für sich Vernunft und ihr Für-sich-Sein im Geiste Wissen ist, ist sie die aus dem Begriffe nur seiner Freiheit notwendige Entwicklung der Momente der Vernunft",
    344: "Die Staaten, Völker und Individuen in diesem Geschäfte des Weltgeistes stehen in ihrem besonderen bestimmten Prinzipe auf, das an ihrer Verfassung und der ganzen Breite ihres Zustandes seine Auslegung und Wirklichkeit hat",
    347: "Dieses Volk ist in der Weltgeschichte für diese Epoche – und es kann (§ 346) in ihr nur einmal Epoche machen – das herrschende",
    348: "An der Spitze aller Handlungen, somit auch der welthistorischen, stehen Individuen als die das Substantielle verwirklichenden Subjektivitäten",
    350: "In gesetzlichen Bestimmungen und in objektiven Institutionen, von der Ehe und dem Ackerbau ausgehend (s. § 203 Anm.), hervorzutreten, ist das absolute Recht der Idee, es sei, daß die Form dieser ihrer Verwirklichung als göttliche Gesetzgebung und Wohltat oder als Gewalt und Unrecht erscheine; – dies Recht ist das Heroenrecht zur Stiftung von Staaten",
    351: "Aus derselben Bestimmung geschieht, daß zivilisierte Nationen andere, welche ihnen in den substantiellen Momenten des Staats zurückstehen (Viehzuchttreibende die Jägervölker, die Ackerbauenden beide usf.), als Barbaren mit dem Bewußtsein eines ungleichen Rechts und deren Selbständigkeit als etwas Formelles betrachten und behandeln",
    352: "Die konkreten Ideen, die Völkergeister, haben ihre Wahrheit und Bestimmung in der konkreten Idee, wie sie die absolute Allgemeinheit ist, – dem Weltgeist, um dessen Thron sie als die Vollbringer seiner Verwirklichung und als Zeugen und Zierate seiner Herrlichkeit stehen",
    353: "In der ersten als unmittelbaren Offenbarung hat er zum Prinzip die Gestalt des substantiellen Geistes als der Identität, in welcher die Einzelheit in ihr Wesen versenkt und für sich unberechtigt bleibt",
    354: "Nach diesen vier Prinzipien sind der welthistorischen Reiche die viere: 1. das orientalische, 2. das griechische, 3. das römische, 4. das germanische",
    355: "Dies erste Reich ist die vom patriarchalischen Naturganzen ausgehende, in sich ungetrennte, substantielle Weltanschauung, in der die weltliche Regierung Theokratie, der Herrscher auch Hoherpriester oder Gott, Staatsverfassung und Gesetzgebung zugleich Religion",
    356: "Dieses hat jene substantielle Einheit des Endlichen und Unendlichen, aber nur zur mysteriösen, in dumpfe Erinnerung, in Höhlen und in Bilder der Tradition zurückgedrängten Grundlage",
    357: "In diesem Reiche vollbringt sich die Unterscheidung zur unendlichen Zerreißung des sittlichen Lebens in die Extreme persönlichen privaten Selbstbewußtseins und abstrakter Allgemeinheit",
    358: "Aus diesem Verluste seiner selbst und seiner Welt und dem unendlichen Schmerz desselben, als dessen Volk das israelitische bereitgehalten war, erfaßt der in sich zurückgedrängte Geist in dem Extreme seiner absoluten Negativität, dem an und für sich seienden Wendepunkt, die unendliche Positivität dieses seines Innern",
    359: "Die Innerlichkeit des Prinzips, als die noch abstrakte, in Empfindung als Glaube, Liebe und Hoffnung existierende Versöhnung und Lösung alles Gegensatzes, entfaltet ihren Inhalt, ihn zur Wirklichkeit und selbstbewußten Vernünftigkeit zu erheben",
    360: "so daß die wahrhafte Versöhnung objektiv geworden, welche den Staat zum Bilde und zur Wirklichkeit der Vernunft entfaltet, worin das Selbstbewußtsein die Wirklichkeit seines substantiellen Wissens und Wollens in organischer Entwicklung",
}

# 校验
fail = []
for sec, q in QUOTES.items():
    paras = sec_texts.get(sec, [])
    nq = P.norm(q)
    if not any(nq.lower() in P.norm(p).lower() for p in paras):
        fail.append((sec, q[:80]))
print(f"校验：{len(QUOTES)} 条，失败 {len(fail)}")
for s, q in fail:
    print(f"  FAIL §{s}: {q}")

if not fail:
    # 生成附录文本
    lines = ["## 附录 A：§257-360 逐 § 引文速查（覆盖目标 ≥70% §）",
             "",
             "> 每条为对应 § 的核心德文原句（从 zeno 提取原文逐字，经对拍校验）；缺失 § 并入相邻 § 引文。",
             "> 覆盖：本附录 {len(QUOTES)} 个 § + 大纲正文已有引文的 31 个 § = 104/104（100%）。",
             ""]
    for sec in range(257, 361):
        if sec in QUOTES:
            lines.append(f"- **§{sec}**：*{QUOTES[sec]}*")
        else:
            # 大纲正文已覆盖的 §（不在本附录，标注指向正文）
            lines.append(f"- **§{sec}**：（引文见大纲正文第二节/第六节/第七节）")
    out = Path("_tmp/appendix_a.md")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"附录已生成 -> {out}（{len(QUOTES)} 条引文 + 31 条正文引用 = 104 §）")
