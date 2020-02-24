#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ngender
names = ['阿宝',
'阿彪',
'阿城',
'阿丑',
'阿达']
for name in names:
    import re
    lang_re = re.compile(r'[^\u4e00-\u9FBF]', re.S)
    name = re.sub(lang_re, '', name)
    a = ngender.guess(name)
    print(a[0], a[1])