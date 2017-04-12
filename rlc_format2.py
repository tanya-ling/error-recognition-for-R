# -*- coding: utf-8 -*-

import codecs
import ast


S = codecs.open('C:\\Tanya\\НИУ ВШЭ\\диплом\\rlc\\annotator_sentence.csv', 'r', 'utf-8')
SENTENCES = {}
for line in S:
    line = line.rstrip().split(';')
    SENTENCES[line[0][1: -1]] = line[1][1: -1]


def get_data(string):
    strong = string.split(';')
    try:
        sent_ind = strong[2][1: -1]
    except IndexError:
        print(string)
        return
    sent = SENTENCES[sent_ind]
    correct = strong[-1][1: -1]
    if correct == 'UL':
        strong = string.replace('""', '"').replace('false', 'False').replace('true', 'True').split(';')
        dic = strong[6][1: -1]
        try:
            dic = ast.literal_eval(dic)
        except SyntaxError:
            w2.write('\t'.join([sent_ind, sent, '?', '?', '?', '?', '?']) + '\r\n')
            return
        orig = dic['quote'].replace('u', '\\u')
        try:
            orig = ast.literal_eval('"' + orig + '"')
        except SyntaxError:
            orig = orig.replace('\\', '')
        correct = dic['corrs'].replace('u', '\\u')
        correct = ast.literal_eval('"' + correct + '"')
        finish = dic['ranges'][0]['end'][6: -1]
        start = dic['ranges'][0]['start'][6: -1]
        tags = ', '.join(dic['tags'])
    else:
        orig = strong[-2][1: -1]
        finish = strong[-5][1: -1]
        start = strong[-6][1: -1]
        tags = strong[-7][1: -1]
    w.write('\t'.join([sent_ind, sent, start, finish, orig, correct, tags]) + '\r\n')

w = codecs.open('rlc_db.csv', 'w', 'utf-8')
w.write('sentid\tsent\tstart\tfinish\terror\tcorrection\ttag\r\n')
get_data('"18317";"80";"61119";"3d0dc5ef-cfd1-4e1e-ae5d-ea14cb5f3bb2";"2016-07-13 09:57:32";"2016-07-13 09:57:32";"{""corrs"": ""\u043f\u043e\u043b\u0447\u0430\u0441\u0430"", ""quote"": ""\u043f\u043e\u043b   \u0447\u0430\u0441\u0430."", ""text"": """", ""ranges"": [{""start"": ""/span[3]"", ""end"": ""/span[4]"", ""startOffset"": 0, ""endOffset"": 5}], ""tags"": [""Space""]}";"Space";"3";"4";"0";"5";"пол   часа.";"полчаса"')
get_data('"2118";NULL;"19055";"7ef3d262-106e-4549-b7da-68c50f2c1a75";"2015-07-08 02:47:55";"2015-07-08 02:47:55";"{""corrs"": """", ""tags"": [""orpho""], ""quote"": ""u041fu0435u043du0441u0438u043bu0432u0430u043du0438u044f"", ""ranges"": [{""start"": ""/span[7]"", ""end"": ""/span[7]"", ""startOffset"": 0, ""endOffset"": 11}], ""readonly"": false, ""text"": """"}";"orpho";"1";"1";NULL;NULL;NULL;NULL')
f = codecs.open('C:\\Tanya\\НИУ ВШЭ\\диплом\\rlc\\annotator_annotation.csv', 'r', 'utf-8')
w2 = codecs.open('rlc_db_failed.csv', 'w', 'utf-8')
for line in f:
    get_data(line.rstrip())