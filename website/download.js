import { buildIds, verifiedReleaseMetadata, digestMatches } from './release-check.mjs';

const builds = new Map(buildIds.map(id => {
  return [id, {
    status: document.getElementById(`${id}-status`),
    details: document.getElementById(`${id}-details`),
    verify: document.getElementById(`${id}-verify`),
    download: document.getElementById(`${id}-download`),
    direct: document.getElementById(`${id}-direct`),
    release: null,
    verifiedBlob: null,
  }];
}));

function unavailable(build, message) {
  build.status.textContent = message;
  build.details.textContent = '';
  build.verify.disabled = true;
  build.download.disabled = true;
  if (build.direct) build.direct.disabled = true;
  build.verifiedBlob = null;
  build.release = null;
}

for (const build of builds.values()) unavailable(build, '尚未发布 · 暂无公开安装包');

try {
  const response = await fetch('./release-manifest.json', { cache: 'no-store' });
  if (!response.ok || response.type === 'opaque') throw new Error('manifest unavailable');
  const manifest = await response.json();
  for (const [id, build] of builds) {
    const release = verifiedReleaseMetadata(manifest, id);
    if (!release) continue;
    if (!globalThis.crypto?.subtle) {
      unavailable(build, '当前环境不支持安全校验；请使用 HTTPS 或 localhost');
      continue;
    }
    build.release = release;
    build.status.textContent = '清单已读取 · 需验证安装包后才能下载';
    build.details.textContent = `版本 ${release.version} · ${release.date} · ${(release.sizeBytes / 1024 / 1024).toFixed(1)} MB · SHA-256 ${release.sha256} · 连接器支持版本：${release.supportedConnectorVersions.join('、')}`;
    build.verify.disabled = false;
    if (build.direct) build.direct.disabled = false;
  }
} catch {
  for (const build of builds.values()) unavailable(build, '无法读取发布清单 · 下载保持关闭');
}

for (const build of builds.values()) {
  build.verify.addEventListener('click', async () => {
    const release = build.release;
    if (!release || !globalThis.crypto?.subtle) return;
    build.verify.disabled = true;
    build.download.disabled = true;
    build.verifiedBlob = null;
    build.status.textContent = '正在下载并校验安装包…';
    try {
      const response = await fetch(`./${release.file}`, { cache: 'no-store' });
      if (!response.ok || response.type === 'opaque') throw new Error('artifact unavailable');
      const contentLength = response.headers.get('content-length');
      if (contentLength && Number(contentLength) !== release.sizeBytes) throw new Error('size mismatch');
      const blob = await response.blob();
      if (blob.size !== release.sizeBytes) throw new Error('size mismatch');
      const hash = await crypto.subtle.digest('SHA-256', await blob.arrayBuffer());
      const hex = Array.from(new Uint8Array(hash), b => b.toString(16).padStart(2, '0')).join('');
      if (!digestMatches(blob.size, release, hex) || build.release !== release) throw new Error('digest mismatch');
      build.verifiedBlob = blob;
      build.download.disabled = false;
      build.status.textContent = '校验通过 · 可以保存此安装包';
    } catch {
      build.status.textContent = '无法验证安装包或校验不一致 · 下载保持关闭';
    } finally {
      build.verify.disabled = false;
    }
  });

  // Direct download skips the hash check at the user's request; the URL still
  // only becomes reachable after the release manifest was read successfully.
  build.direct?.addEventListener('click', () => {
    if (!build.release || build.direct.disabled) return;
    const link = document.createElement('a');
    link.href = `./${build.release.file}`;
    link.download = build.release.file.split('/').at(-1);
    document.body.append(link);
    link.click();
    link.remove();
  });

  build.download.addEventListener('click', () => {
    if (!build.verifiedBlob || !build.release || build.download.disabled) return;
    const url = URL.createObjectURL(build.verifiedBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = build.release.file.split('/').at(-1);
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 60_000);
  });
}
