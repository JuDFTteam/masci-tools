#!/usr/bin/env python

from aiida_kkr.tools.kkr_params import kkrparams

p = kkrparams(params_type='kkr')
p.read_keywords_from_inputcard()
