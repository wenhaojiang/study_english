import os
import logging


def change_words(sentence, name):
    sentence_depart = sentence.split(' ', 1)
    words = sentence_depart[0]
    trans = sentence_depart[1]
    words_line = "<item> <word>{}</word>\r<trans> " \
                 "<![CDATA[{}]]></trans>\r<tags>{}</tags>" \
                 "\r</item>\r".format(words, trans, name)
    return words_line


fileDir = "./"
fileFormat = ".txt"
input_file = "考研单词.txt"
ouput_file = "none.xml"
head = "<wordbook>"
file_name = ''
logging.basicConfig(level=logging.DEBUG)
for root, dirs, files in os.walk(fileDir):
    for item in files:
        if item.find(fileFormat) != -1:
            input_file = item
            file_name = item.split('.')[0]
            ouput_file = file_name + ".xml"
            logging.info(ouput_file)
            break
inputs = open(input_file, 'r', encoding='utf-8')
outputs = open(ouput_file, 'w', encoding='utf-8')
for item in inputs:
    head += change_words(item, file_name)
head += "</wordbook>"
outputs.write(head)
outputs.close()
inputs.close()