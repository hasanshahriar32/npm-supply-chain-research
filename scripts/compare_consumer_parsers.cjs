'use strict';
// Compare two offline interpretations of the same committed npm lockfile.
// No dependency installation, lifecycle scripts, or network resolution.
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');
const {evaluate} = require('./consumer_lock_evidence.cjs');
const npmRequire = createRequire(fs.realpathSync(process.argv[2]));
const Arborist = npmRequire('@npmcli/arborist');
const semver = npmRequire('semver');
const nodeKey = (location, name, version) => JSON.stringify([location, name, version]);
const edgeKey = (from, location, name, version) => JSON.stringify([from, location, name, version]);

async function compare(directory, lockName) {
    const manifest = JSON.parse(fs.readFileSync(path.join(directory, 'package.json'), 'utf8'));
    const lock = JSON.parse(fs.readFileSync(path.join(directory, lockName), 'utf8'));
    const custom = evaluate(manifest, lock);
    const review = {
        custom_status: custom.status,
        custom_issues: {},
        custom_locations: custom.witnesses.length,
        arborist_version: npmRequire('@npmcli/arborist/package.json').version,
        semver_version: npmRequire('semver/package.json').version,
    };
    for (const issue of custom.issues) {
        review.custom_issues[issue.reason] = (review.custom_issues[issue.reason] || 0) + 1;
    }
    if (custom.status === 'unavailable') return {...review, status: 'unsupported_input'};
    // Never follow a lockfile link outside the captured root in the virtual loader.
    if (Object.entries(lock.packages).some(([location, entry]) => {
        const unsafe = p => typeof p !== 'string' || path.isAbsolute(p) ||
            p.includes('\\') || p.split('/').includes('..');
        return unsafe(location) || (entry?.link && unsafe(entry.resolved));
    })) return {...review, status: 'outside_or_ambiguous_path'};
    const tree = await new Arborist({path: directory, offline: true, ignoreScripts: true}).loadVirtual();
    const seen = new Set([tree]), pending = [tree], nodes = new Set(), edges = new Set();
    for (let i = 0; i < pending.length; i++) {
        const parent = pending[i];
        for (const edge of parent.edgesOut.values()) {
            const target = edge.to;
            if (edge.type !== 'prod' || !edge.valid || !edge.spec.trim() || semver.validRange(edge.spec) === null ||
                !target || target.isLink || target.inBundle || target.dev || target.optional ||
                target.devOptional || target.extraneous || target.package.name !== edge.name ||
                ['os','cpu','libc'].some(k => target.package[k]?.length)) continue;
            nodes.add(nodeKey(target.location, edge.name, target.version));
            edges.add(edgeKey(parent.location, target.location, edge.name, target.version));
            if (!seen.has(target)) { seen.add(target); pending.push(target); }
        }
    }
    const common = custom.witnesses.filter(w => nodes.has(nodeKey(w.location, w.package, w.version)));
    const confirmed = common.filter(w => w.path.every(e => edges.has(edgeKey(e.from, e.location, e.package, e.version))));
    return {...review, status: 'compared', arborist_locations: nodes.size, common_locations: common.length,
        corroborated_paths: confirmed.length,
        witnesses: confirmed.map(w => ({...w, path: w.path.map(e => [e.package, e.spec, e.version, e.location])}))};
}
compare(process.argv[3], process.argv[4]).then(record => console.log(JSON.stringify(record))).catch(error => {
    if (error instanceof SyntaxError) console.log(JSON.stringify({status: 'invalid_json'}));
    else if (error.code && ['ELOCKVERIFY','ENOLOCK','EUSAGE','EINVALIDTAGNAME','EINVALIDPACKAGENAME','EMISSINGARG','ENOENT','ERESOLVE'].includes(error.code))
        console.log(JSON.stringify({status: 'parser_error', code: error.code}));
    else { console.error(error); process.exitCode = 1; }
});
