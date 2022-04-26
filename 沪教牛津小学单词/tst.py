from main import parse_book, parse_unit, parse_word


def tst_parse_book():
    all_books = '''Line 7: 一年级英语上册词汇表 
	Line 104: 一年级英语下册词汇表 
	Line 203: 二年级英语上册词汇表 
	Line 291: 二年级英语下册词汇表 
	Line 379: 小学三年级上册英语单词表 
	Line 572: 三年级下册英语单词 
	Line 755: 小学四年级上册英语单词表 
	Line 1015: 小学四年级下册英语单词表 
	Line 1353: 小学五年级上册英语单词表 
	Line 1731: 小学五年级下册英语单词表 
	Line 2060: 小学六年级上册英语单词表 
	Line 2141: grade  年级    [greɪd]  
	Line 2322: 小学六年级下册英语单词表 '''

    lines = all_books.split('\n')
    print(lines)
    for line in lines:
        print(line)
        rst = parse_book(line)
        print(rst)

def tst_parse_unit():
    all_books = '''	Line 8: Unit 1-5 
	Line 37: Unit 6-9 
	Line 69: Unit 10-12 
	Line 105: Unit 1-5 
	Line 133: Unit 6-10 
	Line 163: Unit 11-12 
	Line 204: Unit 1-5 
	Line 233: Unit 6-10 
	Line 265: Unit 11-12 
	Line 292: Unit 1-3 
	Line 322: Unit 4-7 
	Line 350: Unit 8-12 
	Line 381: Unit 1-3 
	Line 416: Unit 4-5 
	Line 446: Unit6-7 
	Line 474: Unit 8-9 
	Line 503: Unit 10-11 
	Line 533: Unit 12 
	Line 573: Unit 1-2 
	Line 604: Unit 3-4 
	Line 632: Unit 5-6 
	Line 662: Unit 7-8 
	Line 692: Unit 9-10 
	Line 724: Unit 11-12 
	Line 756: Unit1 
	Line 767: Unit2 
	Line 784: Unit3 
	Line 795: Unit4 
	Line 812: Unit5 
	Line 826: Unit6 
	Line 844: Unit7 
	Line 879: Unit8 
	Line 915: Unit9 
	Line 950: Unit10 
	Line 985: Unit11 
	Line 996: Unit12 
	Line 1016: Unit1-2 
	Line 1044: Unit3 
	Line 1079: Unit4 
	Line 1113: Unit5 
	Line 1147: Unit6 
	Line 1185: Unit7 
	Line 1216: Unit8 
	Line 1251: Unit9 
	Line 1282: Unit10 
	Line 1292: Unit11 
	Line 1317: Unit12 
	Line 1354: Unit1 
	Line 1389: Unit2 
	Line 1423: Unit3 
	Line 1435: Unit4 
	Line 1454: Unit5 
	Line 1485: Unit6 
	Line 1518: Unit7 
	Line 1555: Unit8 
	Line 1591: Unit9 
	Line 1628: Unit10 
	Line 1663: Unit11 
	Line 1694: Unit12 
	Line 1732: Unit1 
	Line 1763: Unit2 
	Line 1798: Unit3 
	Line 1831: Unit4 
	Line 1865: Unit5 
	Line 1901: Unit6 
	Line 1913: Unit7 
	Line 1931: Unit8 
	Line 1963: Unit9 
	Line 1993: Unit10 
	Line 2031: Unit11 
	Line 2047: Unit12 
	Line 2061: Unit1 
	Line 2073: Unit2 
	Line 2092: Unit3 
	Line 2107: Unit4 
	Line 2120: Unit5-6 
	Line 2149: Unit7 
	Line 2184: Unit8 
	Line 2221: Unit9 
	Line 2258: Unit10 
	Line 2273: Unit11 
	Line 2287: Unit12 
	Line 2323: Unit1 
	Line 2359: Unit2 
	Line 2391: Unit3 
	Line 2429: Unit4 
	Line 2465: Unit5 
	Line 2499: Unit6 
	Line 2512: Unit7 
	Line 2531: Unit8 
	Line 2565: Unit9 
	Line 2602: Unit10 
	Line 2612: Unit11 
	Line 2638: Unit12 '''

    lines = all_books.split('\n')
    print(lines)
    for line in lines:
        print(line)
        rst = parse_unit(line)
        print(rst)

def tst_parse_word():
    all_books = '''pea  豌豆    [piː] 
pod  豆荚    [pɒd] 
forever  永远    [fə'revə]  
bigger  更大的    [bɪgə(r)] 
excited  兴奋的    [ɪk'saɪtɪd] 
bullet  子弹    ['bʊlɪt]  
lazy  懒惰的    ['leɪzɪ] 
roof  屋顶    [ruːf]  
yard  院子    [jɑːd] 
hit  碰撞；撞击    [hɪt]  
see the world  见世面 
one by one  一个接一个地 
look out of  往外看 
(be) weak in  不擅长 
north  北方；向北[nɔːθ] 
woof  （狗叫声）汪汪  [wʊf] 
no    不  ，不是    [nəʊ]         
are    是（复数）[ɑ:(r)]        
fine    健康的；身体很好的    [faɪn]     
goodbye    再见      [gʊd'baɪ]            
hi  （用于打招呼）喂，嗨      [haɪ] 
skip(跳绳)    [skɪp] 
ride a bicycle(骑自行车) 
salad(沙拉)    ['sæləd] 
carrot(胡萝卜)    ['kærət]  '''

    lines = all_books.split('\n')
    print(lines)
    for line in lines:
        print(line)
        rst = parse_word(line)
        print(rst)

def tst_parse_word2():
    all_books = '''salad(沙拉)    ['sæləd] 
carrot(胡萝卜)    ['kærət]  '''

    lines = all_books.split('\n')
    print(lines)
    for line in lines:
        print(line)
        rst = parse_word(line)
        print(rst)

def tst_parse_word3():
    all_books = '''get…in 收割 
    far away from… 远离…
    warm-up 准备活动；热身练习
    O`clock …点钟
    a.m 上午
    play ping-pong(打乒乓球)
jack-o’-lantern 南瓜灯 ['læ ntən]'''

    lines = all_books.split('\n')
    print(lines)
    for line in lines:
        print(line)
        rst = parse_word(line)
        print(rst)

if __name__ == '__main__':
    # tst_parse_book()
    # tst_parse_unit()
    # tst_parse_word()
    # tst_parse_word2()
    tst_parse_word3()
