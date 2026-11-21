'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { test } = require('node:test');
const { createRequire } = require('node:module');

const npmRoot = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm');
const Arborist = createRequire(path.join(npmRoot, 'package.json'))('@npmcli/arborist');

test('Arborist distinguishes nominal and effective ranges for a scoped override', async () => {
    const folder = fs.mkdtempSync(path.join(os.tmpdir(), 'consumer-override-'));
    const packages = {
        '': {name: 'test-project', version: '1.0.0', dependencies: {alpha: '1.0.0', beta: '1.0.0'}},
        'node_modules/alpha': {version: '1.0.0', dependencies: {leaf: '^1.0.0'}},
        'node_modules/beta': {version: '1.0.0', dependencies: {leaf: '^1.0.0'}},
        'node_modules/leaf': {version: '1.0.0'},
        'node_modules/alpha/node_modules/leaf': {version: '2.0.0'},
    };
    try {
        const lock = {name: 'test-project', version: '1.0.0', lockfileVersion: 3, packages};
        fs.writeFileSync(path.join(folder, 'package-lock.json'), JSON.stringify(lock));
        const cases = [
            [{}, [['^1.0.0', '2.0.0', false], ['^1.0.0', '1.0.0', true]]],
            [{alpha: {leaf: '2.0.0'}}, [['2.0.0', '2.0.0', true], ['^1.0.0', '1.0.0', true]]],
            [{beta: {leaf: '2.0.0'}}, [['^1.0.0', '2.0.0', false], ['2.0.0', '1.0.0', false]]],
            [{leaf: '2.0.0'}, [['2.0.0', '2.0.0', true], ['2.0.0', '1.0.0', false]]],
        ];
        for (const [overrides, expected] of cases) {
            fs.writeFileSync(path.join(folder, 'package.json'), JSON.stringify({...packages[''], overrides}));
            const tree = await new Arborist({path: folder, offline: true, ignoreScripts: true}).loadVirtual();
            const edges = ['alpha', 'beta'].map(name => tree.edgesOut.get(name).to.edgesOut.get('leaf'));
            assert.deepEqual(edges.map(edge => edge.rawSpec), ['^1.0.0', '^1.0.0']);
            assert.deepEqual(edges.map(edge => [edge.spec, edge.to.version, edge.valid]), expected);
        }
    } finally {
        fs.unlinkSync(path.join(folder, 'package.json'));
        fs.unlinkSync(path.join(folder, 'package-lock.json'));
        fs.rmdirSync(folder);
    }
});
