'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {test} = require('node:test');
const npm = require('../consumer_npm_development.cjs');
const pnpm = require('../consumer_pnpm_development.cjs');

async function fixture(root, records, files, inspect) {
    const folder = fs.mkdtempSync(path.join(os.tmpdir(), 'consumer-path-fixture-'));
    const save = (name, value) => {
        const target = path.join(folder, name);
        fs.mkdirSync(path.dirname(target), {recursive: true});
        fs.writeFileSync(target, JSON.stringify(value));
    };
    try {
        save('package.json', root);
        save('package-lock.json', {name: root.name, version: root.version, lockfileVersion: 3, packages: records});
        for (const [name, value] of Object.entries(files)) save(name, value);
        return await inspect(folder);
    } finally {
        fs.rmSync(folder, {recursive: true, force: true});
    }
}

test('workspace witnesses stay attached to their own importer', async () => {
    const root = {name: 'application', version: '1.0.0', workspaces: ['packages/*']};
    const first = {name: 'workspace-a', version: '1.0.0', dependencies: {leaf: '1.0.0'}};
    const second = {name: 'workspace-b', version: '1.0.0', dependencies: {leaf: '2.0.0'}};
    const records = {
        '': root,
        'packages/a': first,
        'packages/b': second,
        'node_modules/workspace-a': {resolved: 'packages/a', link: true},
        'node_modules/workspace-b': {resolved: 'packages/b', link: true},
        'node_modules/leaf': {version: '1.0.0'},
        'packages/b/node_modules/leaf': {version: '2.0.0'},
    };
    await fixture(root, records, {'packages/a/package.json': first, 'packages/b/package.json': second}, async folder => {
        const result = await npm.compare(folder, 'package-lock.json');
        assert.equal(result.status, 'ok');
        assert.deepEqual(result.importers.map(i => i.witnesses.map(w => w.version)), [[], ['1.0.0'], ['2.0.0']]);

        // A stale pinned manifest produces an unresolved importer rather than
        // being replaced with the declarations from the lockfile.
        fs.writeFileSync(path.join(folder, 'packages/b/package.json'),
            JSON.stringify({...second, dependencies: {leaf: '3.0.0'}}));
        const changed = await npm.compare(folder, 'package-lock.json');
        assert.equal(changed.importers[2].status, 'unavailable');
        assert.equal(changed.importers[2].witnesses.length, 0);
    });
});

test('only the authorized override context validates an out-of-range locked version', async () => {
    const root = {name: 'application', version: '1.0.0', dependencies: {alpha:'1.0.0', beta:'1.0.0'},
        overrides: {alpha: {leaf:'2.0.0'}}};
    const records = {
        '': root,
        'node_modules/alpha': {version: '1.0.0', dependencies: {leaf:'^1.0.0'}},
        'node_modules/beta': {version: '1.0.0', dependencies: {leaf:'^1.0.0'}},
        'node_modules/alpha/node_modules/leaf': {version: '2.0.0'},
        'node_modules/beta/node_modules/leaf': {version: '2.0.0'},
    };
    await fixture(root, records, {}, async folder => {
        const {importers: [result]} = await npm.compare(folder, 'package-lock.json');
        const paths = result.witnesses.filter(w => w.package === 'leaf');
        assert.equal(paths.length, 1);
        assert.equal(paths[0].path[0].package, 'alpha');
        assert.equal(paths[0].path[1].nominal, '^1.0.0');
        assert.equal(paths[0].path[1].effective, '2.0.0');
        assert.equal(result.status, 'partial');
    });
});

test('pnpm requires the correct importer, peer snapshot and native path', () => {
    const manifest = {dependencies: {alpha: '^1.0.0'}};
    const lock = {
        lockfileVersion: '9.0',
        importers: {'.': {dependencies: {alpha: {specifier: '^1.0.0', version: '1.0.1(peer@2.0.0)'}}}},
        packages: {'alpha@1.0.1': {resolution: {integrity:'sha512-YWJjZA=='}}, 'leaf@2.0.0': {}},
        snapshots: {'alpha@1.0.1(peer@2.0.0)': {dependencies:{leaf:'2.0.0'}},
                    'alpha@1.0.1(peer@3.0.0)': {dependencies:{wrong:'9.0.0'}}, 'leaf@2.0.0': {}},
    };
    const native = [{dependencies: {alpha: {from:'alpha', version:'1.0.1',
        dependencies:{leaf:{from:'leaf', version:'2.0.0'}}}}}];
    const result = pnpm.compare(manifest, lock, native);
    assert.equal(result.status, 'ok');
    assert.deepEqual(result.witnesses.map(w => w.package), ['alpha','leaf']);
    assert.equal(result.witnesses[0].public_npm_tarball, false);
    assert.equal(result.witnesses[0].registry_integrity_candidate, 'sha512-YWJjZA==');
    assert.equal(pnpm.compare({dependencies:{alpha:'^2.0.0'}}, lock, native).status, 'unavailable');
    native[0].dependencies.alpha.dependencies.leaf.version = '3.0.0';
    const wrong = pnpm.compare(manifest, lock, native);
    assert.equal(wrong.status, 'partial');
    assert.deepEqual(wrong.witnesses.map(w => w.package), ['alpha']);
    lock.importers['.'].dependencies.alpha.version = '1.0.1(patch_hash=abc)';
    assert.equal(pnpm.compare(manifest, lock, native).witnesses.length, 0);
});
