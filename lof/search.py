# -*- coding: utf-8 -*-

"""have a nice day.

@author: Khan
@contact:  
@time: 2020/5/29 11:28
@file: search.py
@desc:  
"""

import numpy as np
from collections import Counter
import jieba
import re


def spiltword(str):
    seg_list = jieba.cut_for_search(str)  # 搜索引擎模式
    result = list(seg_list)
    return result


# 其中的str1，str2是分词后的标签列表
def tf_idf(str1, str2):
    co_str1 = (Counter(str1))  # 统计字符数量
    print(co_str1)
    co_str2 = (Counter(str2))
    p_str1 = []
    p_str2 = []
    for temp in set(str1 + str2):
        p_str1.append(co_str1[temp])
        p_str2.append(co_str2[temp])
    p_str1 = np.array(p_str1)
    p_str2 = np.array(p_str2)
    return p_str1.dot(p_str2) / (np.sqrt(p_str1.dot(p_str1)) * np.sqrt(p_str2.dot(p_str2)))


def findforkeyword(str1, str2):
    for i in str1:
        if str2.find(i) == -1:
            return False
    return True


def findintext(str1, str2):
    if str2 is None or str2 == "":
        return False
    list1 = spiltword(str1)
    list2 = spiltword(str2)
    score = tf_idf(list1, list2)
    print(score)
    if score > 0.5:
        return True
    else:
        flag = False
        if len(str1) <= 6:
            flag = findforkeyword(list1, str2)
        return flag


def parseDate(l):
    patternForTime = r'(\d{4}[\D]\d{1,2}[\D]\d{1,2}[\D]?)'
    m = re.search(patternForTime, l)
    if m is not None:
        str = m.group(1)
        return str


def findtime(sentence1, sentence2):
    try:
        str1 = parseDate(sentence1)
        print(str1)
        str2 = parseDate(sentence2)
        if str2 is None or str2 == "":
            return False
        print(str2)
        split_list = ['年', '月', '日', '-', '/', ' ', ',', '.']
        for i in split_list:
            str1 = str1.replace(i, '/')
        print(str1)
        strg1 = str1.split('/')
        print(strg1)
        for item in strg1:
            if len(item) == 1:
                item = item.zfill(2)
            if item != '' and str2.find(item) == -1:
                return False
        return True
    except Exception:
        return False
