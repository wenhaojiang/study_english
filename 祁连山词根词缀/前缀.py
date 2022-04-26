import re

import pandas as pd
import pdfplumber
from pandas import DataFrame


def parse_方向(line):
    pattern = r'第[一二三四五]{1}节 +(表示(.{4})的|其他)前缀'
    search_objs = re.search(pattern, line)
    if search_objs:
        方向 = search_objs.group(1)
        if 方向 != '其他':
            方向 = search_objs.group(2)
        print(f'方向：{方向}')
        return 方向
    else:
        return None


def tst_parse_方向1():
    rst = parse_方向('第二节 表示数量方向的前缀')
    print(rst)
    assert rst == '数量方向'


def tst_parse_方向2():
    rst = parse_方向('第五节 其他前缀')
    print(rst)
    assert rst == '其他'


def tst_parse_方向3():
    # [一-五]不能匹配六
    rst = parse_方向('第六节 其他前缀')
    print(rst)
    assert rst is None


def tst_parse_方向4():
    # [一-五]不能匹配六
    rst = parse_方向('第四节 表示否定方向的前缀')
    print(rst)
    assert rst == '否定方向'


def parse_前缀(line):
    pattern = r'([0-9]{2}).? ([a-zA-Z\-\(\)/ ,.]+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        序号 = search_objs.group(1)
        # print(grade)
        前缀 = search_objs.group(2)
        print(f'序号：{序号}，前缀：{前缀}')
        return (序号, 前缀)
    else:
        return None


def tst_parse_前缀():
    line = '11 under-'
    rst = parse_前缀(line)
    print(rst)
    assert rst == ('11', 'under-')


def tst_parse_前缀2():
    line = '12. out-'
    rst = parse_前缀(line)
    print(rst)
    assert rst == ('12', 'out-')


def parse_word(line):
    # '  bicycle /ˈbaɪsɪkəl/ n. 自行车'
    # 注意：这里对音标的匹配，使用了非贪婪模式.+?，只匹配第一个音标
    pattern = r' +([a-zA-Z\-]+) ?英?(/.+?/) (.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        单词 = search_objs.group(1)
        # print(grade)
        音标 = search_objs.group(2)
        中文释义 = search_objs.group(3)

        # 如果中文释义中有音标，要剔除掉
        中文释义 = re.sub(r'(/.+?/)', '', 中文释义)
        # 如果有多个连续的空格，只保留一个
        中文释义 = re.sub(r'(\s{2,})', ' ', 中文释义)

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


def parse_前缀含义(line):
    pattern = r'前缀含义：(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        前缀含义 = search_objs.group(1)
        print(f'前缀含义：{前缀含义}')
        return 前缀含义
    else:
        return None


def parse_词根词缀拆解(line):
    # 词根词缀拆解：前缀 bi-双+plane 飞机
    # 词根词缀释义：前缀 ant-相反+Arctic 北极→与北极相反的
    pattern = r'词根词缀(拆解|释义|)： *(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        词根词缀拆解 = search_objs.group(2)
        print(f'词根词缀拆解：{词根词缀拆解}')
        return 词根词缀拆解
    else:
        return None


def tst_parse_词根词缀拆解1():
    rst = parse_词根词缀拆解('词根词缀拆解：前缀 bi-双+plane 飞机')
    print(rst)
    assert rst == '前缀 bi-双+plane 飞机'


def tst_parse_词根词缀拆解2():
    rst = parse_词根词缀拆解('词根词缀释义：前缀 ant-相反+Arctic 北极→与北极相反的')
    print(rst)
    assert rst == '前缀 ant-相反+Arctic 北极→与北极相反的'


def tst_parse_词根词缀拆解3():
    rst = parse_词根词缀拆解('词根词缀：前缀 ap-去+position 位置')
    print(rst)
    assert rst == '前缀 ap-去+position 位置'


def parse_页码(line):
    # 词根词缀拆解：前缀 bi-双+plane 飞机
    # 词根词缀释义：前缀 ant-相反+Arctic 北极→与北极相反的
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

    direct = parse_方向(line)
    if direct is not None:
        g_direct = direct
        return

    prefix = parse_前缀(line)
    if prefix is not None:
        g_prefix_idx, g_prefix = prefix[0], prefix[1]
        return

    prefix_mean = parse_前缀含义(line)
    if prefix_mean is not None:
        g_prefix_mean = prefix_mean

        # 保留下前一行，可能需要与后一行合并，有些语句超过了一行
        g_pre_line = line
        return

    words = parse_word(line)
    if words is not None:
        g_dct_words = {'方向': g_direct, '前缀序号': g_prefix_idx, '前缀': g_prefix, '前缀含义': g_prefix_mean, '单词': words[0], '音标': words[1], '中文释义': words[2]}
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
            # 前缀从第5页到第23页
            if page.page_number < 5:
                continue

            if page.page_number > 23:
                break

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
    pd_book.to_csv('前缀.csv', index=0, encoding="utf-8")


def 制作背诵卡():
    df_book = pd.read_csv('前缀.csv', encoding="utf-8", index_col=0)
    sr_recite_tmp = df_book.groupby(['方向', '前缀序号', '前缀', '前缀含义']).apply(lambda df: df['单词'].str.cat(sep='  '))
    # print(sr_recite_tmp)
    df_recite_tmp = sr_recite_tmp.to_frame('单词')
    df_recite = df_recite_tmp.reset_index()

    df_recite = df_recite.sort_values(by='前缀序号', axis=0, ascending=True)
    print(df_recite)

    df_recite.to_csv('前缀_背诵卡.csv', index=0, encoding="utf-8")


if __name__ == '__main__':
    export_pdf()

    # 制作背诵卡()

    # tst_parse_方向1()
    # tst_parse_方向2()
    # tst_parse_方向3()
    # tst_parse_方向4()
    #
    # tst_parse_词根词缀拆解1()
    # tst_parse_词根词缀拆解2()
    # tst_parse_词根词缀拆解3()
    #
    # tst_parse_前缀()
    # tst_parse_前缀2()
    #
    # tst_parse_word()
    # tst_parse_word2()
    # tst_parse_word3()
    # tst_parse_word4()
    # tst_parse_word5()
