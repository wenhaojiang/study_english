# coding=utf-8
import json
import re

from docx import Document

# 打开文档
from get_yinbiao_selenium import get_yinbiao
from 音标 import PhoneticSymbol

all_word_detail = []

# file_name = r'D:\蒋一山的文件\英语\中考词汇\第 6 天.docx'
file_name = r'第 6 天.docx'
document = Document(file_name)
# 读取每段资料
# lines = lines[:5]
# 输出并观察结果，也可以通过其他手段处理文本即可
for paragraph in document.paragraphs:
    word_details = paragraph.text
    # print(word_details)
    # 1、先对词性进行规范化整理
    word_details = word_details.replace(' a dv .', ' adv. ')
    word_details = word_details.replace(' ad v.', ' adv. ')
    word_details = word_details.replace(' adv .', ' adv. ')
    word_details = word_details.replace(' a dj .', ' adj. ')
    word_details = word_details.replace(' ad j.', ' adj. ')
    word_details = word_details.replace(' adj .', ' adj. ')
    word_details = word_details.replace(' n .', ' n. ')
    word_details = word_details.replace(' v .', ' v. ')
    word_details = word_details.replace(' prep .', ' prep. ')
    word_details = word_details.replace(' conj .', ' conj. ')
    word_details = word_details.replace(' pron .', ' pron. ')
    word_details = word_details.replace(' pron.', ' pron. ')
    word_details = word_details.replace(' interj.', ' interj. ')
    word_details = word_details.replace(' vt .', ' vt. ')
    word_details = word_details.replace(' vi .', ' vi. ')
    word_details = word_details.replace('＆', '&')
    word_details = word_details.replace('  ', ' ')
    print(word_details)

    # 2、找出词性，并规范化
    pattern = r'( adv\. | adj\. | n\. | v\. | vt\. | vi\. | prep\. | pron\. | conj\. | interj. |&)+'
    search_objs = re.search(pattern, word_details)
    if search_objs:
        # print(search_objs.group(0))
        word_type = search_objs.group(0)
        # 词性 = word_type.replace(' ', '')
        # print(search_objs.group(1))
        # print(search_objs.group(2))
        # print(search_objs.group(3))
        # print(词性)
        # word_details = word_details.replace(word_type, word_type)
    else:
        continue

    # 3、分离出词性前的重点符号、序号、单词，以及词性后的中文释义
    idx_word_type = word_details.find(word_type)
    if -1 == idx_word_type:
        continue
    pre_word_detail = word_details[:idx_word_type]
    中文释义 = word_details[idx_word_type+len(word_type):]
    # print(f'词性前：{pre_word_detail}, 词性后：{中文释义}')

    # 4、找出单词的各部分
    pattern = r'([\*]?)(\d+)\.[\b]?([A-Za-z ]+)'
    search_objs = re.search(pattern, pre_word_detail)
    if search_objs:
        重点符号 = search_objs.group(1)
        序号 = search_objs.group(2)
        英文原型 = search_objs.group(3)
        # print(search_objs.group(0))
        # print(search_objs.group(1))
        # print(search_objs.group(2))
        # print(search_objs.group(3))
        英文原型 = 英文原型.strip()
        print(f'重点符号:{重点符号}，序号：{序号}，英文原型：{英文原型}，词性：{word_type}，中文释义：{中文释义}')

        ps = PhoneticSymbol()
        ps_word = ps.get_phonetic_symbol(英文原型)
        print(f'英文原型：{英文原型}，音标：{ps_word}')

        if ps_word == '没找到音标':
            continue

        all_word_detail.append({'重点符号':重点符号, '序号': 序号,'英文原型': 英文原型, '词性': word_type, '中文释义': 中文释义, '音标': ps_word})

        # 要匹配整个单词，不能用replace，否则可能会替换单词的一部分
        word_details = re.sub(f'{英文原型}\\b', f'{英文原型} {ps_word}', word_details, 1)
        paragraph.text = word_details

filename_strategy_summary = '音标.json'
with open(filename_strategy_summary, 'w', encoding='utf-8') as file:
    json.dump(all_word_detail, file, ensure_ascii=False)

document.save(r'第6天_带音标.docx')




