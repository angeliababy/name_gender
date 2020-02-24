#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re


def kcc(textOrList):
    DIGITS = "[0-9]+"
    orex = "|"
    ENGLISH = "[a-zA-Z]+"
    PUNCTUATION = "[\pP‘’“”]+"
    NEWLINES = "[\r\n]+"
    WS = "[\s]+"
    DONT_KNOW = "."

    KHMER_PUNCTUATION = "([\u17D4-\u17DD])" # 高棉文标点符号
    KHMER_DIGITS = "([\u17E0-\u17E9]+)" # 高棉文数字0 - 9
    KHMER_DIGITS_O = "([\u17F0-\u17F9]+)" # 高棉文数字0 - 9另一种形式

    # *KCC由一个元音加上一个特殊元音构成：元音 + 特殊元音
    KCC_VV = "([\u17A3-\u17C5][\u17C6-\u17C8])"


    # *KCC由一个辅音或元音加上元音再加上一个特殊元音构成：辅音 / 元音 + 元音 + 特殊元音
    KCC_CVVV = "(([\u1780-\u17A2]|[\u17A3-\u17C5])[\u17A3-\u17C5][\u17C6-\u17C8])"

    KCC_K = "(([\u1780-\u17A2]|[\u17A3-\u17C5])(\u17CC|(\u17C9|\u17CA))?"+ "(\u17D2([\u1780-\u17A2](\u17C9|\u17CA)?|[\u17A3-\u17C5]"+ "(\u17C9|\u17CA)?)){0,2}[\u17B6-\u17C8]?[\u17CB-\u17D3]{0,2}(\u17D2[\u17A3-\u17C5])?"+ "[\u17B6-\u17C8])"

    KCC_CC = "(([\u1780-\u17A2]|[\u17A3-\u17C5])(\u17CC|(\u17C9|\u17CA))?"+ "(\u17D2([\u1780-\u17A2](\u17C9|\u17CA)?|[\u17A3-\u17C5](\u17C9|\u17CA)?)){0,2}"+ "[\u17B6-\u17C8]?[\u17CB-\u17D3]{0,2}(\u17D2([\u1780-\u17A2]|[\u17A3-\u17C5]))?)"

    dont_know = DIGITS + orex + ENGLISH + orex + PUNCTUATION + orex + NEWLINES + orex + WS + orex + DONT_KNOW

    kcc =KCC_VV+ orex + KCC_CVVV+ orex + KCC_K+ orex + KCC_CC+ orex + KHMER_PUNCTUATION+ orex + KHMER_DIGITS+ orex + KHMER_DIGITS_O+ orex + dont_know

    # khmer_kcc_pattern = re.compile(kcc, re.S)
    # kcc_pattern = khmer_kcc_pattern.findall(textOrList)
    # print(kcc_pattern)
    # substrs = re.split(khmer_kcc_pattern, textOrList)

    matchers = re.finditer(kcc, textOrList, re.S)
    word_kcc = ''
    for match in matchers:
        word_kcc = word_kcc + match.group()+ '|'
    return word_kcc


if __name__ == '__main__':

    print(kcc('ជ្រេង ច័ន្ទសុវណ្ណរស្មី'))