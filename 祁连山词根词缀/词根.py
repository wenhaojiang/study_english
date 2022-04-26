import re

import pandas as pd
import pdfplumber
from pandas import DataFrame


from docx import Document


def parse_词根(line):
    pattern = r'([0-9\-]{1,4}).?[ 、]([a-zA-Z\-\(\)/ ,，.]+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        序号 = search_objs.group(1)
        # print(grade)
        词根 = search_objs.group(2)
        print(f'序号：{序号}，词根：{词根}')
        return (序号, 词根)
    else:
        return None


def tst_parse_词根():
    line = '4 cid，cis'
    rst = parse_词根(line)
    print(rst)
    assert rst == ('4', 'cid，cis')


def tst_parse_词根2():
    line = '02 bio，bi'
    rst = parse_词根(line)
    print(rst)
    assert rst == ('02', 'bio，bi')

def tst_parse_词根3():
    line = '75、man(u)'
    rst = parse_词根(line)
    print(rst)
    assert rst == ('75', 'man(u)')

def tst_parse_词根5():
    line = '63-1 fac, fact, fect'
    rst = parse_词根(line)
    print(rst)
    assert rst == ('63-1', 'fac, fact, fect')



def parse_词根含义(line):
    pattern = r'词根含义： *[a-zA-Z ]*(.*)'
    search_objs = re.search(pattern, line)
    if search_objs:
        词根含义 = search_objs.group(1)
        词根含义 = 词根含义.strip()
        词根含义_只保留中文 = re.sub('[a-zA-Z ]*', '', 词根含义)
        print(f'用法及含义：{词根含义_只保留中文}')
        return 词根含义_只保留中文
    else:
        return None

def tst_parse_词根含义():
    # 音标中少了前/
    line = '词根含义：life生命；生物'
    print(f'原始行数据：{line}')
    rst = parse_词根含义(line)
    print(rst)
    assert rst == '生命；生物'

def tst_parse_词根含义2():
    # 音标中少了前/
    line = '词根含义：the middle point中心'
    print(f'原始行数据：{line}')
    rst = parse_词根含义(line)
    print(rst)
    assert rst == '中心'

def tst_parse_词根含义3():
    # 音标中少了前/
    line = '词根含义：（1）表示名词，“人或物”'
    print(f'原始行数据：{line}')
    rst = parse_词根含义(line)
    print(rst)
    assert rst == '（1）表示名词，“人或物”'

def tst_parse_词根含义4():
    # 音标中少了前/
    line = '词根含义：speech 说话；reason推理    '
    print(f'原始行数据：{line}')
    rst = parse_词根含义(line)
    print(rst)
    assert rst == '说话；推理'

def parse_word(line):
    # '  bicycle /ˈbaɪsɪkəl/ n. 自行车'
    # 注意：这里对音标的匹配，使用了非贪婪模式.+?，只匹配第一个音标
    pattern = r'([a-zA-Z\-\(\)]+) ?英? ?(/.+?/) (.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        单词 = search_objs.group(1)

        音标 = search_objs.group(2)
        音标 = 音标.strip()
        # 如果音标中少了前/，补上
        if not 音标.startswith('/'):
            音标 = '/' + 音标

        中文释义 = search_objs.group(3)

        # 如果中文释义中有音标，要剔除掉
        中文释义 = re.sub(r'(美? ?/.+?/)', '', 中文释义)
        # 如果有多个连续的空格，只保留一个
        中文释义 = re.sub(r'(\s{2,})', ' ', 中文释义)

        中文释义 = 中文释义.strip()

        print(f'单词：{单词}，音标：{音标}，中文释义：{中文释义}')
        return (单词, 音标, 中文释义)
    else:
        return None


def tst_parse_word():
    line = "centralize /ˈsɛntrə,laɪz/ v. 使归中央控制，集权"
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('centralize', '/ˈsɛntrə,laɪz/', 'v. 使归中央控制，集权')


def tst_parse_word2():
    # 后只有一个空格
    line = 'incline /ˈɪnklaɪn/ n. 斜坡 /ɪnˈklaɪn/ v. 点头；使倾向于，使有意于'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('incline', '/ˈɪnklaɪn/', 'n. 斜坡 v. 点头；使倾向于，使有意于')



def parse_词根词缀拆解(line):
    # 词根词缀拆解：词根 bi-双+plane 飞机
    # 词根词缀释义：词根 ant-相反+Arctic 北极→与北极相反的
    pattern = r'词根词缀(拆解|释义|解释|)： *(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        词根词缀拆解 = search_objs.group(2)
        print(f'词根词缀拆解：{词根词缀拆解}')
        return 词根词缀拆解
    else:
        return None


def tst_parse_词根词缀拆解1():
    rst = parse_词根词缀拆解('词根词缀拆解：act 表演 + 后缀 -or 表示名词，“人或物”')
    print(rst)
    assert rst == 'act 表演 + 后缀 -or 表示名词，“人或物”'


def tst_parse_词根词缀拆解2():
    rst = parse_词根词缀拆解('词根词缀释义：词根 ant-相反+Arctic 北极→与北极相反的')
    print(rst)
    assert rst == '词根 ant-相反+Arctic 北极→与北极相反的'


def tst_parse_词根词缀拆解3():
    rst = parse_词根词缀拆解('词根词缀：词根 ap-去+position 位置')
    print(rst)
    assert rst == '词根 ap-去+position 位置'


def parse_页码(line):
    # 词根词缀拆解：词根 bi-双+plane 飞机
    # 词根词缀释义：词根 ant-相反+Arctic 北极→与北极相反的
    pattern = r'^[0-9]{1,2}$'
    search_objs = re.search(pattern, line)
    if search_objs:
        页码 = search_objs.group(0)
        print(f'页码：{页码}')
        return 页码
    else:
        return None


def is_invalid_line(line):
    invalid_lines = ['ŋ', '必背词汇：', '必背词汇:']
    if line in invalid_lines:
        return True
    else:
        return False


g_direct = None
g_prefix_idx = None
g_prefix = None
g_prefix_mean = None
g_dct_words = dict()
g_lst_word = []
g_pre_line = None
g_new_word = False


def parse_line(line, append_line=False):
    global g_direct
    global g_prefix_idx
    global g_prefix
    global g_prefix_mean
    global g_dct_words
    global g_lst_word
    global g_pre_line
    global g_new_word

    line = line.strip()
    if len(line) == 0:
        return

    prefix = parse_词根(line)
    if prefix is not None:
        g_prefix_idx, g_prefix = prefix[0], prefix[1]
        # 如果字符串以'-'开头，在excel中显示时有时会出错
        if g_prefix.startswith('-'):
            g_prefix = g_prefix[1:]
        return

    prefix_mean = parse_词根含义(line)
    if prefix_mean is not None:
        g_prefix_mean = prefix_mean

        # 保留下前一行，可能需要与后一行合并，有些语句超过了一行
        g_pre_line = line
        return

    words = parse_word(line)
    if words is not None:
        g_dct_words = {'词根序号': g_prefix_idx, '词根': g_prefix, '词根含义': g_prefix_mean, '单词': words[0], '音标': words[1], '中文释义': words[2]}
        g_new_word = True

        # 保留下前一行，可能需要与后一行合并，有些语句超过了一行
        g_pre_line = line
        return

    词根词缀拆解 = parse_词根词缀拆解(line)
    if 词根词缀拆解 is not None:
        if not (g_new_word or append_line):
            print(f'词根词缀{line}之前没有解析出单词')
            assert False

        # 如果是追加的行，把原来的删除
        if append_line:
            老的词根词缀拆解 = g_lst_word.pop()
            print(f'老的词根词缀拆解: {老的词根词缀拆解}， 新的词根词缀拆解： {词根词缀拆解}')

        g_dct_words['词根词缀拆解'] = 词根词缀拆解
        g_lst_word.append(g_dct_words)

        # 将字典清空
        g_new_word = False

        # 保留下前一行，可能需要与后一行合并，有些语句超过了一行
        g_pre_line = line
        return

    print(f'无法解析的行数据：{line}')

    # 与上一行合并后再解析一次
    if g_pre_line is None:
        return

    multi_line = g_pre_line + line
    print(f'与上一行合并后的数据：{multi_line}')
    parse_line(multi_line, append_line=True)

input_filename = r'漫画词汇day7.txt'
output_filename = r'词根61-70.csv'
recite_filename = r'词根61-70背诵卡.csv'

def export_pdf():
    inputs = open(input_filename, 'r', encoding='utf-8')
    print(inputs)

    for line in inputs:

        line = line.strip()

        print(line)

        line = line.strip()
        if len(line) == 0:
            continue

        # 有时会出现一些没有意义的文字，直接跳过
        if is_invalid_line(line):
            continue

        # 解析行数据
        parse_line(line)

    global g_lst_word
    pd_book = DataFrame(g_lst_word)
    pd_book.to_csv(output_filename, index=0, encoding="utf-8")


def 制作背诵卡():
    df_book = pd.read_csv(output_filename, encoding="utf-8", index_col=0)
    sr_recite_tmp = df_book.groupby(['词根序号', '词根', '词根含义']).apply(lambda df: df['单词'].str.cat(sep='  '))
    # print(sr_recite_tmp)
    df_recite_tmp = sr_recite_tmp.to_frame('单词')
    df_recite = df_recite_tmp.reset_index()

    df_recite = df_recite.sort_values(by='词根序号', axis=0, ascending=True)
    print(df_recite)

    df_recite.to_csv(recite_filename, index=0, encoding="utf-8")


if __name__ == '__main__':
    export_pdf()
    #
    # 制作背诵卡()

    # tst_parse_词根词缀拆解1()
    # tst_parse_词根词缀拆解2()
    # tst_parse_词根词缀拆解3()
    #
    # tst_parse_词根()
    # tst_parse_词根2()
    # tst_parse_词根3()
    # tst_parse_词根5()

    # tst_parse_词根含义()
    # tst_parse_词根含义2()
    # tst_parse_词根含义3()
    # tst_parse_词根含义4()
    #
    # tst_parse_word()
    # tst_parse_word2()
