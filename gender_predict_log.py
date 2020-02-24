#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
from collections import defaultdict
import math
import re

from kcc import kcc

train = pd.read_csv('user_gender_train.txt',encoding='utf-8')
train = train.dropna(axis=0, how='any')
train.loc[train['gender'] == 2, 'gender'] = 0

test = pd.read_csv('user_gender_predict.txt',encoding='utf-8')
test = test.dropna(axis=0, how='any')


names_female = train[train['gender'] == 0]
names_male = train[train['gender'] == 1]

totals = {'f': len(names_female),
          'm': len(names_male)}

def split_lang(name):
    if re.match("^[A-Za-z ]+$", name):
        name = name.split()
    elif re.match("^[\u1780-\u17ff ]+$", name):
        name = kcc(name).split('|')
    return name

# 1.计算概率，即通过一个汉字判断为男女的概率
frequency_list_f = defaultdict(int)
for name in names_female['name']:
    name = split_lang(name)
    name = [i for i in name if i.strip() != '']
    for char in name:
        frequency_list_f[char] += 1. / totals['f']

frequency_list_m = defaultdict(int)
for name in names_male['name']:
    name = split_lang(name)
    name = [i for i in name if i.strip() != '']
    for char in name:
        frequency_list_m[char] += 1. / totals['m']

# 2.定义拉普拉斯函数，处理概率为0的情况，分子加1，分母加取值范围的大小
def LaplaceSmooth(char, frequency_list, total, alpha=1.0):
    count = frequency_list[char] * total
    distinct_chars = len(frequency_list)
    freq_smooth = (count + alpha ) / (total + distinct_chars * alpha)
    return freq_smooth

def GetLogProb(char, frequency_list, total):
    freq_smooth = LaplaceSmooth(char, frequency_list, total)
    return math.log(freq_smooth) - math.log(1 - freq_smooth)

# 平滑后的男、女概率
def ComputeLogProb(name, bases, totals, frequency_list_m, frequency_list_f):
    logprob_m = bases['m']
    logprob_f = bases['f']
    name = split_lang(name)
    name = [i for i in name if i.strip() != '']
    for char in name:
        logprob_m += GetLogProb(char, frequency_list_m, totals['m'])
        logprob_f += GetLogProb(char, frequency_list_f, totals['f'])
    return {'male': logprob_m, 'female': logprob_f}

def GetGender(LogProbs):
    return LogProbs['male'] > LogProbs['female'], abs(LogProbs['male'] - LogProbs['female'])


base_f = math.log(1 - train['gender'].mean())
base_f += sum([math.log(1 - frequency_list_f[char]) for char in frequency_list_f])

base_m = math.log(train['gender'].mean())
base_m += sum([math.log(1 - frequency_list_m[char]) for char in frequency_list_m])

bases = {'f': base_f, 'm': base_m}


result = []
scores = []
for name in test['name']:
    LogProbs = ComputeLogProb(name, bases, totals, frequency_list_m, frequency_list_f)
    # print(name, LogProbs)
    gender, score = GetGender(LogProbs)
    result.append(int(gender))
    scores.append(score)

test['gender'] = result
test['score'] = scores

test = test[test['score'] >= 1]

test[['id', 'gender', 'score', 'name']].to_csv('prediction.csv', index=False, encoding="utf-8")

