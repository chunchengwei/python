#!/usr/bin/env python
# encoding: utf-8
'''
@Author: Chuncheng Wei
@Email: weicc1989@gmail.com
@Date: 2019-11-14 16:16:51
@LastEditTime: 2019-11-14 16:38:31
@Description:
@FilePath: /python/chi2_to_sigma.py
'''

import sys
from scipy import stats


def chi2_to_sigma(chi2, df):
    """chi-square value to sigma

    Args:
        chi2 ([type]): chi2 value
        df ([type]): d.o.f

    Returns:
        [type]: sigma
    """
    sigma = stats.chi2.isf(stats.chi2.sf(chi2, df), 1)**0.5
    return sigma


chi2, df = [float(i) for i in sys.argv[1:]]
sigma = chi2_to_sigma(chi2, df)
print('[chi2: {}, df: {}]: === >> sigma: {}'.format(chi2, df, sigma))
