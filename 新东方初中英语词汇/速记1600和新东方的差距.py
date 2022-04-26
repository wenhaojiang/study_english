# -*- coding:utf-8 -*-
import re

import pandas as pd
from docx import Document
from pandas import DataFrame


def parse_lesson_title(one_line):
    # '【第二十二 课】'
    pattern = r'^【第(.+)课】$'
    search_objs = re.search(pattern, one_line)
    if search_objs:
        lesson_id = search_objs.group(1)
        return lesson_id
    else:
        return None


def number_C2E(ChineseNumber):
    """中文数字转整形"""
    map = dict(〇=0, 一=1, 二=2, 三=3, 四=4, 五=5, 六=6, 七=7, 八=8, 九=9, 十=10)
    size = len(ChineseNumber)
    if size == 0: return 0
    if size < 2:
        return map[ChineseNumber]

    ans = 0
    continue_flag = False  # 连续进两个的标志位
    for i in range(size):
        if continue_flag:
            continue_flag = False
            continue

        if i + 1 < size and ChineseNumber[i + 1] == '十':
            ans += map[ChineseNumber[i]] * 10
            continue_flag = True
            continue
        ans += map[ChineseNumber[i]]
    return ans


def parse_word(one_line):
    # 'text [tekst]					课文'
    pattern = r'^([a-zA-Z\- ]+)\[.+'
    search_objs = re.search(pattern, one_line)
    if search_objs:
        word = search_objs.group(1)
        word = word.strip()
        return word
    else:
        return None


def parse_速记1600():
    word_list = []
    lesson_id = 1
    word_id = 1
    file_name = r'D:/蒋一山的文件/英语/中考单词速记/中考1600单词速记.docx'
    document = Document(file_name)
    for paragraph in document.paragraphs:
        one_line = paragraph.text
        one_line = one_line.strip()

        if len(one_line) == 0:
            continue

        # print(one_line)

        lesson_id_cn = parse_lesson_title(one_line)
        if lesson_id_cn is not None:
            # print(lesson_id_cn)
            lesson_id = number_C2E(lesson_id_cn)
            print(lesson_id)
            continue

        word = parse_word(one_line)
        # print(word)
        word_list.append({'word_id': f'{word_id}_l{lesson_id}', 'word': word})
        word_id += 1

    df_速记1600 = DataFrame(word_list)
    print(df_速记1600)
    out_file_name = r'D:/蒋一山的文件/英语/中考单词速记/中考1600单词速记.csv'
    df_速记1600.to_csv(out_file_name, index=0, encoding="utf-8")


def read_速记1600():
    file_name = r'D:/蒋一山的文件/英语/中考单词速记/中考1600单词速记.csv'
    df_wordlist = pd.read_csv(file_name, encoding="utf-8")
    return df_wordlist


def read_新东方():
    file_name = r'D:/蒋一山的文件/英语/新东方初中词汇/正序版单词/全书背诵.csv'
    df_wordlist = pd.read_csv(file_name, encoding="utf-8")
    return df_wordlist


if __name__ == '__main__':
    # parse_速记1600()

    pd.set_option('display.max_columns', None)

    df_速记1600 = read_速记1600()
    print(df_速记1600)
    
    df_新东方 = read_新东方()
    print(df_新东方)

    df_all = df_新东方[['序号', '单词']].merge(df_速记1600, left_on='单词', right_on='word', how='outer')
    df_all.to_csv('df_all.csv', index=0, encoding="gbk")


