import fs from 'node:fs';
import path from 'node:path';

const dir = 'D:/Code/Anything/Books/_tmp';

// 1. Merge part files
const parts = [];
for (let i = 1; i <= 9; i++) {
  parts.push(fs.readFileSync(path.join(dir, `part${i}.json`), 'utf8'));
}
// Each part is already an object fragment {...}; strip its outer braces and merge as one object
const inner = parts.map((s) => s.trim().replace(/^\s*\{/, '').replace(/\}\s*$/, '')).join(',');
const merged = '{"paragraphs": {' + inner + '}}';
fs.writeFileSync(path.join(dir, 'ch6c_rh.json'), merged, 'utf8');

// 2. Parse merged
let rh;
try {
  rh = JSON.parse(merged);
  console.log('merged JSON valid');
} catch (e) {
  console.log('merged JSON INVALID:', e.message);
  process.exit(1);
}

// 3. Load source
const srcArr = JSON.parse(fs.readFileSync(path.join(dir, 'ch6_uncited.json'), 'utf8'));
const srcMap = new Map();
for (const p of srcArr) srcMap.set(p.id, p.text);

const ids = Object.keys(rh.paragraphs);
console.log('paragraph count in output:', ids.length);

// 4. Verbatim check
const strip = (s) => s.replace(/\s+/g, '');
let errors = 0;
let chunkTotal = 0;
for (const id of ids) {
  if (!srcMap.has(id)) { console.log(`ERROR: ${id} not in source`); errors++; continue; }
  const src = strip(srcMap.get(id));
  const para = rh.paragraphs[id];
  for (const field of ['first', 'last', 'middle']) {
    if (!para[field]) continue;
    if (!Array.isArray(para[field])) { console.log(`ERROR: ${id}.${field} not array`); errors++; continue; }
    const n = para[field].length;
    if (n < 2 || n > 7) { console.log(`ERROR: ${id}.${field} has ${n} chunks (must be 2-7)`); errors++; }
    for (const c of para[field]) {
      chunkTotal++;
      if (!src.includes(strip(c.de))) {
        console.log(`MISS: ${id}.${field} chunk: [${c.de}]`);
        errors++;
      }
    }
  }
  // words check (informational)
  if (para.words) {
    for (const w of para.words) {
      if (!src.includes(strip(w.de))) {
        console.log(`WORD-MISS: ${id} word: [${w.de}]`);
        errors++;
      }
    }
  }
}
console.log('total chunks checked:', chunkTotal);
console.log(errors === 0 ? 'ALL CHECKS PASSED' : `FAILURES: ${errors}`);
