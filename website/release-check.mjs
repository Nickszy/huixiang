const SHA256 = /^[a-f0-9]{64}$/i;
const VERSION = /^\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?$/i;
const BUILDS = {
  windows: { platform: 'windows', architecture: 'x64', extension: '(?:exe|msi)' },
  'macos-arm64': { platform: 'macos', architecture: 'arm64', extension: '(?:dmg|pkg)' },
  'macos-x64': { platform: 'macos', architecture: 'x64', extension: '(?:dmg|pkg)' },
};

export const buildIds = Object.keys(BUILDS);

export function verifiedReleaseMetadata(manifest, buildId) {
  const expected = BUILDS[buildId];
  if (!expected || !manifest || manifest.schemaVersion !== 2 || manifest.status !== 'released') return null;
  const build = manifest.builds?.[buildId];
  if (!build || build.status !== 'released' || build.platform !== expected.platform ||
    build.architecture !== expected.architecture ||
    build.publishGate?.sourceReviewed !== true ||
    build.publishGate?.releaseNotesReviewed !== true ||
    build.publishGate?.approved !== true ||
    typeof build.version !== 'string' || !VERSION.test(build.version) ||
    typeof build.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(build.date) ||
    Number.isNaN(Date.parse(`${build.date}T00:00:00Z`)) ||
    typeof build.file !== 'string' ||
    !new RegExp(`^artifacts/[a-zA-Z0-9][a-zA-Z0-9._-]*\\.${expected.extension}$`).test(build.file) ||
    build.file.includes('..') ||
    typeof build.sha256 !== 'string' || !SHA256.test(build.sha256) || /^0{64}$/.test(build.sha256) ||
    !Number.isSafeInteger(build.sizeBytes) || build.sizeBytes <= 0 ||
    !Array.isArray(build.supportedConnectorVersions) || build.supportedConnectorVersions.length === 0 ||
    !build.supportedConnectorVersions.every(v => typeof v === 'string' && /^\d+(?:\.\d+){2,4}$/.test(v))) return null;
  return { version: build.version, date: build.date, file: build.file, sha256: build.sha256.toLowerCase(), sizeBytes: build.sizeBytes, supportedConnectorVersions: build.supportedConnectorVersions };
}

export function digestMatches(bytes, metadata, digestHex) {
  return Number.isSafeInteger(bytes) && bytes === metadata?.sizeBytes &&
    typeof digestHex === 'string' && SHA256.test(digestHex) && digestHex.toLowerCase() === metadata.sha256;
}
