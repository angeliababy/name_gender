本项目完整源码地址：

https://github.com/angeliababy/name_gender

项目博客地址:

https://blog.csdn.net/qq_29153321/article/details/104043632

方法一：

调用包，只适合中文，原理也是贝叶斯算法
```
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
```

方法二：
贝叶斯算法

对于一个分类问题，如果我们只需要得到其标签，我们只需要求解：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120141126717.png)

1.计算每个汉字的男女概率
```
frequency_list_f = defaultdict(int)
for name in names_female['name']:
    name = split_lang(name)
    name = [i for i in name if i.strip() != '']
    for char in name:
        frequency_list_f[char] += 1. / totals['f']
```

2.考虑到预测集中可能会有汉字并没有出现在训练集中，所以我们需要对频率进行Laplace平滑。定义拉普拉斯函数，处理概率为0的情况，分子加1，分母加取值范围的大小。
```
def LaplaceSmooth(char, frequency_list, total, alpha=1.0):
    count = frequency_list[char] * total
    distinct_chars = len(frequency_list)
    freq_smooth = (count + alpha ) / (total + distinct_chars * alpha)
    return freq_smooth
```
3.在性别预测中，每个样本中大量的特征都是0。比如说只有X2=1，其他都为0，那么
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120144202921.png)
由于P(Xi)的数值通常较小，我们对整体取对数（防止浮点误差），可得
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120143822122.png)
对于一种性别，为了方面，我们将其数值存放在bases当中
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200120144616401.png)
```
base_f = math.log(1 - train['gender'].mean())
base_f += sum([math.log(1 - frequency_list_f[char]) for char in frequency_list_f])
 
base_m = math.log(train['gender'].mean())
base_m += sum([math.log(1 - frequency_list_m[char]) for char in frequency_list_m])
 
bases = {'f': base_f, 'm': base_m}
```
4.代码说明

其中一个代码为不取对数的性别预测代码，
另一个为取对数（防止浮点误差）的性别预测代码，
这两个代码主要面向中文和柬文的性别预测，
其中kcc.py为柬文的切分单字方法。

训练数据部分如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224163914550.png)

预测结果部分如下：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224163958101.png)

准确率如下:

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200224165354481.png)