const assert = require('node:assert/strict');
const {test} = require('node:test');
const {evaluate, independentParse, registry} = require('../consumer_yarn_classic.cjs');

const text = [
    '# yarn lockfile v1',
    'parent@^1:',
    '  version "1.2.0"',
    '  resolved "https://registry.npmjs.org/parent/-/parent-1.2.0.tgz"',
    '  dependencies:',
    '    child "^1"',
    '    elective "^1"',
    '  optionalDependencies:',
    '    elective "^1"',
    '',
    'child@^1, child@~1.2:',
    '  version "1.2.1"',
    '  resolved "https://registry.yarnpkg.com/child/-/child-1.2.1.tgz"',
    '',
].join('\n');
const reference = input => ({type: 'success', object: independentParse(input)});

test('traces only mandatory descriptor paths and skips a selective resolution', () => {
    const manifest = {dependencies: {parent: '^1'}};
    const accepted = evaluate(manifest, text, reference);
    assert.equal(accepted.status, 'readable');
    assert.deepEqual(Object.keys(accepted.nodes), ['parent@^1', 'child@^1']);
    assert.deepEqual(accepted.nodes['parent@^1'].children, [['child', '^1']]);

    const overridden = evaluate({...manifest, resolutions: {'**/child': '1.2.0'}}, text, reference);
    assert.equal(overridden.issues.selective_resolution, 1);
    assert.equal(overridden.nodes['child@^1'], undefined);
});

test('rejects syntactic ambiguity and incompatible lock or registry identities', () => {
    assert.throws(() => independentParse(text + '\nparent@^1:\n  version "1.0.0"\n'), /duplicate selector/);
    assert.equal(evaluate({}, text, () => ({type: 'success', object: {}})).status, 'lock_parsers_disagree');
    assert.equal(evaluate({packageManager: 'yarn@4.0.0'}, text, reference).status, 'incompatible_declared_manager');
    assert.equal(registry('child', '1.2.1', 'https://registry.yarnpkg.com/child/-/other-1.2.1.tgz'), null);
});
