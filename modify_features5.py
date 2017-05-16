import codecs

SOMETHING = {'brev': ['кр', 'полн'],
             'gender': ['муж', "жен", "сред"],
             'num': ['мн', "ед"],
             'pers': ['1-л', "2-л", "3-л"]}


def samesomething(analysis1, analysis2, something):
    for element in SOMETHING[something]:
        if element in analysis1 and element in analysis2:
            return '1'
    return '0'

f = codecs.open('rlc_featured_mod5.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod6.csv', 'w', 'utf-8')

f_lines = f.readlines()

newfeatures = '\tsamebrev\tsamegender\tsamenum\tsamepers'

w.write(f_lines[0].rstrip() + newfeatures + '\r\n')

for line in f_lines[1:]:
    line = line.rstrip()
    data = line.split('\t')
    analysis1 = data[-3]
    analysis2 = data[-2]
    w.write(line + '\t' + '\t'.join([samesomething(analysis1, analysis2, 'brev'),
                                     samesomething(analysis1, analysis2, 'gender'),
                                     samesomething(analysis1, analysis2, 'num'),
                                     samesomething(analysis1, analysis2, 'pers')]) + '\r\n')

w.close()