import codecs

CYRILLIC = 'йцукенгшщзхъфывапролджэячсмитьбю'


def hascyr(words1):
    for letter in words1.lower():
        if letter in CYRILLIC:
            return '1'
    return '0'


def has_passive(analysis1, analysis2):
    if 'страд' in analysis1 or 'страд' in analysis2:
        return '1'
    return '0'


f = codecs.open('rlc_featured_mod7.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod8.csv', 'w', 'utf-8')

f_lines = f.readlines()

newfeatures = '\tgov_w_prep\tlex_wo_conj\tortho_wo_others\tsyntax_wo_others\thaspassive\thascyrillic'


w.write(f_lines[0].rstrip() + newfeatures + '\r\n')

i = 0
for j in f_lines[0].split('\t'):
    print(j, i)
    i += 1

for line in f_lines[1:]:
    line = line.rstrip()
    data = line.split('\t')
    words1 = data[4]
    ana1 = data[91]
    ana2 = data[92]
    if data[16] == '1' or data[36] == '1':
        gov = '1'
    else:
        gov = '0'
    if data[45] == '1' and data[38] == '0':
        lex = '1'
    else:
        lex = '0'
    if data[6] == 'ortho' or data[6] == 'orpho':
        ortho = '1'
    else:
        ortho = '0'
    if data[6] == 'syntax':
        syntax = '1'
    else:
        syntax = '0'
    w.write('\t'.join(data) + '\t' +
            '\t'.join([gov, lex, ortho, syntax, has_passive(ana1, ana2), hascyr(words1)]) + '\r\n')

w.close()