// Return one semver-checked mandatory root dependency per archived npm project.
const fs = require('node:fs');
const path = require('node:path');
const {evaluate} = require('./consumer_lock_evidence.cjs');
const base = process.argv[2];
const results = {};
for (const id of fs.readdirSync(base).sort()) {
    const file = name => path.join(base, id, name + '.txt');
    const read = name => JSON.parse(fs.readFileSync(file(name), 'utf8'));
    const lock = ['npm-shrinkwrap.json','package-lock.json'].find(n => fs.existsSync(file(n)));
    if (!lock || !fs.existsSync(file('package.json'))) continue;
    try {
        const manifest = read('package.json');
        if (manifest?.packageManager ? !String(manifest.packageManager).startsWith('npm@') :
            ['yarn.lock','pnpm-lock.yaml'].some(n => fs.existsSync(file(n)))) continue;
        const outcome = evaluate(manifest, read(lock));
        const w = outcome.witnesses.find(w => w.path.length === 1 && w.public_npm_tarball);
        if (w) results[id] = {package:w.package, version:w.version, spec:w.path[0].spec, location:w.location, lock};
    } catch (error) {
        if (!(error instanceof SyntaxError)) throw error;
    }
}
console.log(JSON.stringify(results));
