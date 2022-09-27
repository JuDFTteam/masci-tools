(devguidetests)=


# Test suite of masci-tools

## Installation

Install the package with the `testing` extra:

```bash
pip install -e .[testing]
```

## Running the tests

Run `pytest` in the `tests` path of masci-tools:
```bash
cd tests
pytest .
```

## Regenerating test files

With some code changes an update of the reference files for the tests is required. This can be done with the `--force-regen` option:


```bash
pytest --force-regen .
```
