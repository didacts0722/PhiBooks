# -*- coding: utf-8 -*-
"""修正 8 条主引文为单段连续原文（逐字对照 dump）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
g = d["gestalten"][0]

FIX = {
    "§273": "c) die Subjektivität als die letzte Willensentscheidung, – die fürstliche Gewalt, in der die unterschiedenen Gewalten zur individuellen Einheit zusammengefaßt sind, die also die Spitze und der Anfang des Ganzen, der konstitutionellen Monarchie, ist",
    "§279": "Die Subjektivität aber ist in ihrer Wahrheit nur als Subjekt, die Persönlichkeit nur als Person, und in der zur reellen Vernünftigkeit gediehenen Verfassung hat jedes der drei Momente des Begriffes seine für sich wirkliche ausgesonderte Gestaltung. Dies absolut entscheidende Moment des Ganzen ist daher nicht die Individualität überhaupt, sondern ein Individuum, der Monarch",
    "§298": "Die gesetzgebende Gewalt betrifft die Gesetze als solche, insofern sie weiterer Fortbestimmung bedürfen, und die ihrem Inhalte nach ganz allgemeinen inneren Angelegenheiten. Diese Gewalt ist selbst ein Teil der Verfassung, welche ihr vorausgesetzt ist und insofern an und für sich außer deren direkter Bestimmung liegt, aber in der Fortbildung der Gesetze und in dem fortschreitenden Charakter der allgemeinen Regierungsangelegenheiten ihre weitere Entwicklung erhält",
    "§302": "Als vermittelndes Organ betrachtet, stehen die Stände zwischen der Regierung überhaupt einerseits und dem in die besonderen Sphären und Individuen aufgelösten Volke andererseits. Ihre Bestimmung fordert an sie so sehr den Sinn und die Gesinnung des Staats und der Regierung als der Interessen der besonderen Kreise und der Einzelnen",
    "§316": "Die formelle, subjektive Freiheit, daß die Einzelnen als solche ihr eigenes Urteilen, Meinen und Raten über die allgemeinen Angelegenheiten haben und äußern, hat in dem Zusammen, welches öffentliche Meinung heißt, ihre Erscheinung. Das an und für sich Allgemeine, das Substantielle und Wahre, ist darin mit seinem Gegenteile, dem für sich Eigentümlichen und Besonderen des Meinens der Vielen, verknüpft",
    "§324": "Es ist notwendig, daß das Endliche, Besitz und Leben, als Zufälliges gesetzt werde, weil dies der Begriff des Endlichen ist. Diese Notwendigkeit hat einerseits die Gestalt von Naturgewalt, und alles Endliche ist sterblich und vergänglich. Im sittlichen Wesen aber, dem Staate, wird der Natur diese Gewalt abgenommen und die Notwendigkeit zum Werke der Freiheit, einem Sittlichen erhoben",
    "§331": "Das Volk als Staat ist der Geist in seiner substantiellen Vernünftigkeit und unmittelbaren Wirklichkeit, daher die absolute Macht auf Erden; ein Staat ist folglich gegen den anderen in souveräner Selbständigkeit. Als solcher für den anderen zu sein, d. i. von ihm anerkannt zu sein, ist seine erste absolute Berechtigung",
    "§333": "Es gibt keinen Prätor, höchstens Schiedsrichter und Vermittler zwischen Staaten, und auch diese nur zufälligerweise, d. i. nach besonderen Willen. Die Kantische Vorstellung eines ewigen Friedens durch einen Staatenbund, welcher jeden Streit schlichtete und als eine von jedem einzelnen Staate anerkannte Macht jede Mißhelligkeit beilegte und damit die Entscheidung durch Krieg unmöglich machte, setzt die Einstimmung der Staaten voraus, welche auf moralischen, religiösen oder welchen Gründen und Rücksichten, überhaupt immer auf besonderen souveränen Willen beruhte und dadurch mit Zufälligkeit behaftet bliebe",
}

n = 0
for b in g["bewegung"]:
    if b[1] in FIX:
        b[2] = FIX[b[1]]
        n += 1
        print(f"修正 {b[1]} | {b[0]}")

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print(f"修正 {n} 条，JSON 校验通过")
