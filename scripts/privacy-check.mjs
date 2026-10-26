import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const git = args => execFileSync('git', args, { maxBuffer: 128 * 1024 * 1024 });
const root = git(['rev-parse', '--show-toplevel']).toString().trim();
process.chdir(root);
const staged = process.argv.includes('--staged');
const files = [...new Set(git(staged
  ? ['diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z']
  : ['ls-files', '--cached', '--others', '--exclude-standard', '-z']
).toString().split('\0').filter(Boolean))];
const denyFile = path.join(os.homedir(), '.local', 'share', 'onchain-asset-reports-private', 'denylist.json');
const deny = fs.existsSync(denyFile) ? JSON.parse(fs.readFileSync(denyFile, 'utf8')) : [];
const username = path.basename(os.homedir());
if (!['root', 'runner', 'user', 'home'].includes(username) && username.length > 3) deny.push(username);
const patterns = [
  ['absolute home path', /\/(?:Users|home|root)\//i],
  ['personal temporary path', /\/(?:private\/)?var\/folders\//i],
  ['Windows home path', /[a-z]:[\\/]+Users[\\/]/i],
  ['SSH private key', /-----BEGIN (?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----/],
  ['SSH public key / identity', /ssh-(?:ed25519|rsa)\s+[A-Za-z0-9+/]{20,}/],
  ['credential token', /(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16})/],
  ['server hostname', /codex-[a-z]+-[a-z]+-[a-f0-9]{4}/i],
  ['Cloudflare requester IP', /cf-footer-ip["'][^>]*>\s*(?:\d{1,3}\.){3}\d{1,3}/i]
];
const forbiddenNames = /(?:^|\/)(?:\.env(?:\..*)?|.*\.(?:pem|key|p12|pfx)|events[^/]*\.jsonl|SERVER-JOB\.md|download-verification\.json|research-prompt\.md|run-[^/]*-research\.sh|\.DS_Store)$/i;
const failures = [];
for (const file of files) {
  if (forbiddenNames.test(file)) failures.push([file, 'operational or credential filename']);
  if (!staged && fs.lstatSync(file).isSymbolicLink()) { failures.push([file, 'symlink requires review']); continue; }
  if (staged && git(['ls-files', '--stage', '--', file]).toString().startsWith('120000 ')) {
    failures.push([file, 'staged symlink requires review']); continue;
  }
  const bytes = staged ? git(['show', ':' + file]) : fs.readFileSync(file);
  if (bytes.includes(0)) { failures.push([file, 'binary file requires metadata review']); continue; }
  const content = bytes.toString('utf8');
  const lower = (file + '\n' + content).toLowerCase();
  if (deny.some(value => value && lower.includes(value.toLowerCase()))) failures.push([file, 'private identifier']);
  for (const [label, regex] of patterns) if (regex.test(content)) failures.push([file, label]);
}
if (failures.length) {
  for (const [file, category] of failures) console.error(`${file}: ${category}`);
  console.error('Privacy check failed. Review flagged files before sharing. Matched private values are not printed.');
  process.exitCode = 1;
} else {
  console.log(`Privacy check passed: ${files.length} ${staged ? 'staged' : 'Git-visible'} files; ${deny.length ? 'local denylist active' : 'generic checks only'}.`);
}
