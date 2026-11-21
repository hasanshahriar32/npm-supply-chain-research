'use strict';
// Interpret root importer edges in pnpm v9 snapshots. Corroborate each static
// path with an offline comparison against pnpm list --lockfile-only.
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const npmRoot = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm');
const semver = createRequire(path.join(npmRoot, 'package.json'))('semver');
const MAX_HOPS = 3;
const own = (obj, key) => Object.hasOwn(obj || {}, key);
const map = v => v !== null && typeof v === 'object' && !Array.isArray(v);
const namePattern = /^(?:@[a-z0-9~][a-z0-9._~-]*\/)?[a-z0-9~][a-z0-9._~-]*$/i;

function matchesIdentity(name, version, tarball) {
    if (typeof tarball !== 'string') return false;
    try {
        const url = new URL(tarball);
        const last = name.split('/').at(-1);
        return url.origin === 'https://registry.npmjs.org' && !url.username && !url.password &&
            decodeURIComponent(url.pathname) === `/${name}/-/${last}-${version}.tgz`;
    } catch {
        return false;
    }
}

function checkRoot(manifest, importer) {
    for (const kind of ['dependencies','optionalDependencies']) {
        const declared = manifest[kind] ?? {};
        const stored = importer[kind] ?? {};
        if (!map(declared) || !map(stored)) return false;
        if (Object.keys(declared).length !== Object.keys(stored).length) return false;
        if (!Object.entries(declared).every(([k,v]) => typeof v === 'string' && stored[k]?.specifier === v)) return false;
    }
    return true;
}

function compare(manifest, lock, native) {
    const result = {status: 'unavailable', witnesses: [], issues: {}};
    const unavailable = reason => ({...result, reason});
    if (!map(manifest) || String(lock?.lockfileVersion) !== '9.0' || !map(lock.importers?.['.']))
        return unavailable('unsupported_lockfile_or_root');
    const importer = lock.importers['.'];
    if (!checkRoot(manifest, importer)) return unavailable('manifest_importer_disagree');
    if (!Array.isArray(native) || native.length !== 1 || !map(native[0]))
        return unavailable('expected_one_native_root');
    const project = native[0];
    const pending = [{locked: importer, native: project, path: []}];
    // Full references preserve peer suffixes. Visit a context only once at its
    // shortest corroborated path within the three-hop observation scope.
    const visited = new Set();
    for (let i = 0; i < pending.length; i++) {
        const current = pending[i];
        const dependencies = current.locked.dependencies ?? {};
        if (!map(dependencies)) return unavailable('invalid_snapshot_dependencies');
        if (current.path.length >= MAX_HOPS) {
            if (Object.keys(dependencies).some(k => !own(current.locked.optionalDependencies, k)))
                result.issues.depth_limit = (result.issues.depth_limit || 0) + 1;
            continue;
        }
        for (const [name, raw] of Object.entries(dependencies).sort(([a], [b]) => a.localeCompare(b))) {
            if (own(current.locked.optionalDependencies, name)) continue;
            const issue = key => result.issues[key] = (result.issues[key] || 0) + 1;
            const ref = current.path.length ? raw : raw?.version;
            const version = typeof ref === 'string' ? ref.split('(')[0] : '';
            if (!namePattern.test(name) || !semver.valid(version) || ref.includes('patch_hash=') ||
                (current.path.length === 0 && (!semver.validRange(raw.specifier) ||
                                               !semver.satisfies(version, raw.specifier)))) {
                issue('unsupported_ref_or_root_spec');
                continue;
            }
            const snapshot = lock.snapshots?.[`${name}@${ref}`];
            const base = lock.packages?.[`${name}@${version}`];
            if (!map(snapshot) || !map(base) || ['os','cpu','libc'].some(k => base[k] !== undefined)) {
                issue('missing_snapshot_or_conditional_target');
                continue;
            }
            const other = current.native.dependencies?.[name];
            if (other?.from !== name || other?.version !== version) {
                issue('native_path_disagrees');
                continue;
            }
            const node = `${name}@${ref}`;
            if (visited.has(node)) continue;
            visited.add(node);
            const witness = [...current.path, {package: name, version, snapshot: node}];
            const resolution = base.resolution ?? {};
            const explicit = matchesIdentity(name, version, resolution.tarball);
            // A missing tarball URL often relies on registry configuration.
            // Preserve integrity separately for a future independent registry join.
            const integrity = typeof resolution.integrity === 'string' &&
                /^sha512-[A-Za-z0-9+/]+={0,2}$/.test(resolution.integrity) ? resolution.integrity : null;
            result.witnesses.push({package: name, version, path: witness, public_npm_tarball: explicit,
                registry_integrity_candidate: resolution.tarball === undefined ? integrity : null});
            pending.push({locked: snapshot, native: other, path: witness});
        }
    }
    result.status = Object.keys(result.issues).length ? 'partial' : 'ok';
    return result;
}

module.exports = {compare, MAX_HOPS};
if (require.main === module) {
    const input = JSON.parse(fs.readFileSync(0, 'utf8'));
    console.log(JSON.stringify(compare(input.manifest, input.lock, input.native)));
}
