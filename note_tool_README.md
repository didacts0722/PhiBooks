# note_tool.py —— 跨作品通用笔记工具

> 定位：对 `项目/<作品>/notes/*.json`（四书同构数据模型）的**持续笔记工作链**——对拍审计、书序维护、引文修正、内容追加、颗粒度观察。
> 适用于：现象学 / 小逻辑 / 法哲学 / 柏拉图（未来作品加一条配置即可）。
> 2026-08-29 建立：合并/替代散落的 reorder_sitt、reorder_staat、fix_sitt_quotes、fix_staat_quotes、check_staat_miss、verify_s260_329、dump_staat、append_sitt_gs、check_recht_gloss 等一次性脚本（多数已断链于 notes 迁移）。

## 用法

```bash
# 对拍审计 + 颗粒度报告（核心产出：暴露引文未命中/正文单薄/无有效锚环节）
python note_tool.py --work 法哲学 verify
python note_tool.py --work 现象学 verify

# 书序检查（默认只报告逆序对；含「总纲前置」时会提示勿重排）
python note_tool.py --work 法哲学 reorder
# 确认后写盘
python note_tool.py --work 法哲学 reorder --apply

# 引文逐字修正（锚定位；--quote 传逐字原文）
python note_tool.py --work 法哲学 fix-quote --anchor §166 --quote "……"

# 追加讨论补充（supps 条目）
python note_tool.py --work 现象学 append --anchor p.140 --supp-title "🔑 ……" --supp-content "……"

# 结构观察（环节清单/正文长度）
python note_tool.py --work 法哲学 dump --file sittlichkeit.json --verbose
```

## 数据模型（四书同构，2026-08-29 实测）

```
项目/<作品>/notes/*.json:
  顶层 {title, pages, mode, gestalten}
  gestalten[] {name, position, bestimmung, bewegung, diagnose, uebergang, [chain, supps]}
  bewegung[] 每元素为 list，前 4 字段语义一致：
    [0] 环节标题   [1] 原文锚（现象学 p.140 / 小逻辑 181 / 法哲学 §158 / 柏拉图 126）
    [2] 德文引文（原始，对拍对象）  [3] 笔记正文
    后续字段因作品而异（supps/diagram/group…）——工具只动 [0]-[3]，扩展字段透传
```

## 作品差异（收敛为配置，非代码分支）

| 作品 | notes 文件 | 锚格式 | 排序 | 特殊 |
|---|---|---|---|---|
| 现象学 | ch*.json + reading_help.json | `p.140` 或裸数字（ch0 Vorrede） | 页码 | **段落引读**（reading_help，无 § 标号） |
| 小逻辑 | sein/essence/begriff/vorbegriff.json | `181`（裸 § 号） | § | 原文 index 页面乱序须按页码排序 |
| 法哲学 | vorrede/abstraktes/moralitaet/sittlichkeit.json | `§158` | § | §260-329 走 staat_sec_map（页内无 § 标题） |
| 柏拉图 | parmenides.json | `126`（Stephanus） | 页码 | — |

## 对拍基准（与 build_pheno_ch123.resolve_citation 同款）

- norm：去 `*` → HTML unescape → 空白归一；**大小写不敏感**（lower 对比，避免句中/句首大小写差异误报）
- 命中：引文 norm+lower 后是某原文段落的连续子串（长度 > 8）
- 段落基线：原文 index 按页码排序重建书序（zeno 提取页面为字母序）；§ 上下文由 h4/h5 继承；法哲学 §260-329 用 sec_map

## 已知语义（verify 的「警告」分级）

- **引文未命中**：真实对拍失败（引文截断/改写/锚错）——需 fix-quote 或核对原文
- **正文单薄**（< 60 字）：颗粒度提示——该环节笔记薄，是细化候选
- **无有效锚且无对拍**：锚格式异常且无引文可依——需补锚
- 无锚但引文命中（如 Vorrede p.Vor）：正常，不警告

## 回归基线（2026-08-29 全绿）

| 作品 | 环节数 | 对拍命中 |
|---|---|---|
| 现象学 | 181 | 181/181 |
| 小逻辑 | 83 | 83/83 |
| 法哲学 | 67 | 67/67 |
| 柏拉图 | 17 | 17/17 |
