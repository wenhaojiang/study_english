import time

import pywinauto
from pywinauto import Desktop, clipboard
from pywinauto.application import Application
from pywinauto.application import ProcessNotFoundError
import pywinauto.keyboard as kb

class GetPhoneticSymbol:
    def __init__(self):
        try:
            app = Application(backend="uia").connect(path=r"C:\Program Files (x86)\Youdao\Dict\YoudaoDict.exe")
            print('网易有道词典客户端已连接')
        except ProcessNotFoundError as ex:
            # print(ex)
            print('网易有道词典尚未启动，现在启动。。。')
            app = Application(backend="uia").start(r'C:\Program Files (x86)\Youdao\Dict\YoudaoDict.exe')
            dlg = Desktop(backend="uia")['网易有道词典']
            dlg.wait('visible')
            print('网易有道词典客户端已启动')

        self.main_dlg = Desktop(backend="uia")['网易有道词典']
        # main_dlg.draw_outline(colour='red')

    def get_phonetic_symbol(self, word):
        # 输入单词
        self._input_word(word)

        # 在界面上查询音标
        英国音标 = ''
        英国音标 = self._query_phonetic_symbol()
        return 英国音标


    def _input_word(self, word):
        # 单词输入框 = self.main_dlg.child_window(auto_id="1003", control_type="Document")

        单词输入框 = self.main_dlg.child_window(auto_id="1001", control_type="Edit")


        单词输入框.draw_outline(colour='red')
        print('aaa')
        单词输入框.print_control_identifiers()
        print('bbb')
        # 单词输入框.click()
        word1 = 单词输入框.texts()
        单词输入框.set_edit_text(word)
        单词输入框.type_keys(word)

        # 单词输入框.set_focus()
        # 单词输入框.type_keys(word)
        #
        #
        # location = 单词输入框.rectangle()
        # center = (int((location.left + location.right) / 2), int((location.top + location.bottom) / 2))
        # pywinauto.mouse.double_click(button='left', coords=center)
        # time.sleep(1)
        # # 单词输入框.texts([word])
        # # 单词输入框.type_keys(word)
        #
        #
        # pywinauto.keyboard.send_keys(word)
        # time.sleep(1)

    def _query_phonetic_symbol(self):
        # position_menu = main_dlg.child_window(title="英", control_type="UIA_EditControlTypeId")
        英国音标标志 = self.main_dlg.child_window(title="英", control_type="Edit")
        英国音标标志.draw_outline(colour='red')
        print('aaa')
        英国音标标志.print_control_identifiers()
        print('bbb')

        parent_英国音标标志 = 英国音标标志.parent()
        all_ctrls = parent_英国音标标志.descendants()

        print('ccc')
        # 英国音标 = main_dlg.child_window(title="/dʒəʊk/", control_type="Edit")
        英国音标控件 = all_ctrls[1]
        英国音标控件.draw_outline(colour='red')
        英国音标 = 英国音标控件.texts()[0]
        print(f'英国音标：{英国音标}')
        # 英国音标.print_control_identifiers()
        print('ddd')
        return 英国音标

    def _type_edit_control_keys(self, control_id, text):
        if not self._editor_need_type_keys:
            self._main.child_window(
                control_id=control_id, class_name="Edit"
            ).set_edit_text(text)
        else:
            editor = self._main.child_window(control_id=control_id, class_name="Edit")
            editor.select()
            editor.type_keys(text)

if __name__ == '__main__':
    obj = GetPhoneticSymbol()
    英国音标 = obj.get_phonetic_symbol('make')
    print(f'英国音标：{英国音标}')
