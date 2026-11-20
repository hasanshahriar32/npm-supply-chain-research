'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { evaluate } = require('../consumer_lock_evidence.cjs');

const project = {name: 'project', version: '1.0.0'};
const a = {version: '1.3.3', resolved: 'https://registry.npmjs.org/a/-/a-1.3.3.tgz'};
function fixture(deps, entries = {}, version = 3, extra = {}) {
  const manifest = {...project, dependencies: deps, ...extra};
  return [manifest, {lockfileVersion: version, packages: {'': {...manifest}, ...entries}}];
}

test('rejects the recorded ^1.3.2 to 1.2.0 mismatch, regardless of an unrelated matching node', () => {
  const [manifest, lock] = fixture({a: '^1.3.2'}, {
    'node_modules/a': {version: '1.2.0'},
    'node_modules/unrelated/node_modules/a': a,
  });
  const out = evaluate(manifest, lock);
  assert.equal(out.status, 'partial');
  assert.deepEqual(out.witnesses, []);
  assert.equal(out.issues[0].reason, 'missing_or_incompatible_version');
});

test('honors nearest installed version and follows transitive links to hoisted siblings', () => {
  for (const version of [2, 3]) {
    const [manifest, lock] = fixture({a:'^1', b:'2'}, {
      'node_modules/a': {...a, dependencies: {b:'1', c:'3'}},
      'node_modules/b': {version:'2.0.0'},
      'node_modules/a/node_modules/b': {version:'1.1.0'},
      'node_modules/c': {version:'3.1.0', dependencies:{a:'^1'}},
    }, version);
    const {status, witnesses} = evaluate(manifest, lock);
    assert.equal(status, 'ok');
    assert.deepEqual(witnesses.map(w => w.location).sort(), [
      'node_modules/a', 'node_modules/a/node_modules/b','node_modules/b','node_modules/c',
    ]);
    const viaA = witnesses.find(w => w.location.endsWith('/a/node_modules/b'));
    assert.deepEqual(viaA.path.map(e => [e.package, e.from]), [['a',''],['b','node_modules/a']]);
    assert.equal(witnesses.find(w => w.package === 'a').public_npm_tarball, true);
    assert.equal(viaA.public_npm_tarball, false);
  }
});

test('never falls back past an incompatible nearer version', () => {
  const [manifest, lock] = fixture({a:'1'}, {
    'node_modules/a':{...a,dependencies:{b:'2'}},
    'node_modules/b':{version:'2.0.0'},
    'node_modules/a/node_modules/b':{version:'1.9.9'},
  });
  const out = evaluate(manifest, lock);
  assert.deepEqual(out.witnesses.map(w => w.package), ['a']);
  assert.equal(out.issues[0].location,'node_modules/a/node_modules/b');
});

test('uses supplied workspace importer, never a sibling workspace or the root manifest by accident', () => {
  const ws = {name:'workspace', dependencies:{a:'^1'}};
  const [root, lock] = fixture({other:'1'}, {
    'packages/x':ws,
    'packages/y/node_modules/a':a,
    'node_modules/other':{version:'1.0.0'},
  });
  const opts = {importer:'packages/x', rootManifest:root};
  assert.equal(evaluate(ws, lock, opts).issues[0].reason, 'missing_dependency_location');
  lock.packages['packages/x/node_modules/a'] = a;
  assert.deepEqual(evaluate(ws, lock, opts).witnesses.map(w=>w.location), ['packages/x/node_modules/a']);
  assert.equal(evaluate(root, lock, opts).status,'unavailable');
  assert.equal(evaluate(ws, lock, {importer:'packages/x'}).status,'unavailable');
});

test('excludes optional, peer-only and dev-only edges and unreferenced lock entries', () => {
  const [manifest, lock] = fixture({a:'^1', o:'1'}, {
    'node_modules/a':a, 'node_modules/o':a, 'node_modules/peer':a, 'node_modules/dev':a,
  },3,{optionalDependencies:{o:'2'}, devDependencies:{dev:'*'}, peerDependencies:{peer:'*'}});
  const out=evaluate(manifest,lock);
  assert.equal(out.status,'ok');
  assert.deepEqual(out.witnesses.map(w=>w.package),['a']);
});

test('missing, invalid or stale importer data never certify absence', () => {
  const [manifest, lock] = fixture({a:'1'}, {'node_modules/a':a});
  assert.equal(evaluate(manifest, {...lock,lockfileVersion:1}).status,'unavailable');
  assert.equal(evaluate(manifest, {...lock,packages:{}}).status,'unavailable');
  assert.equal(evaluate({...manifest,dependencies:{a:'2'}},lock).status,'unavailable');
  assert.equal(evaluate({...manifest,overrides:{a:'1'}},lock).issues[0].reason,'unsupported_overrides');
  assert.equal(evaluate({...manifest,dependencies:{a:null}},lock).status,'unavailable');
});

test('local links, alias specs, bundled and conflicting scope flags remain unresolved', () => {
  const [manifest, lock] = fixture({a:'1',b:'npm:a@1',c:'1', d:'1',e:'1'}, {
    'node_modules/a':{link:true,resolved:'packages/x'},'node_modules/c':{...a,inBundle:true},
    'node_modules/d':{...a,dev:true},'node_modules/e':{...a,name:'different'},
  });
  const out=evaluate(manifest, lock);
  assert.equal(out.status,'partial');
  assert.equal(out.witnesses.length,0);
  assert.equal(out.issues.length,5);
});

test('scoped package paths, public origin flag, and prerelease comparison', () => {
  const name='@org/pkg';
  const [manifest,lock] = fixture({[name]:'^2.0.0'}, {
    ['node_modules/'+name]:{version:'2.1.0-beta.1',resolved:'https://registry.npmjs.org/@org/pkg/-/pkg-2.1.0-beta.1.tgz'},
  });
  assert.equal(evaluate(manifest,lock).witnesses.length,0);
  const record=lock.packages['node_modules/'+name];
  record.version='2.1.0';
  record.resolved='https://registry.npmjs.org/@org%2fpkg/-/pkg-2.1.0.tgz';
  assert.equal(evaluate(manifest,lock).witnesses[0].public_npm_tarball,true);
  record.resolved='https://registry.example/@org/pkg/-/pkg-2.1.0.tgz';
  assert.equal(evaluate(manifest,lock).witnesses[0].public_npm_tarball,false);
});

test('does not infer portable paths through OS, CPU or libc conditional nodes', () => {
  for (const key of ['os', 'cpu', 'libc']) {
    const [manifest, lock] = fixture({a:'1'}, {
      'node_modules/a':{...a,[key]:['linux'],dependencies:{b:'1'}}, 'node_modules/b':a,
    });
    const out=evaluate(manifest,lock);
    assert.equal(out.status,'partial');
    assert.deepEqual(out.witnesses,[]);
    assert.equal(out.issues[0].reason,'platform_conditional');
  }
});
