import { cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { buildIds, digestMatches, verifiedReleaseMetadata } from './release-check.mjs';

const root = fileURLToPath(new URL('.', import.meta.url));
const destination = process.argv[2];
if (!destination) throw new Error('Usage: node build-site.mjs <fresh-output-directory>');
// A fresh directory prevents stale files from an earlier release being published.
await mkdir(destination, { recursive: false });
const files = ['index.html', 'features.html', 'privacy.html', 'download.html', 'release-notes.html', 'styles.css', 'download.js', 'release-check.mjs', 'release-manifest.json'];
for (const file of files) await cp(join(root, file), join(destination, file));
await mkdir(join(destination, 'assets'));
const assets = ['workspace.png', 'media-library.png', 'social-cover.png', 'video-cover.png', 'echo-insight-intro.mp4', 'intro.vtt'];
for (const file of assets) await cp(join(root, 'assets', file), join(destination, 'assets', file));
const manifest = JSON.parse(await readFile(join(root, 'release-manifest.json'), 'utf8'));
await mkdir(join(destination, 'artifacts'));
for (const id of buildIds) {
  const metadata = verifiedReleaseMetadata(manifest, id);
  if (!metadata) continue;
  const source = join(root, metadata.file);
  const bytes = await readFile(source);
  if (!digestMatches(bytes.length, metadata, createHash('sha256').update(bytes).digest('hex'))) throw new Error(`Artifact verification failed: ${id}`);
  await cp(source, join(destination, metadata.file));
}
await writeFile(join(destination, 'robots.txt'), 'User-agent: *\nAllow: /\n');
console.log(`Prepared static product site: ${destination}`);
