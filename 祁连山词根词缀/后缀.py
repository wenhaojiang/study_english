import re

import pandas as pd
import pdfplumber
from pandas import DataFrame


def parse_词性分类(line):
    pattern = r'第[一二三四]{1}节 +(.+后缀)'
    search_objs = re.search(pattern, line)
    if search_objs:
        词性分类 = search_objs.group(1)
        print(f'词性分类：{词性分类}')
        return 词性分类
    else:
        return None


def tst_parse_词性分类1():
    rst = parse_词性分类('第一节 动词后缀')
    print(rst)
    assert rst == '动词后缀'


def tst_parse_词性分类2():
    rst = parse_词性分类('第二节 形容词/副词后缀')
    print(rst)
    assert rst == '形容词/副词后缀'


def tst_parse_词性分类3():
    rst = parse_词性分类('第三节 形容词后缀')
    print(rst)
    assert rst == '形容词后缀'


def tst_parse_词性分类4():
    rst = parse_词性分类('第四节 名词后缀')
    print(rst)
    assert rst == '名词后缀'


def parse_后缀(line):
    pattern = r'([0-9]{2}).? ([a-zA-Z\-\(\)/ ,.]+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        序号 = search_objs.group(1)
        # print(grade)
        后缀 = search_objs.group(2)
        print(f'序号：{序号}，后缀：{后缀}')
        return (序号, 后缀)
    else:
        return None


def tst_parse_后缀():
    line = '20 -er/-or/-eer/-eur'
    rst = parse_后缀(line)
    print(rst)
    assert rst == ('20', '-er/-or/-eer/-eur')


def tst_parse_后缀2():
    line = '08 -able (-ible, -ile)'
    rst = parse_后缀(line)
    print(rst)
    assert rst == ('08', '-able (-ible, -ile)')


def parse_word(line):
    # '  bicycle /ˈbaɪsɪkəl/ n. 自行车'
    # 注意：这里对音标的匹配，使用了非贪婪模式.+?，只匹配第一个音标
    pattern = r' +([a-zA-Z\-\(\)]+) ?英? ?(/?.+?/) (.+)'
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
    line = '  bicycle /ˈbaɪsɪkəl/ n. 自行车'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('bicycle', '/ˈbaɪsɪkəl/', 'n. 自行车')


def tst_parse_word2():
    # 后只有一个空格
    line = ' postdate /pəʊstˈdeɪt/ v. （在文件上）写上未来日期'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('postdate', '/pəʊstˈdeɪt/', 'v. （在文件上）写上未来日期')


def tst_parse_word3():
    # 单词和音标之间没有空格
    line = '  postwar/ˌpəʊstˈwɔː/ adj. （尤指二战）战后的'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('postwar', '/ˌpəʊstˈwɔː/', 'adj. （尤指二战）战后的')


def tst_parse_word4():
    # 音标前出现了一个“英”字
    line = ' microcopy 英/ˈmaɪkrəʊˌkɒpɪ/ n. 缩微本'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('microcopy', '/ˈmaɪkrəʊˌkɒpɪ/', 'n. 缩微本')


def tst_parse_word5():
    # 出现了两个音标
    line = ' contest /ˈkɒntest/ n. 竞赛，比赛；争夺 /kənˈtest/ v. 对……提出抗辩；参加（竞选或比赛）'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('contest', '/ˈkɒntest/', 'n. 竞赛，比赛；争夺 v. 对……提出抗辩；参加（竞选或比赛）')


def tst_parse_word6():
    # 单词中出现了括号
    line = ' afterward(s) /ˈɑːftəwəd(z)/ adv. （某事件、某时间）之后'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('afterward(s)', '/ˈɑːftəwəd(z)/', 'adv. （某事件、某时间）之后')


def tst_parse_word7():
    # 音标中少了前/
    line = ' government ˈɡʌvənmənt/ n. 政府；治理'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('government', '/ˈɡʌvənmənt/', 'n. 政府；治理')

def tst_parse_word8():
    # 音标中少了前/
    line = ' chemistry 英 /ˈkemɪstri/ 美 /ˈkemɪstri/ n.化学'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('chemistry', '/ˈkemɪstri/', 'n.化学')

def parse_后缀含义(line):
    pattern = r'后缀(用法及含义|含义及用法)(：|；) *(.*)'
    search_objs = re.search(pattern, line)
    if search_objs:
        后缀含义 = search_objs.group(3)
        print(f'用法及含义：{后缀含义}')
        return 后缀含义
    else:
        return None

def tst_parse_后缀含义():
    # 音标中少了前/
    line = '后缀含义及用法：（1）表示名词，“人或物”'
    print(f'原始行数据：{line}')
    rst = parse_后缀含义(line)
    print(rst)
    assert rst == '（1）表示名词，“人或物”'

def tst_parse_后缀含义2():
    # 音标中少了前/
    line = '后缀用法及含义：（1）表示名词，“人或物”'
    print(f'原始行数据：{line}')
    rst = parse_后缀含义(line)
    print(rst)
    assert rst == '（1）表示名词，“人或物”'

def tst_parse_后缀含义3():
    # 音标中少了前/
    line = '后缀含义及用法；（1）表示名词，“人或物”'
    print(f'原始行数据：{line}')
    rst = parse_后缀含义(line)
    print(rst)
    assert rst == '（1）表示名词，“人或物”'

def parse_词根词缀拆解(line):
    # 词根词缀拆解：后缀 bi-双+plane 飞机
    # 词根词缀释义：后缀 ant-相反+Arctic 北极→与北极相反的
    pattern = r'词根词缀(拆解|释义|解释|)： *(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        词根词缀拆解 = search_objs.group(2)
        print(f'词根词缀拆解：{词根词缀拆解}')
        return 词根词缀拆解
    else:
        return None


def tst_parse_词根词缀拆解1():
    rst = parse_词根词缀拆解('词根词缀拆解：后缀 bi-双+plane 飞机')
    print(rst)
    assert rst == '后缀 bi-双+plane 飞机'


def tst_parse_词根词缀拆解2():
    rst = parse_词根词缀拆解('词根词缀释义：后缀 ant-相反+Arctic 北极→与北极相反的')
    print(rst)
    assert rst == '后缀 ant-相反+Arctic 北极→与北极相反的'


def tst_parse_词根词缀拆解3():
    rst = parse_词根词缀拆解('词根词缀：后缀 ap-去+position 位置')
    print(rst)
    assert rst == '后缀 ap-去+position 位置'


def parse_页码(line):
    # 词根词缀拆解：后缀 bi-双+plane 飞机
    # 词根词缀释义：后缀 ant-相反+Arctic 北极→与北极相反的
    pattern = r'^[0-9]{1,2}$'
    search_objs = re.search(pattern, line)
    if search_objs:
        页码 = search_objs.group(0)
        print(f'页码：{页码}')
        return 页码
    else:
        return None


def is_invalid_line(line):
    invalid_lines = ['ŋ', ]
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

    页码 = parse_页码(line)
    if 页码 is not None:
        # 丢弃，无需处理
        return

    direct = parse_词性分类(line)
    if direct is not None:
        g_direct = direct
        return

    prefix = parse_后缀(line)
    if prefix is not None:
        g_prefix_idx, g_prefix = prefix[0], prefix[1]
        # 如果字符串以'-'开头，在excel中显示时有时会出错
        if g_prefix.startswith('-'):
            g_prefix = g_prefix[1:]
        return

    prefix_mean = parse_后缀含义(line)
    if prefix_mean is not None:
        g_prefix_mean = prefix_mean

        # 保留下前一行，可能需要与后一行合并，有些语句超过了一行
        g_pre_line = line
        return

    words = parse_word(line)
    if words is not None:
        g_dct_words = {'词性分类': g_direct, '后缀序号': g_prefix_idx, '后缀': g_prefix, '后缀含义': g_prefix_mean, '单词': words[0], '音标': words[1], '中文释义': words[2]}
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
    multi_line = g_pre_line + line
    print(f'与上一行合并后的数据：{multi_line}')
    parse_line(multi_line, append_line=True)


def export_pdf():
    with pdfplumber.open("前后缀电子教材.pdf") as pdf:
        # first_page = pdf.pages[0]  #获取第一页
        # print(first_page.chars[0])

        page_count = len(pdf.pages)
        print(page_count)  # 得到页数

        for page in pdf.pages:
            # 后缀从第25页到最后一页
            if page.page_number < 25:
                continue

            print('---------- 第[%d]页 ----------' % page.page_number)
            # 获取当前页面的全部文本信息，包括表格中的文字
            page_text = page.extract_text()
            print(page_text)
            lines = page_text.split('\n')
            print(lines)
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue

                页码 = parse_页码(line)
                if 页码 is not None:
                    # 丢弃，无需处理
                    continue

                # 有时会出现一些没有意义的文字，直接跳过
                if is_invalid_line(line):
                    continue

                # 解析行数据
                parse_line(line)

    global g_lst_word
    pd_book = DataFrame(g_lst_word)
    pd_book.to_csv('后缀.csv', index=0, encoding="utf-8")


def 制作背诵卡():
    df_book = pd.read_csv('后缀.csv', encoding="utf-8", index_col=0)
    sr_recite_tmp = df_book.groupby(['词性分类', '后缀序号', '后缀', '后缀含义']).apply(lambda df: df['单词'].str.cat(sep='  '))
    # print(sr_recite_tmp)
    df_recite_tmp = sr_recite_tmp.to_frame('单词')
    df_recite = df_recite_tmp.reset_index()

    df_recite = df_recite.sort_values(by='后缀序号', axis=0, ascending=True)
    print(df_recite)

    df_recite.to_csv('后缀_背诵卡.csv', index=0, encoding="utf-8")


if __name__ == '__main__':
    export_pdf()

    制作背诵卡()

    # tst_parse_词性分类1()
    # tst_parse_词性分类2()
    # tst_parse_词性分类3()
    # tst_parse_词性分类4()
    #
    # tst_parse_词根词缀拆解1()
    # tst_parse_词根词缀拆解2()
    # tst_parse_词根词缀拆解3()
    #
    # tst_parse_后缀()
    # tst_parse_后缀2()

    # tst_parse_后缀含义()
    # tst_parse_后缀含义2()
    # tst_parse_后缀含义3()

    #
    # tst_parse_word()
    # tst_parse_word2()
    # tst_parse_word3()
    # tst_parse_word4()
    # tst_parse_word5()
    # tst_parse_word6()
    # tst_parse_word7()
    # tst_parse_word8()
