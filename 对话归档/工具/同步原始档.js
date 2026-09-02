// 对话归档 · 同步原始档（无意识层自动落沙箱）
// 读取当前会话（DSH_SESSION_JSONL 环境变量），复制到 对话归档/原始/session.jsonl.zstd
// 用法：node 对话归档/工具/同步原始档.js（可集成到构建流程——每次重建后自动归档）
const fs = require("fs");
const path = require("path");
const os = require("os");

const src = process.env.DSH_SESSION_JSONL ||
  path.join(os.homedir(), ".dsh", "sessions", "--D-Code-Anything-Books--",
    (process.env.DSH_SESSION_ID || ""), "session.jsonl.zstd");
const dst = path.join(__dirname, "..", "原始", "session.jsonl.zstd");

if (!fs.existsSync(src)) {
  console.error("[归档] 未找到会话文件:", src);
  process.exit(1);
}
fs.mkdirSync(path.dirname(dst), { recursive: true });
fs.copyFileSync(src, dst);
const mb = (fs.statSync(dst).size / 1024 / 1024).toFixed(1);
console.log(`[归档] 无意识层已同步: ${dst}（${mb} MB @ ${new Date().toISOString().slice(0, 19)}）`);
