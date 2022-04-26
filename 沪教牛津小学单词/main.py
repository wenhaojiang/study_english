import re

import pdfplumber
from pandas import DataFrame


def parse_book(line):
    pattern_grade_term = r'([一二三四五六])年级.*([上下])册'
    search_objs = re.search(pattern_grade_term, line)
    if search_objs:
        grade = search_objs.group(1)
        # print(grade)
        term = search_objs.group(2)
        # print(term)
        return f'{grade}年级{term}册'
    else:
        return None

def parse_unit(line):
    pattern_unit = r'Unit ?([0-9]{1,2}(-[0-9]{1,2})?)'
    search_objs = re.search(pattern_unit, line)
    if search_objs:
        unit = search_objs.group(1)
        return f'Unit{unit}'
    else:
        return None

def parse_word(line):
    if '[' in line:
        pattern_word = r'([a-zA-Z \(\)…\-\.’`]+)(.*)(\[.+\])'
        search_objs = re.search(pattern_word, line)
        if search_objs:
            word_english = search_objs.group(1)
            word_chinese = search_objs.group(2)
            word_yinbiao = search_objs.group(3)
            word_english, word_chinese, word_yinbiao = word_english.strip(), word_chinese.strip(), word_yinbiao.strip()
            if word_english[-1] == '(':
                word_english = word_english[:-1]
                word_chinese = '(' + word_chinese
            if word_chinese[0] in ['(', '（'] and word_chinese[-1] in [')', '）']:
                word_chinese = word_chinese[1:-1]
            return (word_english, word_chinese, word_yinbiao)
        else:
            return None
    else:
        pattern_word = r'([a-zA-Z \(\)…\-\.’`]+)(.*)'
        search_objs = re.search(pattern_word, line)
        if search_objs:
            word_english = search_objs.group(1)
            word_chinese = search_objs.group(2)
            word_yinbiao = ''
            word_english, word_chinese, word_yinbiao = word_english.strip(), word_chinese.strip(), word_yinbiao.strip()
            if word_english[-1] == '(':
                word_english = word_english[:-1]
                word_chinese = '(' + word_chinese
            if word_chinese[0] in ['(', '（'] and word_chinese[-1] in [')', '）']:
                word_chinese = word_chinese[1:-1]
            return (word_english, word_chinese, word_yinbiao)
        else:
            return None

def read_pdf():
    g_book = None
    g_unit = None
    g_words = None
    g_lst_word = []
    with pdfplumber.open("沪教牛津版小学一至六年级英语单词.pdf") as pdf:
        # first_page = pdf.pages[0]  #获取第一页
        # print(first_page.chars[0])

        page_count = len(pdf.pages)
        print(page_count)  # 得到页数
        for page in pdf.pages:
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

                book = parse_book(line)
                if book is not None:
                    g_book = book
                    continue

                unit = parse_unit(line)
                if unit is not None:
                    g_unit = unit
                    continue

                words = parse_word(line)
                if words is not None:
                    g_words = words
                    g_lst_word.append({'单词': g_words[0], '中文释义': g_words[1], '音标': g_words[2], '学期': g_book, '单元': g_unit})
                    continue
                else:
                    print(f"无法解析{line}")

    pd_book = DataFrame(g_lst_word)
    pd_book.to_csv('小学单词.csv', encoding="utf-8")

if __name__ == '__main__':
    read_pdf()



