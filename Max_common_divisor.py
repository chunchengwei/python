#!/usr/bin/env python
'''
@Author: Chuncheng Wei
@Email: weicc1989@gmail.com
@Date: 2019-11-05 17:34:18
@LastEditTime: 2019-11-05 17:45:44
@Description:
@FilePath: /python/Max_common_divisor.py
'''


def max_common_divisor(a, b):

    def mcd(x, y):
        """
        get max common divisor
        Args: x > y
        Returns: y, x % y
        """
        r = x % y
        if r == 0:
            return y
        else:
            return mcd(y, r)

    if a < b:
        a, b = b, a

    return mcd(a, b)


res = max_common_divisor(12, 40)
print(res)
