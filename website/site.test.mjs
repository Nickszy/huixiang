import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildIds, verifiedReleaseMetadata, digestMatches } from './release-check.mjs';

const root = fileURLToPath(new URL('.', import.meta.url));
const manifest = JSON.parse(await readFile(join(root, 'release-manifest.json'), 'utf8'));
const pages = ['index.html', 'features.html', 'privacy.html', 'download.html', 'release-notes.html'];
const release = (id, overrides = {}) => ({
  status: 'released', platform: id === 'windows' ? 'windows' : 'macos',
  architecture: id === 'macos-arm64' ? 'arm64' : 'x64',
  publishGate: { sourceReviewed: true, releaseNotesReviewed: true, approved: true },
  version: '0.1.0-beta.1', date: '2026-09-29',
  file: `artifacts/insight-${id}-0.1.0.${id === 'windows' ? 'exe' : 'dmg'}`,
  sha256: 'a'.repeat(64), sizeBytes: 128, supportedConnectorVersions: ['4.1.2'], ...overrides,
});
const published = (id, overrides = {}) => ({ schemaVersion: 2, status: 'released', builds: { [id]: release(id, overrides) } });

test('manifest state gates every build consistently', () => {
  assert.equal(manifest.schemaVersion, 2);
  if (manifest.status === 'unreleased') {
    for (const id of buildIds) {
      assert.equal(manifest.builds[id], null);
      assert.equal(verifiedReleaseMetadata(manifest, id), null);
    }
  } else {
    assert.equal(manifest.status, 'released');
  }
});

test('each platform/architecture has an independent release gate', () => {
  for (const id of buildIds) {
    const sample = published(id);
    assert.ok(verifiedReleaseMetadata(sample, id), id);
    for (const other of buildIds.filter(other => other !== id)) assert.equal(verifiedReleaseMetadata(sample, other), null);
    assert.equal(verifiedReleaseMetadata({ ...sample, status: 'unreleased' }, id), null);
    for (const field of ['sourceReviewed', 'releaseNotesReviewed', 'approved']) {
      assert.equal(verifiedReleaseMetadata(published(id, { publishGate: { ...release(id).publishGate, [field]: false } }), id), null);
    }
    for (const bad of [
      { status: 'unreleased' }, { platform: 'other' }, { architecture: 'other' },
      { version: '' }, { date: 'not-a-date' }, { file: 'https://evil.test/app.exe' },
      { file: 'artifacts/../app.exe' }, { file: 'artifacts/other.pkg', platform: 'windows' },
      { sha256: '0'.repeat(64) }, { sizeBytes: 0 },
      { supportedConnectorVersions: ['latest'] }, { supportedConnectorVersions: [] },
    ]) assert.equal(verifiedReleaseMetadata(published(id, bad), id), null, `${id}: ${JSON.stringify(bad)}`);
  }
  assert.equal(digestMatches(128, release('windows'), 'a'.repeat(64)), true);
  assert.equal(digestMatches(127, release('windows'), 'a'.repeat(64)), false);
  assert.equal(digestMatches(128, release('windows'), 'b'.repeat(64)), false);
});

test('all pages have working same-directory links, landmarks and no external runtime dependencies', async () => {
  for (const page of pages) {
    const html = await readFile(join(root, page), 'utf8');
    assert.match(html, /<html lang="zh-CN">/);
    assert.match(html, /<main id="main">/);
    assert.match(html, /<nav aria-label="主导航">/);
    assert.match(html, /<title>[^<]+<\/title>/);
    // Navigational links may point at the GitHub release channel; no external
    // resource loading (scripts, styles, fonts, images) is allowed.
    assert.doesNotMatch(html, /src="(?:https?:)?\/\//i);
    for (const [, url] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
      if (/^https?:\/\//i.test(url)) { assert.match(url, /^https:\/\/github\.com\//, `${page}: ${url}`); continue; }
      if (url.startsWith('#')) { assert.ok(html.includes(`id="${url.slice(1)}"`), `${page}: ${url}`); continue; }
      await readFile(join(root, url.split('#')[0]));
    }
  }
});

test('homepage distinguishes archive development from the published installer', async () => {
  const html = await readFile(join(root, 'index.html'), 'utf8');
  assert.match(html, /聊天里的生活/);
  assert.match(html, /值得好好收藏/);
  assert.match(html, /尚未打包公开/);
  assert.match(html, /0\.1\.0 为早期演示版/);
  assert.match(html, /合成界面示意/);
  assert.match(html, /搜索当前已载入的消息/);
  for (const phrase of ['跨群追一个话题', '跟进重要的人', '定时收到重点', '规划中']) assert.ok(html.includes(phrase));
  const download = await readFile(join(root, 'download.html'), 'utf8');
  assert.match(download, /下载后不会获得视频中的聊天与媒体体验/);
  assert.match(download, /仅保存模型配置，不发起调用/);
});

test('download page starts all builds disabled and does not expose direct artifact links', async () => {
  const html = await readFile(join(root, 'download.html'), 'utf8');
  for (const id of buildIds) {
    assert.match(html, new RegExp(`<button id="${id}-verify"[^>]* disabled>`));
    assert.match(html, new RegExp(`<button id="${id}-download"[^>]* disabled>`));
    assert.match(html, new RegExp(`<button id="${id}-direct"[^>]* disabled>`));
    assert.match(html, new RegExp(`id="${id}-status"`));
  }
  assert.doesNotMatch(html, /href="(?:\.\/)?artifacts\//);
  for (const page of ['index.html', 'features.html', 'download.html', 'privacy.html']) {
    assert.doesNotMatch(await readFile(join(root, page), 'utf8'), /邀请制|仅限受邀|INVITATION ONLY/);
  }
});

test('a published artifact must match metadata; existence alone is insufficient', async () => {
  for (const id of buildIds) {
    const metadata = verifiedReleaseMetadata(manifest, id);
    if (!metadata) continue;
    const path = resolve(root, metadata.file);
    assert.ok(path.startsWith(resolve(root, 'artifacts') + sep));
    const bytes = await readFile(path);
    assert.ok(digestMatches(bytes.length, metadata, createHash('sha256').update(bytes).digest('hex')));
  }
});

test('there are no published binaries while unreleased', async () => {
  const files = await readdir(root);
  if (manifest.status === 'unreleased') assert.ok(!files.includes('artifacts'), 'remove unpublished artifacts');
});
