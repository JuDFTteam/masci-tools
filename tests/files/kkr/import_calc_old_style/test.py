#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: skip-file

from __future__ import absolute_import
from masci_tools.io.kkr_params import kkrparams

p = kkrparams(params_type='kkr')
p.read_keywords_from_inputcard()
