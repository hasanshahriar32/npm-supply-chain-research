# Bounded `react-native-country-select` March 2026 candidate screen

**Screen status:** Candidate evidence recorded; no primary-ledger admission or reconstruction decision has been made.

## Candidate scope

The screen is limited to `react-native-country-select` and a strict intersection target of `0.3.91`. It does not add later releases, the separately named `react-native-international-phone-number` package, supporting scoped packages, a Glassworm campaign census, a common-actor assertion, or a relationship to any existing governed family.

## Independently reviewed incident evidence

StepSecurity reports that malicious releases were detected in the two React Native packages on 16 March 2026 and names `react-native-country-select@0.3.91` among the compromised releases. Its article separately lists later `0.4.1` and `0.4.2` releases, which are not part of the current intersection target.[1]

Aikido independently reports that two packages from the same publisher were backdoored in a coordinated supply-chain attack. It explicitly identifies `react-native-country-select@0.3.91` and gives a 16 March 2026 10:54:18 UTC publication time.[2]

The sole finite affected-version target used in this screen is therefore the independently shared `0.3.91` version. This evidence supports a candidate screen only. It does not establish historical installations, dependency reach, blast radius, current maintainer state, payload execution, controls, benignness, outcome completeness, causality, statistical independence, or predictive utility.

## Next permitted action

Access only the official npm registry metadata response for `react-native-country-select` to determine whether the exact release time is retained and whether a version object exists strictly before the one-millisecond cutoff. No package tarball, source archive, installation, payload extraction, or execution is permitted.

## References

[1]: https://www.stepsecurity.io/blog/malicious-npm-releases-found-in-popular-react-native-packages---130k-monthly-downloads-compromised "StepSecurity, Malicious npm Releases Found in Popular React Native Packages"
[2]: https://www.aikido.dev/blog/glassworm-strikes-react-packages-phone-numbers "Aikido, Glassworm Strikes Popular React Native Phone Number Packages"
