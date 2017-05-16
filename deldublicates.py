import codecs

LETTERS = 'ETAOINSHRDLCUMWFGYPBVKXJQZ'


def hyphen(word1, word2):
    if '-' in word1 or '-' in word2:
        return '1'
    return '0'


def graph(word1):
    lw = word1.upper()
    for letter in LETTERS:
        if letter in lw:
            return '1'
    return '0'


def neg(word1, word2):
    for word in word1.split(' '):
        if word == 'не' or word == 'ни':
            return '1'
    for word in word2.split(' '):
        if word == 'не' or word == 'ни':
            return '1'
    return '0'


def space(word1, word2):
    if word1.replace(' ', '').lower() == word2.replace(' ', '').lower():
        return '1'
    return '0'

f = codecs.open('rlc_featured_mod2.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod3.csv', 'w', 'utf-8')

f_lines = f.readlines()

d = {}
poslist = 'A ADVPRO PART CONJ ANUM ADV SPRO S COM V APRO INTJ PR NUM'.split(' ')
j = 0
for i in poslist:
    d[i] = j
    j += 1

newfeatures = '\thashyphen\thasgraph\thasneg\thasspace'

w.write(f_lines[0].rstrip() + '\t' + '\t'.join([i + '1' for i in poslist]) + '\t' +
        '\t'.join([i + '2' for i in poslist]) + newfeatures + '\r\n')

f_set = set(f_lines[1:])


for line in f_set:
    line = line.rstrip()
    data = line.split('\t')
    pos1 = data[14][1:-1].replace('', '').split(' ')
    pos2 = data[15][1:-1].replace('', '').split(' ')
    arr = ['0' for i in poslist]
    arr2 = ['0' for i in poslist]
    word1 = data[4][1:-1]
    word2 = data[5][1:-1]
    for i in pos1:
        if i in d:
            arr[d[i]] = '1'
    for i in pos2:
        if i in d:
            arr2[d[i]] = '1'
    newfeatures = '\t'.join([hyphen(word1, word2), graph(word1), neg(word1, word2), space(word1, word2)])
    w.write(line + '\t' + '\t'.join(arr) + '\t' + '\t'.join(arr2) + '\t' + newfeatures + '\r\n')

w.close()

for i in d:
    print(i, d[i])