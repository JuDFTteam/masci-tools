#!/usr/bin/env sh
pytest -v --cov-report=term-missing --cov=masci_tools --cov=./ --mpl --mpl-baseline-path=files/mpl-baseline "$@"
