import re

print('=======正则表达式替换=======')
# 2用正则表达式来完成替换:
c1 = 'hello world'
strinfo = re.compile('world')
d1 = strinfo.sub('python', c1)
print('1原始字符串:{}'.format(c1))
print('1替换字符串:{}'.format(d1))

c2 = 'hello world world world World'
strinfo = re.compile('world')
d2 = strinfo.sub('python', c2, )
print('2原始字符串:{}'.format(c2))
print('2替换字符串:{}'.format(d2))

c2_1 = 'hello world world world World'
strinfo = re.compile('world')
d2_1 = strinfo.sub('python', c2_1, 2)  # 只替换2次
print('2_1原始字符串:{}'.format(c2_1))
print('2_1替换字符串:{}'.format(d2_1))

c2_2 = 'hello world world world World'
strinfo = re.compile('world', re.I)  # re.I 表示忽略大小写
d2_2 = strinfo.sub('python', c2_2)
print('2_2原始字符串:{}'.format(c2_2))
print('2_2替换字符串:{}'.format(d2_2))

print('*****替换特殊字符*****')
c3 = 'Hello-world\hello/python:World*Python?555"666<777>888|999OK'
strinfo = re.compile('[/:*?"<>|\\\\]')  # 注意用4个\\\\来替换\
d3 = strinfo.sub('_', c3)
print('3原始字符串:{}'.format(c3))
print('3替换字符串:{}'.format(d3))

c4 = 'Hello-world\hello/python:World*Python?555"666<777>888|999OK'
strinfo = re.compile(r'[/:*?"<>|\\]')  # 加r,2个\即可
d4 = strinfo.sub('_', c4)
print('4原始字符串:{}'.format(c4))
print('4替换字符串:{}'.format(d4))

import re


# 将匹配的数字乘以 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)


s = 'A23G4HFD567'
print(re.sub('(?P<value>\d+)', double, s))

# 一次完成多个字符串替换

# 利用正则表达式re的sub方法

import re


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return rx.sub(one_xlat, text)  # 每遇到一次匹配就会调用回调函数

# 把key做成了 |分割的内容，也就是正则表达式的OR
map1 = {'1': '2', '3': '4', }
print('|'.join(map(re.escape, map1)))

str = '1133'
print(multiple_replace(str, map1))
