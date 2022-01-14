#!/usr/bin/env sh
pytest -v --cov-report=html --cov=masci_tools --cov=./ --mpl --mpl-generate-summary=html --mpl-results-path=mpl-results --mpl-baseline-path=files/mpl-baseline "$@"
