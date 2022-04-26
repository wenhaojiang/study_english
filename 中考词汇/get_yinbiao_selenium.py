import os
import time

from selenium import webdriver

driver = None

def get_yinbiao(word: str):
    url = f"https://fanyi.baidu.com/?aldtype=85#en/zh/{word}"

    global driver
    if driver is None:
        # 获取当前文件路径
        current_path = os.path.abspath(os.path.dirname(__file__))
        chromedriver_file_pathname = os.path.join(current_path, 'chromedriver.exe')
        driver = webdriver.Chrome(executable_path=chromedriver_file_pathname)
    driver.get(url)

    time.sleep(5)

    yinbiao_html = driver.find_elements_by_class_name("phonetic-transcription")
    # print(yinbiao_html)
    for yinbiao in yinbiao_html:
        音标 = yinbiao.text
        # print(音标)

        if 音标.startswith('英 '):
            音标 = 音标.replace('英 ', '')
            return 音标

    return "没找到音标"

if __name__ == '__main__':
    音标 = get_yinbiao('walk')
    print(音标)
    音标 = get_yinbiao('joke')
    print(音标)
