import codecs
from pymystem3 import Mystem

m = Mystem()

def hasaux(analysis1, analysis2):
    for word in analysis1:
        try:
            if word['analysis'][0]['lex'] == 'быть':
                return '1'
        except KeyError:
            continue
        except IndexError:
                continue
    for word in analysis2:
        try:
            if word['analysis'][0]['lex'] == 'быть':
                return '1'
        except KeyError:
            continue
        except IndexError:
                continue
    return '0'

def analysisstring(analysis):
    string = ''
    for word in analysis:
        if 'analysis' in word:
            try:
                string += word['analysis'][0]['gr'] + ' '
            except KeyError:
                continue
            except IndexError:
                continue
    return string[:-1]


f = codecs.open('rlc_featured_mod3.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod5.csv', 'w', 'utf-8')

f_lines = f.readlines()

newfeatures = '\tgramm1\tgramm2\thasaux'

w.write(f_lines[0].rstrip() + newfeatures + '\r\n')

for line in f_lines[1:]:
    line = line.rstrip()
    data = line.split('\t')
    words1 = data[4][1:-1]
    words2 = data[5][1:-1]
    analysis1 = m.analyze(words1)
    analysis2 = m.analyze(words2)
    w.write(line + '\t' + '\t'.join([analysisstring(analysis1),
                                     analysisstring(analysis2),
                                     hasaux(analysis1, analysis2)])
            + '\r\n')


w.close()