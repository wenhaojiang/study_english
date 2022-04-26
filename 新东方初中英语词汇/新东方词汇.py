import os
import re

import pandas as pd
from pandas import DataFrame


def parse_word(line):
    # "able [ˈeɪbl]"
    # 注意：这里对音标的匹配，使用了非贪婪模式.+?，只匹配第一个音标
    pattern = r'^([a-zA-Z\-\(\)/]+) (\[.+\])$'
    search_objs = re.search(pattern, line)
    if search_objs:
        单词 = search_objs.group(1)

        音标 = search_objs.group(2)
        音标 = 音标.strip()

        print(f'单词：{单词}，音标：{音标}')
        return (单词, 音标)
    else:
        return None


def tst_parse_word():
    line = "able [ˈeɪbl]"
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('able', '[ˈeɪbl]')


def tst_parse_word2():
    # 后只有一个空格
    line = 'a/an [ə]/[ən]'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst == ('a/an', '[ə]/[ən]')

def tst_parse_word3():
    # 后只有一个空格
    line = '【派】trainer（n.训练者）；trainee [n.受训练的人（或动物）]'
    print(f'原始行数据：{line}')
    rst = parse_word(line)
    print(rst)
    assert rst is None

def parse_chinese(line):
    # "n.能力，本领；才能，才智"
    # 注意：这里对音标的匹配，使用了非贪婪模式.+?，只匹配第一个音标
    pattern = r'(n\.|adj\.|adv\.|prep\.|v\.|vt\.|vi\.|v\.aux|conj\.|art\.|num\.|int\.).+'
    search_objs = re.search(pattern, line)
    if search_objs:
        中文释义 = search_objs.group(0)
        print(f'中文释义：{中文释义}')
        # 这个词性显示出来，只做调试用。词性与中文释义是捆绑的，一个单词可能对应多个词性和意思的组合
        词性 = search_objs.group(1)
        print(f'第一个词性：{词性}')
        return 中文释义
    else:
        return None

def tst_parse_chinese():
    # 后只有一个空格
    line = 'adv./prep./conj.在…以后，在…后面'
    print(f'原始行数据：{line}')
    rst = parse_chinese(line)
    print(rst)
    assert rst == 'adv./prep./conj.在…以后，在…后面'

def tst_parse_chinese2():
    # 后只有一个空格
    line = "able [ˈeɪbl]"
    print(f'原始行数据：{line}')
    rst = parse_chinese(line)
    print(rst)
    assert rst == None

def tst_parse_chinese3():
    # 后只有一个空格
    line = "v.翻译"
    print(f'原始行数据：{line}')
    rst = parse_chinese(line)
    print(rst)
    assert rst == "v.翻译"



def parse_例句(line):
    # 词根词缀拆解：词根 bi-双+plane 飞机
    # 词根词缀释义：词根 ant-相反+Arctic 北极→与北极相反的
    pattern = r'^【例】(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        例句 = search_objs.group(1)
        print(f'例句：{例句}')
        return 例句
    else:
        return None


def tst_parse_例句1():
    rst = parse_例句('【例】I’m afraid I will be late for school.我恐怕上学要迟到了。')
    print(rst)
    assert rst == 'I’m afraid I will be late for school.我恐怕上学要迟到了。'


def tst_parse_例句2():
    rst = parse_例句('adj.害怕的，恐惧的；犯愁的')
    print(rst)
    assert rst == None


def parse_tips(line):
    if 'Tips' == line:
        return True
    else:
        return False


def tst_parse_tips():
    rst = parse_tips('Tips')
    print(rst)
    assert rst


def tst_parse_tips2():
    rst = parse_tips('【例】I’m afraid I will be late for school.我恐怕上学要迟到了。')
    print(rst)
    assert not rst


def parse_真题点评(line):
    if '真题点评' == line:
        return True
    else:
        return False


def tst_parse_真题点评():
    rst = parse_真题点评('真题点评')
    print(rst)
    assert rst


def tst_parse_真题点评2():
    rst = parse_真题点评('【例】I’m afraid I will be late for school.我恐怕上学要迟到了。')
    print(rst)
    assert not rst


def parse_固定搭配短语(line):
    pattern = r'^【搭】(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        固定搭配短语 = search_objs.group(1)
        print(f'固定搭配短语：{固定搭配短语}')
        return 固定搭配短语
    else:
        return None

def tst_parse_固定搭配短语1():
    rst = parse_固定搭配短语('【搭】after all毕竟，终究；be after追逐，想得到；soon after不久以后')
    print(rst)
    assert rst == 'after all毕竟，终究；be after追逐，想得到；soon after不久以后'


def tst_parse_固定搭配短语2():
    rst = parse_固定搭配短语('【例】I’m afraid I will be late for school.我恐怕上学要迟到了。')
    print(rst)
    assert rst == None


def parse_记忆方法(line):
    pattern = r'^【记】(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        记忆方法 = search_objs.group(1)
        print(f'记忆方法：{记忆方法}')
        return 记忆方法
    else:
        return None

def tst_parse_记忆方法1():
    rst = parse_记忆方法('【记】合成词：after（在…之后）+noon（中午）→中午之后就是下午→下午')
    print(rst)
    assert rst == '合成词：after（在…之后）+noon（中午）→中午之后就是下午→下午'


def tst_parse_记忆方法2():
    rst = parse_记忆方法('【例】I’m afraid I will be late for school.我恐怕上学要迟到了。')
    print(rst)
    assert rst == None

def parse_派生词(line):
    pattern = r'^【派】(.+)'
    search_objs = re.search(pattern, line)
    if search_objs:
        派生词 = search_objs.group(1)
        print(f'派生词：{派生词}')
        return 派生词
    else:
        return None

def tst_parse_派生词1():
    rst = parse_派生词('【派】aged（adj.…岁的；成年的）；ageing（n.成熟，变老）')
    print(rst)
    assert rst == 'aged（adj.…岁的；成年的）；ageing（n.成熟，变老）'


def tst_parse_派生词2():
    rst = parse_派生词('【例】I’m afraid I will be late for school.我恐怕上学要迟到了。')
    print(rst)
    assert rst == None

def parse_易混淆词(word, line):
    line_new = line.replace('，', ',')
    line_new = line_new.lower()
    word_new = word.lower()

    if ',' not in line_new:
        return None

    pattern = f'^[a-zA-Z, \.]*{word_new}[a-zA-Z, \.]*$'
    search_objs = re.search(pattern, line_new)
    if search_objs:
        # line = search_objs.group(0)
        print(f'易混淆词：{line}')
        return line
    else:
        return None

def tst_parse_易混淆词1():
    rst = parse_易混淆词('accident', 'accident,incident')
    print(rst)
    assert rst == 'accident,incident'


def tst_parse_易混淆词2():
    rst = parse_易混淆词('accident', 'by accident偶然，意外')
    print(rst)
    assert rst == None

def tst_parse_易混淆词3():
    rst = parse_易混淆词('able', 'be able to,can')
    print(rst)
    assert rst == 'be able to,can'

def tst_parse_易混淆词5():
    rst = parse_易混淆词('bring', 'bring forth，bring forward')
    print(rst)
    assert rst == 'bring forth，bring forward'

def tst_parse_易混淆词6():
    rst = parse_易混淆词('madam', 'Madam,Miss,Ms.')
    print(rst)
    assert rst == 'Madam,Miss,Ms.'

def tst_parse_易混淆词8():
    rst = parse_易混淆词('France', 'France,French')
    print(rst)
    assert rst == 'France,French'

def tst_parse_易混淆词9():
    rst = parse_易混淆词('nor', 'neither...nor,either...or')
    print(rst)
    assert rst == 'neither...nor,either...or'


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
    invalid_lines = ['ŋ', '必背词汇：']
    if line in invalid_lines:
        return True
    else:
        return False


g_dct_words = dict()
g_lst_word = []
g_pre_line = None
g_pre_line_性质 = None


def parse_line(line, append_line=False):
    global g_dct_words
    global g_lst_word
    global g_pre_line
    global g_pre_line_性质

    line = line.strip()
    if len(line) == 0:
        return

    if '单词' == g_pre_line_性质:
        中文释义 = parse_chinese(line)
        if 中文释义 is not None:
            g_dct_words['中文释义'] = 中文释义
            g_pre_line_性质 = '中文释义'
        else:
            # 单词下面一行必须是中文释义
            assert False
        return

    words = parse_word(line)
    if words is not None:
        # 把上一个单词加入列表中，并清空g_dct_words缓存
        if len(g_dct_words) > 0:
            g_lst_word.append(g_dct_words.copy())
            g_dct_words.clear()


        g_dct_words = {'单词': words[0], '音标': words[1]}

        # 处理完后，打上标记
        g_pre_line_性质 = '单词'
        return

    例句 = parse_例句(line)
    if 例句 is not None:
        g_dct_words['例句'] = 例句
        g_pre_line_性质 = '例句'
        return


    用法注意 = parse_tips(line)
    if 用法注意:
        g_pre_line_性质 = '用法注意'
        return

    固定搭配短语 = parse_固定搭配短语(line)
    if 固定搭配短语 is not None:
        g_dct_words['固定搭配短语'] = 固定搭配短语
        g_pre_line_性质 = '固定搭配短语'
        return

    真题点评 = parse_真题点评(line)
    if 真题点评:
        g_pre_line_性质 = '真题点评'
        return

    记忆方法 = parse_记忆方法(line)
    if 记忆方法 is not None:
        g_dct_words['记忆方法'] = 记忆方法
        g_pre_line_性质 = '记忆方法'
        return

    派生词 = parse_派生词(line)
    if 派生词 is not None:
        g_dct_words['派生词'] = 派生词
        g_pre_line_性质 = '派生词'
        return

    易混淆词 = parse_易混淆词(g_dct_words['单词'], line)
    if 易混淆词 is not None:
        g_dct_words['易混淆词'] = 易混淆词
        g_pre_line_性质 = '易混淆词'
        return

    # print(f'无法解析的行数据：{line}')
    if g_pre_line_性质 in g_dct_words:
        old = g_dct_words[g_pre_line_性质]
        g_dct_words[g_pre_line_性质] = f'{old}\n{line}'
    else:
        g_dct_words[g_pre_line_性质] = line
    print(f'追加后，{g_pre_line_性质}为：{g_dct_words[g_pre_line_性质]}')


folder = r'D:\蒋一山的文件\英语\新东方初中词汇\正序版单词'
# input_filename = r'WordList2.txt'

def parse_wordlist(input_filename: str):
    path_input_filename = os.path.join(folder, input_filename)
    print(path_input_filename)

    inputs = open(path_input_filename, 'r', encoding='utf-8')
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
    global g_dct_words
    global g_pre_line
    global g_pre_line_性质

    # 把最后一个单词添加进来
    if len(g_dct_words) > 0:
        g_lst_word.append(g_dct_words.copy())


    pd_book = DataFrame(g_lst_word)
    # 输出文件名，将输入文件名后缀有.txt改为.csv即可
    output_filename = input_filename[:-4] + '.csv'
    path_output_filename = os.path.join(folder, output_filename)
    pd_book.to_csv(path_output_filename, index=0, encoding="utf-8")

    # 导出后，记得将单词列表清空，以免下一课又将上一课的单词重复导入
    g_lst_word.clear()
    g_dct_words = dict()
    g_pre_line = None
    g_pre_line_性质 = None

def parse_book():
    # 遍历整个目录，把所有
    for root, dirs, files in os.walk(folder, topdown=False):
        for input_filename in files:
            print(os.path.join(root, input_filename))
            if not input_filename.endswith('.txt'):
                continue

            parse_wordlist(input_filename)

def combine_book():
    lst_df_recite = []
    for i in range(1, 33):
        filename = f'WordList{i}.csv'
        print(filename)
        path_input_filename = os.path.join(folder, filename)
        df_wordlist = pd.read_csv(path_input_filename, encoding="utf-8")
        df_concise = df_wordlist[['单词', '音标', '中文释义', '记忆方法', '例句']].copy()
        df_concise['Lesson'] = f'L{i}'
        # print(df_concise)
        lst_df_recite.append(df_concise)

    df_recite = pd.concat(lst_df_recite)
    df_recite['序号'] = range(1, 1+len(df_recite))
    df_recite['序号'] = df_recite['序号'].astype(str) + '_' + df_recite['Lesson']
    df_recite = df_recite[['序号', '单词', '音标', '中文释义', '记忆方法', '例句']]
    path_output_filename = os.path.join(folder, '全书背诵.csv')
    df_recite.to_csv(path_output_filename, index=0, encoding="utf-8")
    print(f'所有单词整合到了 {path_output_filename} 文件中')

def tst_all_testcase():

    # tst_parse_word()
    # tst_parse_word2()
    # tst_parse_word3()
    #
    # tst_parse_chinese()
    # tst_parse_chinese2()
    # tst_parse_chinese3()
    #
    # tst_parse_例句1()
    # tst_parse_例句2()
    #
    # tst_parse_tips()
    # tst_parse_tips2()
    #
    # tst_parse_固定搭配短语1()
    # tst_parse_固定搭配短语2()
    #
    # tst_parse_真题点评()
    # tst_parse_真题点评2()
    #
    # tst_parse_记忆方法1()
    # tst_parse_记忆方法2()
    #
    # tst_parse_派生词1()
    # tst_parse_派生词2()

    tst_parse_易混淆词1()
    tst_parse_易混淆词2()
    tst_parse_易混淆词3()
    tst_parse_易混淆词5()
    tst_parse_易混淆词6()
    tst_parse_易混淆词8()
    tst_parse_易混淆词9()

if __name__ == '__main__':
    # parse_wordlist('WordList30.txt')

    # parse_book()

    combine_book()

    # tst_all_testcase()

