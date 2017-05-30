import codecs
import Levenshtein

VOWELS = 'уеыаоэяиюё'

POS = {'PRO': [65, 69, 60],
       'A': [59, 63, 69],
       'ADV': [64, 60],
       'INTJ': [70, 67],
       'S': [66, 65],
       'NUM': [63, 72],
       'PART': [61],
       'CONJ': [62],
       'V': [68],
       'PR': [71]}


def cons_lev(words1, words2):
    words1 = words1.lower()
    words2 = words2.lower()
    for vowel in VOWELS:
        words1 = words1.replace(vowel, '')
        words2 = words2.replace(vowel, '')
    return Levenshtein.distance(words1, words2)


def j_pos(data, pl=0):
    pos1 = []
    for pos in POS:
        got = False
        for i in POS[pos]:
            if data[i + pl] == '1':
                pos1.append('1')
                got = True
                break
        if got:
            continue
        pos1.append('0')

    return pos1

f = codecs.open('rlc_featured_mod6.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod7.csv', 'w', 'utf-8')

f_lines = f.readlines()

newfeatures = '\tlevenstein_consonants\t'

j_poses = [pname + '_j1' for pname in POS] + [pname + '_j2' for pname in POS]

w.write(f_lines[0].rstrip() + newfeatures + '\t'.join(j_poses) + '\r\n')

i = 0
for j in f_lines[0].split('\t'):
    print(j, i)
    i += 1

for line in f_lines[1:]:
    line = line.rstrip()
    data = line.split('\t')
    words1 = data[4]
    words2 = data[5]
    if int(data[11]) > 1 and int(data[12]) > 1:
        for i in [8, 9, 10]:
            data[i] = '-1'
    pos1 = j_pos(data)
    pos2 = j_pos(data, pl=14)
    w.write('\t'.join(data) + '\t' + str(cons_lev(words1, words2)) + '\t' +
            '\t'.join(pos1) + '\t' + '\t'.join(pos2) + '\r\n')

w.close()