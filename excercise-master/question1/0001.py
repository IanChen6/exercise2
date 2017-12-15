# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import random,string

import random, string

with open('Promo_code.txt', 'w') as f:
    for i in range(200):
        chars = string.ascii_letters+ string.digits
        s = [random.choice(chars) for i in range(10)]
        f.write(str(s) + '\n')
f.close()