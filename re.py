#!/home/weicc/.pyenv/shims/python
# encoding: utf-8
#******************************************************************************
# File Name: re.py
# Author: Chuncheng Wei
# Mail: weicc1989@gmail.com
# Created Time : Sun 11 Jun 2017 01:48:40 PM CST
# Last Modified: Sun 11 Jun 2017 01:54:40 PM CST
#******************************************************************************

import os
for filename in os.listdir('.'):
    if filename.startswith('PBCMAXdNdx'):
        os.rename(filename, filename.replace('PBCMAXdNdx', 'dNdx',1))

print("rename done!")
