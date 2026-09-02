// 对话归档 · 解压原始档（无意识层 → 明文 JSONL）
// 用法：node 对话归档/工具/解压原始档.js [源.zstd] [目标.jsonl]
// 依赖：node:zlib 内置 zstd（Node 22+）——流式解压（处理多帧）
// 注意：会话运行中最后帧不完整会失败——请先归档最终版或等会话结束
const fs = require("fs");
const path = require("path");
const { createZstdDecompress } = require("node:zlib");

const src = process.argv[2] || path.join(__dirname, "..", "原始", "session.jsonl.zstd");
const dst = process.argv[3] || path.join(__dirname, "..", "原始", "session.jsonl");

if (!fs.existsSync(src)) {
  console.error("[解压] 未找到源文件:", src);
  process.exit(1);
}

const rd = fs.createReadStream(src);
const wr = fs.createWriteStream(dst);
const dec = createZstdDecompress();

function fail(msg) {
  console.error("[解压] 失败:", msg);
  console.error("[解压] 提示：会话运行中最后帧不完整——请先运行 python archive_unconscious.py 归档，或等会话结束后再解压");
  try { fs.unlinkSync(dst); } catch (e) {}  // 清理不完整输出
  process.exit(1);
}

rd.pipe(dec).pipe(wr);
dec.on("error", e => fail(e.message));
rd.on("error", e => fail("读取失败: " + e.message));
wr.on("finish", () => {
  const sz = fs.statSync(dst).size;
  const lines = fs.readFileSync(dst, "utf8").split("\n").filter(l => l.trim());
  console.log(`[解压] 成功: ${dst}`);
  console.log(`[解压] 明文 ${(sz / 1024 / 1024).toFixed(1)} MB，${lines.length} 行`);
  const types = {};
  for (const l of lines.slice(0, 3000)) {
    try { const o = JSON.parse(l); types[o.type] = (types[o.type] || 0) + 1; } catch (e) {}
  }
  console.log("[解压] 类型分布(前3000行):", JSON.stringify(types));
});
