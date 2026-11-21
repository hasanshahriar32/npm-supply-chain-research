'use strict';

// Development-only witness extraction for committed npm dependency trees.
// No reify, lifecycle hooks, registry lookups, or package execution.
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const {evaluate} = require('./consumer_lock_evidence.cjs');

const npmRoot = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm');
const npmRequire = createRequire(path.join(npmRoot, 'package.json'));
const Arborist = npmRequire('@npmcli/arborist');
const semver = npmRequire('semver');

const own = (obj, key) => Object.hasOwn(obj || {}, key);
const obj = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const legalSegment = /^[A-Za-z0-9_@.~-]+$/;
const legalName = /^(?:@[a-z0-9~][a-z0-9._~-]*\/)?[a-z0-9~][a-z0-9._~-]*$/i;

function localPath(location) {
    return typeof location === 'string' && location !== '' &&
        location.split('/').every(part => legalSegment.test(part) && part !== '.' && part !== '..');
}

function workspacePatterns(value) {
    if (value === undefined) return [];
    const items = Array.isArray(value) ? value : value?.packages;
    if (!Array.isArray(items)) return null;
    const patterns = [];
    for (const item of items) {
        if (typeof item !== 'string') return null;
        const parts = item.replace(/^\.\//, '').replace(/\/$/, '').split('/');
        if (!parts.every(p => p === '*' || (localPath(p) && p !== 'node_modules'))) return null;
        patterns.push(parts);
    }
    return patterns;
}

function matchingLocations(patterns, packages) {
    return Object.keys(packages).filter(location => {
        if (!localPath(location)) return false;
        const parts = location.split('/');
        return !parts.includes('node_modules') && patterns.some(pattern =>
            pattern.length === parts.length && pattern.every((value, i) => value === '*' || value === parts[i])
        );
    }).sort();
}

function workspaceLocations(manifest, lock) {
    const rootPatterns = workspacePatterns(manifest.workspaces);
    const lockPatterns = workspacePatterns(lock.packages[''].workspaces);
    if (!rootPatterns || !lockPatterns || JSON.stringify(rootPatterns) !== JSON.stringify(lockPatterns)) {
        return null;
    }
    return matchingLocations(rootPatterns, lock.packages);
}

function sameMap(left = {}, right = {}) {
    return obj(left) && obj(right) && Object.keys(left).length === Object.keys(right).length &&
        Object.entries(left).every(([key, spec]) => typeof spec === 'string' && own(right, key) && right[key] === spec);
}

function matchingManifest(manifest, locked) {
    if (!obj(manifest) || !obj(locked) || locked.link) return false;
    return ['name', 'version'].every(key => locked[key] === undefined || locked[key] === manifest[key]) &&
        ['dependencies', 'optionalDependencies'].every(key => sameMap(manifest[key], locked[key]));
}

function resolveLocation(packages, from, name) {
    let dir = from;
    while (true) {
        if (path.posix.basename(dir) !== 'node_modules') {
            const candidate = path.posix.join(dir, 'node_modules', name);
            if (own(packages, candidate)) return candidate;
        }
        if (!dir) return undefined;
        const parent = path.posix.dirname(dir);
        dir = parent === '.' ? '' : parent;
    }
}

function registryWitness(name, record) {
    if (typeof record.resolved !== 'string') return false;
    try {
        const url = new URL(record.resolved);
        const basename = name.split('/').at(-1);
        return url.origin === 'https://registry.npmjs.org' && !url.username && !url.password &&
            decodeURIComponent(url.pathname) === `/${name}/-/${basename}-${record.version}.tgz`;
    } catch {
        return false;
    }
}

function readJSON(directory, location, name) {
    const target = path.join(directory, location, name);
    const real = fs.realpathSync(target);
    if (real !== target) throw new Error('noncanonical_evidence_path');
    return JSON.parse(fs.readFileSync(real, 'utf8'));
}

function localManifest(directory, location) {
    try {
        return readJSON(directory, location, 'package.json');
    } catch (err) {
        if (err.code === 'ENOENT' || err instanceof SyntaxError) return null;
        throw err;
    }
}

function walkImporter(start, tree, lock, declared) {
    const packages = lock.packages;
    const manifest = declared.get(start);
    const source = tree.inventory.get(start);
    const result = {importer: start, status: 'unavailable', issues: [], witnesses: []};
    if (!manifest || !source) {
        result.issues.push({reason: 'unverified_importer_manifest_or_node'});
        return result;
    }
    const pending = [{node: source, path: []}];
    const visited = new Set([source.location]);
    for (let i = 0; i < pending.length; i++) {
        const {node, path: previous} = pending[i];
        const parent = packages[node.location];
        const deps = parent?.dependencies ?? {};
        if (!obj(deps)) {
            result.issues.push({from: node.location, reason: 'invalid_dependency_declarations'});
            continue;
        }
        for (const [name, nominal] of Object.entries(deps).sort(([a], [b]) => a.localeCompare(b))) {
            if (own(parent.optionalDependencies, name)) continue;
            const issue = reason => result.issues.push({from: node.location, package: name, reason});
            if (!legalName.test(name) || typeof nominal !== 'string' || !nominal.trim() ||
                semver.validRange(nominal) === null) {
                issue('unsupported_nominal_spec');
                continue;
            }
            const edge = node.edgesOut.get(name);
            const located = resolveLocation(packages, node.location, name);
            if (!edge || edge.type !== 'prod' || edge.rawSpec !== nominal || !edge.to ||
                !located || located !== edge.to.location) {
                issue('edge_or_location_disagrees');
                continue;
            }
            const record = packages[located];
            const target = edge.to.isLink ? edge.to.target : edge.to;
            const targetRecord = packages[target.location];
            if (!obj(targetRecord) || target.inBundle || target.dev || target.optional ||
                target.devOptional || target.extraneous || target.package.name !== name ||
                ['os','cpu','libc'].some(k => targetRecord[k] !== undefined)) {
                issue('unsupported_target_or_scope');
                continue;
            }
            if (edge.to.isLink && (!record.link || record.resolved !== target.location ||
                !declared.has(target.location))) {
                issue('unverified_workspace_link');
                continue;
            }
            // Arborist supplies the effective override and its validity. Independently
            // verify both the lockfile provenance of the edge and the strict range match.
            const effective = edge.spec;
            if (!edge.valid || !effective.trim() || semver.validRange(effective) === null ||
                typeof targetRecord.version !== 'string' || target.version !== targetRecord.version ||
                !semver.valid(target.version) || !semver.satisfies(target.version, effective)) {
                issue('unverified_effective_range');
                continue;
            }
            if (visited.has(target.location)) continue;
            visited.add(target.location);
            const link = edge.to.isLink ? located : null;
            const witnessPath = [...previous, {
                from: node.location, package: name, nominal, effective,
                location: target.location, version: target.version, workspace_link: link,
            }];
            if (!link) {
                result.witnesses.push({package: name, version: target.version, location: target.location,
                    public_npm_tarball: registryWitness(name, targetRecord), path: witnessPath});
            }
            pending.push({node: target, path: witnessPath});
        }
    }
    result.status = result.issues.length ? 'partial' : 'ok';
    return result;
}

async function compare(directory, lockName) {
    if (!['package-lock.json', 'npm-shrinkwrap.json'].includes(lockName))
        throw new Error('unsupported_lockfile_name');
    const folder = fs.realpathSync(directory);
    const root = readJSON(folder, '', 'package.json');
    const lock = readJSON(folder, '', lockName);
    const unavailable = reason => ({status: 'unavailable', reason, importers: []});
    if (!obj(root) || ![2, 3].includes(lock?.lockfileVersion) || !obj(lock.packages) ||
        !matchingManifest(root, lock.packages[''])) return unavailable('unsupported_or_inconsistent_root');
    if (lockName === 'package-lock.json' && fs.existsSync(path.join(folder, 'npm-shrinkwrap.json')))
        return unavailable('shrinkwrap_has_precedence');
    for (const [location, record] of Object.entries(lock.packages)) {
        if ((location && !localPath(location)) || !obj(record) || (record.link && !localPath(record.resolved)))
            return unavailable('noncanonical_lock_location_or_link');
    }
    const workspaces = workspaceLocations(root, lock);
    if (!workspaces) return unavailable('unsupported_or_inconsistent_workspace_patterns');
    const declared = new Map([['', root]]);
    for (const location of workspaces) {
        const manifest = localManifest(folder, location);
        if (matchingManifest(manifest, lock.packages[location])) declared.set(location, manifest);
    }
    const tree = await new Arborist({path: folder, offline: true, ignoreScripts: true}).loadVirtual({subtreeOnly: true});
    const nativeLocations = new Set([...(tree.workspaces?.values() ?? [])]
        .map(location => path.relative(folder, location).split(path.sep).join('/')));
    for (const location of workspaces) {
        if (!nativeLocations.has(location)) declared.delete(location);
    }
    const unexpectedWorkspaces = [...nativeLocations].filter(location => !workspaces.includes(location));
    const importers = ['', ...workspaces].map(location => walkImporter(location, tree, lock, declared));
    const old = evaluate(root, lock);
    return {
        status: unexpectedWorkspaces.length || importers.some(i => i.status !== 'ok') ? 'partial' : 'ok',
        importers, unexpected_workspace_count: unexpectedWorkspaces.length,
        legacy_root_status: old.status, legacy_root_witnesses: old.witnesses.length,
        arborist_version: npmRequire('@npmcli/arborist/package.json').version,
        semver_version: npmRequire('semver/package.json').version,
    };
}

module.exports = {compare, workspaceLocations};
if (require.main === module) {
    compare(process.argv[2], process.argv[3]).then(r => console.log(JSON.stringify(r))).catch(err => {
        const reason = err.code || (err instanceof SyntaxError ? 'invalid_json' : 'native_or_input_error');
        console.log(JSON.stringify({status: 'unavailable', reason, importers: []}));
    });
}
