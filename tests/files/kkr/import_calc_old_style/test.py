#!/usr/bin/env python
# pylint: skip-file

from masci_tools.io.kkr_params import kkrparams

p = kkrparams(params_type='kkr')
p.read_keywords_from_inputcard()
