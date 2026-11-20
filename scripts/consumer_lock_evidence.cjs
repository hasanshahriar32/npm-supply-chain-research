#!/usr/bin/env node
'use strict';

// Offline, positive path evidence for the mandatory dependencies of one importer.
// Usage: node scripts/consumer_lock_evidence.cjs --manifest package.json --lockfile package-lock.json
// For a workspace, add --importer packages/example --root-manifest ROOT/package.json.
// No installation, resolution against a registry, or project code execution is performed.
const fs = require('node:fs');
const path = require('node:path');
const { parseArgs } = require('node:util');
const { createRequire } = require('node:module');

// Load the semver implementation shipped with the installed npm CLI, never a
// dependency belonging to the repository whose lockfile we are inspecting.
const npmRoot = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm');
const npmRequire = createRequire(path.join(npmRoot, 'package.json'));
const semver = npmRequire('semver');
const semverVersion = npmRequire('semver/package.json').version;

function object(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function dependencyMap(value) {
  return value === undefined || (object(value) && Object.values(value).every(v => typeof v === 'string'));
}

function sameDeclarations(left = {}, right = {}) {
  return Object.keys(left).length === Object.keys(right).length &&
    Object.entries(left).every(([name, spec]) => Object.hasOwn(right, name) && right[name] === spec);
}

function validName(name) {
  // Conservative npm package-name subset, including historical mixed-case names.
  return /^(?:@[a-z0-9~][a-z0-9._~-]*\/)?[a-z0-9~][a-z0-9._~-]*$/i.test(name);
}

function validImporter(importer) {
  return typeof importer === 'string' && !importer.includes('\\') &&
    (importer === '' || importer.split('/').every(s => s && !['.', '..', 'node_modules'].includes(s)));
}

function resolveLocation(packages, from, name) {
  let dir = from;
  while (true) {
    if (path.posix.basename(dir) !== 'node_modules') {
      const candidate = path.posix.join(dir, 'node_modules', name);
      if (Object.hasOwn(packages, candidate)) return candidate;
    }
    if (!dir) return undefined;
    const parent = path.posix.dirname(dir);
    dir = parent === '.' ? '' : parent;
  }
}

function publicNpmTarball(name, version, resolved) {
  if (typeof resolved !== 'string') return false;
  try {
    const url = new URL(resolved);
    const basename = name.split('/').pop();
    return url.origin === 'https://registry.npmjs.org' && !url.username && !url.password &&
      decodeURIComponent(url.pathname) === '/' + name + '/-/' + basename + '-' + version + '.tgz';
  } catch {
    return false;
  }
}

function evaluate(manifest, lockfile, { importer = '', rootManifest } = {}) {
  const result = {
    status: 'unavailable', importer, semver_version: semverVersion,
    scope: 'committed npm lockfile v2/v3, mandatory dependency edges only',
    witnesses: [], issues: [],
  };
  function unavailable(reason) {
    result.issues.push({reason});
    return result;
  }
  if (!validImporter(importer)) return unavailable('invalid_importer_path');
  if (!object(manifest) || !object(lockfile)) return unavailable('invalid_input_shape');
  if (![2, 3].includes(lockfile.lockfileVersion)) return unavailable('unsupported_lockfile_version');
  if (!object(lockfile.packages) || !Object.hasOwn(lockfile.packages, importer) ||
      !object(lockfile.packages[importer])) return unavailable('missing_importer');
  const root = importer === '' ? manifest : rootManifest;
  if (!object(root)) return unavailable('missing_root_manifest');
  if (root.overrides !== undefined && (!object(root.overrides) || Object.keys(root.overrides).length))
    return unavailable('unsupported_overrides');
  const packages = lockfile.packages;
  const start = packages[importer];
  if (start.link) return unavailable('unsupported_importer_link');
  for (const field of ['name', 'version']) {
    if (start[field] !== undefined && manifest[field] !== undefined && start[field] !== manifest[field])
      return unavailable('importer_identity_disagrees');
  }
  for (const field of ['dependencies', 'optionalDependencies']) {
    if (!dependencyMap(manifest[field]) || !dependencyMap(start[field])) return unavailable('invalid_manifest_or_lock_declarations');
    if (!sameDeclarations(manifest[field], start[field])) return unavailable('manifest_lock_disagree');
  }
  // Store one shortest, reproducible witness per lockfile location. Every
  // incoming edge is checked, including edges reaching an already seen node.
  const queue = [{location: importer, path: []}];
  const visited = new Set([importer]);
  for (let i = 0; i < queue.length; i++) {
    const current = queue[i];
    const record = packages[current.location];
    if (!dependencyMap(record.dependencies) || !dependencyMap(record.optionalDependencies)) {
      result.issues.push({from: current.location, reason: 'invalid_dependency_declarations'});
      continue;
    }
    for (const name of Object.keys(record.dependencies || {}).sort()) {
      if (Object.hasOwn(record.optionalDependencies || {}, name)) continue;
      const spec = record.dependencies[name];
      const edge = {from: current.location, package: name, spec};
      const issue = reason => result.issues.push({...edge, reason});
      if (!validName(name) || !spec.trim() || semver.validRange(spec) === null) {
        issue('unsupported_name_or_spec');
        continue;
      }
      const target = resolveLocation(packages, current.location, name);
      if (target === undefined) {
        issue('missing_dependency_location');
        continue;
      }
      edge.location = target;
      const dep = packages[target];
      if (!object(dep) || dep.link || dep.inBundle || (dep.name !== undefined && dep.name !== name)) {
        issue('unsupported_target_record');
        continue;
      }
      if (['os', 'cpu', 'libc'].some(key => dep[key] !== undefined)) {
        issue('platform_conditional');
        continue;
      }
      if (dep.dev || dep.optional || dep.devOptional || dep.extraneous) {
        issue('conflicting_scope_flag');
        continue;
      }
      edge.version = dep.version;
      if (typeof dep.version !== 'string' || !semver.valid(dep.version) || !semver.satisfies(dep.version, spec)) {
        issue('missing_or_incompatible_version');
        continue;
      }
      if (visited.has(target)) continue;
      visited.add(target);
      const witnessPath = [...current.path, edge];
      result.witnesses.push({
        package: name, version: dep.version, location: target, path: witnessPath,
        public_npm_tarball: publicNpmTarball(name, dep.version, dep.resolved),
      });
      queue.push({location: target, path: witnessPath});
    }
  }
  result.status = result.issues.length ? 'partial' : 'ok';
  return result;
}

function main() {
  const {values} = parseArgs({options: {
    manifest: {type: 'string'}, lockfile: {type: 'string'}, importer: {type: 'string'},
    'root-manifest': {type: 'string'},
  }});
  if (!values.manifest || !values.lockfile) throw new Error('--manifest and --lockfile are required');
  const inputs = {};
  for (const arg of ['manifest', 'lockfile', 'root-manifest']) {
    if (values[arg] === undefined) continue;
    try {
      inputs[arg] = JSON.parse(fs.readFileSync(values[arg], 'utf8'));
    } catch (error) {
      console.log(JSON.stringify({status: 'unavailable', importer: values.importer || '',
        scope: 'committed npm lockfile v2/v3, mandatory dependency edges only', semver_version: semverVersion,
        witnesses: [], issues: [{reason: error instanceof SyntaxError ? 'invalid_json' : 'unreadable_input', input: arg}]}));
      return;
    }
  }
  console.log(JSON.stringify(evaluate(inputs.manifest, inputs.lockfile, {
    importer: values.importer, rootManifest: inputs['root-manifest'],
  })));
}
module.exports = {evaluate};
if (require.main === module) main();
