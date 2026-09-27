# TODO

What is left to do in masci-tools. Keep this short: open items only, one line of context each plus a link. Remove an item in the same commit that closes it; its history lives in the linked issue or PR and in `CHANGELOG.md`.

## Release 0.15.1

`develop` has two parser fixes since 0.15.0: the linear-time KKR/KKRimp parsing ([#251](https://github.com/JuDFTteam/masci-tools/pull/251)) and the corrected `rms_spin_per_atom` ([#254](https://github.com/JuDFTteam/masci-tools/pull/254)). It also has the `ignore_nan`/`doscalc` arguments of the KKRimp parser. PyPI 0.15.0 lacks those arguments, so 0.15.1 would be the first PyPI release that works with aiida-kkr.

- [ ] **Blocker:** `.github/workflows/cd.yml` publishes to PyPI only after the full CI passes, and CI is red (next section).
- [ ] On a `release-0.15.1` branch, run `bumpver update --patch`. It updates `masci_tools/__init__.py` and `pyproject.toml` and commits "bump version 0.15.0 -> 0.15.1", as the 0.15.0 release did.
- [ ] In `CHANGELOG.md`, turn the `## latest` section into `## v.0.15.1` with the compare link `v0.15.0...v0.15.1`, and start a new empty `## latest`.
- [ ] Merge the release PR, then create a GitHub release with tag `v0.15.1`. This triggers `cd.yml`, which publishes to PyPI.
- [ ] Afterwards, in aiida-kkr: raise the masci-tools floor in `pyproject.toml` from `>=0.4.8.dev5` to `>=0.15.1`. Its CI could then install from PyPI instead of git `develop`.

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
