import os
import logging

import pandas as pd


def get_item(english, chinese, tag) -> str:
    words_line = "<item> <word>{}</word>\r<trans> " \
                 "<![CDATA[{}]]></trans>\r<tags>{}</tags>" \
                 "\r</item>\r".format(english, chinese, tag)
    return words_line

df_words = pd.read_csv('小学单词.csv', encoding="utf-8", index_col=0)

xml_body = "<wordbook>"
for idx, row in df_words.iterrows():
    term = row['学期']
    if '六年级下册' != term:
        continue
    if row['单元'] in ['Unit1', 'Unit2', 'Unit3']:
        unit = 'Unit1-3'
    elif row['单元'] in ['Unit4', 'Unit5', 'Unit6', 'Unit7']:
        unit = 'Unit4-7'
    else:
        unit = 'Unit8-12'
    xml_item = get_item(row['单词'], row['中文释义'], unit)
    xml_body += xml_item
xml_body += "</wordbook>"

outputs = open('小学单词六年级下册.xml', 'w', encoding='utf-8')
outputs.write(xml_body)
outputs.close()
