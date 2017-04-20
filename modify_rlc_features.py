import codecs
from rlc_add_features import leven, lemma, gramm, stemming, length, bastard, pos
from pymystem3 import Mystem
import snowballstemmer
import re

reg = re.compile('=.*?([ !])')

stemmer = snowballstemmer.stemmer('russian')
m = Mystem()


def tab_in_sent(line):
    data = line.split('\t')
    analysis1 = m.analyze(data[5])
    analysis2 = m.analyze(data[6])
    new_data = [None for i in range(16)]
    new_data[0] = data[0]
    new_data[1] = data[1] + data[2]
    new_data[2] = data[3]
    new_data[3] = data[4]
    new_data[4] = data[5]
    new_data[5] = data[6]
    new_data[6] = data[7]
    new_data[7] = str(leven(new_data[4], new_data[5]))
    new_data[8] = str(lemma(analysis1, analysis2))
    new_data[9] = str(gramm(analysis1, analysis2))
    new_data[10] = str(stemming(new_data[4], new_data[5]))
    new_data[11] = str(length(new_data[4]))
    new_data[12] = str(length(new_data[5]))
    new_data[13] = str(bastard(analysis1))
    new_data[14] = pos(analysis1)
    new_data[15] = pos(analysis2)
    return new_data

def longline(line):
    data = line.rstrip().split('\t')
    newdata = [None for i in range(16)]
    newdata[5] = ' '.join(data[5:-10])
    newdata[0] = data[0]
    newdata[1] = data[1]
    newdata[2] = data[2]
    newdata[3] = data[3]
    newdata[4] = data[4]
    newdata[6] = data[-10]
    newdata[7] = data[-9]
    newdata[8] = data[-8]
    newdata[9] = data[-7]
    newdata[10] = data[-6]
    newdata[11] = data[-5]
    newdata[12] = data[-4]
    newdata[13] = data[-3]
    newdata[14] = data[-2]
    newdata[15] = data[-1]
    return newdata


def clearpos(posline):
    posline = posline + '!'
    posline = '"' + reg.sub('\1', posline)
    posline = posline[:-1] + '"'
    posline = posline.replace('  ', ' ').replace('" ', '"').replace(' "', '"')
    return posline

# print(len('60731	По словам преме Министра Греции, анти-росисскый санкци есть негативни послицвия для торговлых отнашении между Россей и Евросоюзом. 6.	«	7	7	росисскый	российские	Ortho, AgrNum	9	0	0	0	1	1	1	 	 \r\n'.split('\t')))
# a = tab_in_sent('60731	По словам преме Министра Греции, анти-росисскый санкци есть негативни послицвия для торговлых отнашении между Россей и Евросоюзом. 6.	«	7	7	росисскый	российские	Ortho, AgrNum	9	0	0	0	1	1	1	 	 \r\n')
# for k in a:
#     print(k)

f = codecs.open('rlc_features.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod.csv', 'w', 'utf-8')
first = True
for line in f:
    lin = line.rstrip()
    lin = lin.replace('"', '')
    if first:
        first = False
        w.write(lin + '\r\n')
        continue
    data = lin.split('\t')
    dat = line.replace('"', '').split(('\t'))
    if len(dat) > 16:
        if len(dat) > 17:
            data = longline(line)
            # print(line)
        else:
            data = tab_in_sent(line + '\r\n')
    data[1] = '"' + data[1] + '"'
    data[4] = '"' + data[4] + '"'
    data[5] = '"' + data[5] + '"'
    data[6] = '"' + data[6] + '"'
    try:
        data[14] = clearpos(data[14])
    except IndexError:
        data.append('""')
    try:
        data[15] = clearpos(data[15])
    except IndexError:
        if data[7] == '1' or data[7] == '0':
            # print(line)
            continue
        data.append('""')
    w.write('\t'.join(data) + '\r\n')
f.close()
w.close()