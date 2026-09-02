# 工具/一次性 —— 已归档的一次性工具

> 2026-08-29 结构归位：根目录已完成使命的爬取/转换脚本迁入此处（保持可复用）。
> ⚠️ 路径说明：这些脚本的 ROOT 已修正为 `Path(__file__).resolve().parent.parent`（=项目根），
> 可在任意位置运行；运行前确认对应数据源仍存在（部分源已随项目演进移动/删除）。

## 爬取类（zeno.org / 文库下载）

| 脚本 | 用途 | 数据源状态 |
|---|---|---|
| crawl_enz.py | 爬小逻辑（Enzyklopädie_Logik） | 原文/已就绪 ✅ |
| crawl_pheno.py | 爬现象学（Phänomenologie_des_Geistes） | 原文/已就绪 ✅ |
| download_philosophers.py | 批量下载多位哲学家 zeno 页面 | 原文/已就绪 ✅ |
| download_zeno.py | zeno.org 通用下载 | 原文/已就绪 ✅ |

## 提取类（epub / 会话）

| 脚本 | 用途 | 数据源状态 |
|---|---|---|
| epub_extract.py | 庄振华义解 epub → extracted | 二手材料/已就绪 ✅ |
| epub_inspect.py | epub 结构检查 | 同上 ✅ |
| extract_all.py | 批量提取全部作品（调用 extract_zeno） | 原文/已就绪 ✅ |
| extract_zeno.py | zeno HTML → extracted JSON | 原文/已就绪 ✅ |
| extract_conversation.py | 08-26 会话 zip 转全文 | 源已移 对话归档/历史/（已修正路径） |

> 注：`extract_all.py` 依赖同目录 `extract_zeno.py`（已同迁，import 正常）。
