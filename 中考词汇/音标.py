import json
import os

import pandas as pd
from pandas import DataFrame

from get_yinbiao_selenium import get_yinbiao


class PhoneticSymbol:
    def __init__(self):
        self.dct_phonetic_symbol = None
        # 获取当前文件路径
        current_path = os.path.abspath(os.path.dirname(__file__))
        self.yingbiao_file_pathname = os.path.join(current_path, '音标.csv')
        print('音标文件全路径名:' + self.yingbiao_file_pathname)

    def trans_json_to_csv(self):
        filename_strategy_summary = '音标.json'
        with open(filename_strategy_summary, 'r', encoding='utf-8') as file:
            all_word_detail = json.load(file)

        print(all_word_detail)
        df_phonetic_symbol = DataFrame(all_word_detail)
        df_phonetic_symbol = df_phonetic_symbol[df_phonetic_symbol['音标'] != '没找到音标']
        print(len(df_phonetic_symbol))

        df_phonetic_symbol.to_csv(self.yingbiao_file_pathname, encoding="utf-8")

    def load_phonetic_symbol_df(self):
        df_phonetic_symbol = pd.read_csv(self.yingbiao_file_pathname, encoding="utf-8", index_col=0)
        df_phonetic_symbol = df_phonetic_symbol.drop_duplicates(['英文原型'])

        df_phonetic_symbol = df_phonetic_symbol.set_index(['英文原型'])
        self.dct_phonetic_symbol = df_phonetic_symbol.to_dict(orient='index')
        # print(self.dct_phonetic_symbol)

    def get_phonetic_symbol(self, word: str):
        if self.dct_phonetic_symbol is None:
            self.load_phonetic_symbol_df()

        # 去掉头尾的空格
        word = word.strip()

        if word in self.dct_phonetic_symbol:
            return self.dct_phonetic_symbol[word]['音标']
        else:
            音标 = get_yinbiao(word)
            print(f'上网查询结果，英文原型：{word}，音标：{音标}')
            self.dct_phonetic_symbol[word] = {'音标': 音标}
            self.append_phonetic_symbol_csv(word, 音标)
            return 音标

    def append_phonetic_symbol_csv(self, word, 音标):
        # 将新音标加到csv文件中
        df_phonetic_symbol = pd.read_csv(self.yingbiao_file_pathname, encoding="utf-8", index_col=0)
        df_phonetic_symbol = df_phonetic_symbol.append([{'英文原型': word, '音标': 音标}])
        df_phonetic_symbol.to_csv(self.yingbiao_file_pathname, encoding="utf-8")

    def find_duplicate_phonetic_symbol(self):
        df_phonetic_symbol = pd.read_csv(self.yingbiao_file_pathname, encoding="utf-8", index_col=0)
        df_phonetic_symbol = df_phonetic_symbol.drop_duplicates(['英文原型'])

        # 把音标重复的找出来，可能是取词时错误导致的
        a = df_phonetic_symbol.groupby('音标').count() > 1
        price = a[a['英文原型'] == True].index
        repeat_df = df_phonetic_symbol[df_phonetic_symbol['音标'].isin(price)]
        repeat_df = repeat_df.sort_values('音标')
        print(f"音标重复的单词：{repeat_df[['英文原型', '音标']]}")

if __name__ == '__main__':
    phonetic_symbol = PhoneticSymbol()
    # phonetic_symbol.trans_json_to_csv()
    # 将音标文件加在到缓存中
    phonetic_symbol.load_phonetic_symbol_df()

    # 查询一个缓存中已有的单词
    rst1 = phonetic_symbol.get_phonetic_symbol('word')
    print(rst1)

    # 查询一个缓存中没有的单词
    rst2 = phonetic_symbol.get_phonetic_symbol('selenium')
    print(rst2)

    # 这次在缓存中查询
    rst3 = phonetic_symbol.get_phonetic_symbol('selenium')
    print(rst3)


