# TODO

What is left to do in masci-tools. Keep this short: open items only, one line of context each plus a link. Remove an item in the same commit that closes it; its history lives in the linked issue or PR and in `CHANGELOG.md`.

## Release 0.15.1

Since 0.15.0, `develop` has two parser fixes: the linear-time KKR/KKRimp parsing ([#251](https://github.com/JuDFTteam/masci-tools/pull/251)) and the corrected `rms_spin_per_atom` ([#254](https://github.com/JuDFTteam/masci-tools/pull/254)). It also has new kkrparams keys: `POT_NS_CUTOFF`/`POT_NS_WRITE_CUTOFF` ([#255](https://github.com/JuDFTteam/masci-tools/pull/255)) and KKRimp `FCM` ([#257](https://github.com/JuDFTteam/masci-tools/pull/257)). There is also the option `get_dict(drop_none=True)` ([#256](https://github.com/JuDFTteam/masci-tools/pull/256)). All of these are in `CHANGELOG.md`. `develop` further has the `ignore_nan`/`doscalc` arguments of the KKRimp parser. PyPI 0.15.0 lacks those arguments, so 0.15.1 would be the first PyPI release that works with aiida-kkr.

- [ ] **Blocker:** `.github/workflows/cd.yml` publishes to PyPI only after the full CI passes, and CI is red (next section).
- [ ] On a `release-0.15.1` branch, run `bumpver update --patch`. It updates `masci_tools/__init__.py` and `pyproject.toml` and commits "bump version 0.15.0 -> 0.15.1", as the 0.15.0 release did.
- [ ] In `CHANGELOG.md`, turn the `## latest` section into `## v.0.15.1` with the compare link `v0.15.0...v0.15.1`, and start a new empty `## latest`.
- [ ] Merge the release PR, then create a GitHub release with tag `v0.15.1`. This triggers `cd.yml`, which publishes to PyPI.
- [ ] Afterwards, in aiida-kkr: raise the masci-tools floor in `pyproject.toml` from `>=0.4.8.dev5` to `>=0.15.1`. Its CI could then install from PyPI instead of git `develop`.

## Downstream: aiida-kkr and `get_dict` hashes

With the default `drop_none=False`, every new kkrparams key changes `get_dict()` and the hash of every AiiDA `Dict` built from it. This broke aiida-kkr's cached test calculations after #255; aiida-kkr now pins its CI to masci-tools `c90e5815` (aiida-kkr PR #197).

- [ ] In aiida-kkr (its issue #198): build Dicts with `get_dict(drop_none=True)`, change the two `['IMIX']` lookups to `.get('IMIX')`, and re-export the test archives once, against masci-tools `7b9d423d` or later. Then drop the CI pin.

## CI is red on `develop`

It has failed on every push since March 2026; details and first errors are in [#252](https://github.com/JuDFTteam/masci-tools/issues/252).

- [ ] Drop Python 3.7 from the test matrix: the Ubuntu 24.04 runners no longer provide it.
- [ ] Fix the NumPy 2 errors (`_ARRAY_API not found`) on Python 3.9–3.11: pin `numpy<2` or rebuild the compiled dependency against NumPy 2.
- [ ] Fix the 28 test failures on Python 3.8 after the Fleur file-version 0.38/0.39 schema commits (`tests/parsers/test_schema_dict.py` and others).
- [ ] Add `bokeh_sampledata` to the latest-bokeh job, and update the plot baseline images.
- [ ] Fix the `yapf` pre-commit failures, and the spglib intersphinx link that now returns 404 (`docs-nitpicky`).

## Smaller parser follow-ups (optional)

- [ ] `voroparser_functions.get_radial_meshpoints` still uses the quadratic search-and-pop loop. It was left alone in #251 because potential files have only one header per atom.
- [ ] Every KKR/KKRimp parse step re-reads its file through `get_outfile_txt`, and there are about 15 such steps. A 5 M-line log peaked at about 1.5 GB of memory in a local test driver that held the files in memory; how much of that the re-reads cause is not measured. Reading the file once per parse would help, if memory on the AiiDA workers ever becomes a problem.
