// 모든 HTML 이 참조하는 로컬 파일(src, poster, href)이 저장소에 실제로 올라가 있는지 검사한다.
// 커밋되지 않은 파일(제외 규칙에 걸린 영상 등)이 있으면 실패한다. 사용: node tools/check-assets.mjs
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {posix} from 'node:path';
const {dirname, join, normalize} = posix;  // git 경로는 항상 / 구분

const tracked = new Set(execFileSync('git', ['ls-files'], {encoding: 'utf8'}).split('\n').filter(Boolean));
const missing = [];
for (const page of [...tracked].filter((f) => f.endsWith('.html'))) {
  const html = readFileSync(page, 'utf8');
  for (const [, ref] of html.matchAll(/\s(?:src|poster|href)="([^"#?]+)/g)) {
    if (/^(https?:|mailto:|data:|\/\/)/.test(ref)) continue;
    let target = normalize(join(dirname(page), ref));
    if (ref.endsWith('/') || target === '.') target = join(target, 'index.html');
    if (!tracked.has(target)) missing.push(`${page}: ${ref}`);
  }
}
if (missing.length) {
  console.error('저장소에 없는 참조 파일:\n' + missing.join('\n'));
  process.exit(1);
}
console.log(`ok: ${tracked.size} tracked files, all references present`);
