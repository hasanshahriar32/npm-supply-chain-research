'use strict';
// Read committed Yarn Classic descriptors without invoking install or project code.
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const npm = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm/package.json');
const semver = createRequire(npm)('semver');
const namePattern = /^(?:@[a-z0-9~][a-z0-9._~-]*\/)?[a-z0-9~][a-z0-9._~-]*$/i;
const mapping = value => value && typeof value === 'object' && !Array.isArray(value);
const own = (obj, key) => Object.hasOwn(obj, key);
const atom = /"(?:\\.|[^"\\])*"|[^",\s]+/y;

function tokens(text, separator) {
    const result = [];
    let position = 0;
    while (position < text.length) {
        atom.lastIndex = position;
        const match = atom.exec(text);
        if (!match) throw new Error('unsupported token');
        result.push(match[0][0] === '"' ? JSON.parse(match[0]) : match[0]);
        position = atom.lastIndex;
        if (position === text.length) break;
        if (!text.startsWith(separator, position)) throw new Error('unsupported separator');
        position += separator.length;
        if (position === text.length) throw new Error('empty trailing token');
    }
    return result;
}

function independentParse(text) {
    const entries = Object.create(null);
    let block;
    let group;
    for (const line of text.split(/\r?\n/)) {
        if (line === '' || line.startsWith('#')) continue;
        const trimmed = line.trimStart();
        const indent = line.length - trimmed.length;
        if (indent === 0 && line.endsWith(':')) {
            block = Object.create(null);
            for (const selector of tokens(line.slice(0, -1), ', ')) {
                if (own(entries, selector)) throw new Error('duplicate selector');
                entries[selector] = block;
            }
            group = undefined;
        } else if (block && indent === 2 && /^(?:dependencies|optionalDependencies):$/.test(trimmed)) {
            const field = trimmed.slice(0, -1);
            if (own(block, field)) throw new Error('duplicate field');
            group = block[field] = Object.create(null);
        } else if (block && (indent === 2 || (indent === 4 && group))) {
            const [key, value, extra] = tokens(trimmed, ' ');
            const target = indent === 2 ? block : group;
            if (extra !== undefined || value === undefined || own(target, key)) throw new Error('invalid field');
            target[key] = value;
            if (indent === 2) group = undefined;
        } else {
            throw new Error('unsupported entry');
        }
    }
    return entries;
}

function registry(name, version, resolved) {
    try {
        const url = new URL(resolved);
        const tail = name.split('/').at(-1);
        const tarballPath = '/' + name + '/-/' + tail + '-' + version + '.tgz';
        if (url.protocol === 'https:' && !url.username && !url.password && !url.port && !url.search &&
            (!url.hash || /^#[a-f0-9]{40}$/i.test(url.hash)) &&
            decodeURIComponent(url.pathname) === tarballPath) {
            if (url.hostname === 'registry.npmjs.org') return 'npm';
            if (url.hostname === 'registry.yarnpkg.com') return 'yarn_mirror';
        }
    } catch {
        return null;
    }
    return null;
}

function resolutionNames(resolutions) {
    if (!mapping(resolutions)) return null;
    const names = new Set();
    for (const key of Object.keys(resolutions)) {
        const parts = key.split('/');
        const tail = parts.at(-2)?.startsWith('@') ? parts.slice(-2).join('/') : parts.at(-1);
        if (!namePattern.test(tail)) return null;
        names.add(tail);
    }
    return names;
}

function edgeMap(dependencies, optional) {
    return Object.entries(dependencies).filter(([name]) => !own(optional, name)).sort();
}

function walk(manifest, entries) {
    const overrides = resolutionNames(manifest.resolutions ?? {});
    if (!overrides) return {status: 'unsupported_resolution_pattern'};
    const deps = manifest.dependencies ?? {};
    const optional = manifest.optionalDependencies ?? {};
    if (!mapping(deps) || !mapping(optional)) return {status: 'invalid_declarations'};
    const root = edgeMap(deps, optional);
    const pending = [...root];
    const visited = new Set();
    const nodes = Object.create(null);
    const issues = Object.create(null);
    const issue = key => issues[key] = (issues[key] || 0) + 1;
    for (let i = 0; i < pending.length; i++) {
        const [name, spec] = pending[i];
        if (!namePattern.test(name) || typeof spec !== 'string' || !semver.validRange(spec)) {
            issue('unsupported_dependency_spec');
            continue;
        }
        const descriptor = name + '@' + spec;
        if (visited.has(descriptor)) continue;
        visited.add(descriptor);
        const entry = entries[descriptor];
        if (overrides.has(name)) {
            issue('selective_resolution');
            continue;
        }
        if (!entry || !semver.valid(entry.version) || !semver.satisfies(entry.version, spec)) {
            issue('missing_or_incompatible_descriptor');
            continue;
        }
        if (entry.name !== undefined && entry.name !== name) {
            issue('ambiguous_package_identity');
            continue;
        }
        const origin = registry(name, entry.version, entry.resolved);
        if (!origin) {
            issue('unsupported_tarball');
            continue;
        }
        const dependencies = entry.dependencies ?? {};
        const childrenOptional = entry.optionalDependencies ?? {};
        if (!mapping(dependencies) || !mapping(childrenOptional)) {
            issue('invalid_lock_dependency_map');
            continue;
        }
        const children = edgeMap(dependencies, childrenOptional);
        nodes[descriptor] = {package: name, version: entry.version, origin,
            integrity: entry.integrity ?? null, children};
        for (const child of children) pending.push(child);
    }
    return {status: Object.keys(issues).length ? 'partial' : 'readable', roots: root, nodes, issues};
}

function evaluate(manifest, text, parseNative) {
    if (!text.split(/\r?\n/, 4).includes('# yarn lockfile v1')) return {status: 'unsupported_yarn_format'};
    if (!mapping(manifest) || manifest.workspaces !== undefined) return {status: 'unsupported_workspaces'};
    if (manifest.packageManager !== undefined && !/^yarn@1\./.test(manifest.packageManager))
        return {status: 'incompatible_declared_manager'};
    let entries, native;
    try {
        entries = independentParse(text);
        native = parseNative(text);
    } catch {
        return {status: 'unsupported_lock_syntax'};
    }
    const normalized = item => JSON.stringify(Object.keys(item).sort().map(key => {
        const value = item[key];
        return [key, mapping(value) ? Object.entries(value).sort() : value];
    }));
    if (native.type !== 'success' || Object.keys(entries).length !== Object.keys(native.object).length ||
        !Object.entries(entries).every(([key, item]) => own(native.object, key) &&
            normalized(item) === normalized(native.object[key]))) return {status: 'lock_parsers_disagree'};
    return walk(manifest, entries);
}

module.exports = {evaluate, independentParse, registry};
if (require.main === module) {
    const [manifest, lockfile, native] = process.argv.slice(2);
    const result = evaluate(JSON.parse(fs.readFileSync(manifest, 'utf8')), fs.readFileSync(lockfile, 'utf8'),
        require(native).parse);
    console.log(JSON.stringify(result));
}
