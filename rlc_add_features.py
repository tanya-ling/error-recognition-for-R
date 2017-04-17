import codecs
from pymystem3 import Mystem
import snowballstemmer
import Levenshtein

stemmer = snowballstemmer.stemmer('russian')
m = Mystem()

def leven(words1, words2):
    return Levenshtein.distance(words1, words2)


def lemma(analysis1, analysis2):
    try:
        lemma1 = analysis1[0]['analysis'][0]['lex']
        lemma2 = analysis2[0]['analysis'][0]['lex']
    except IndexError:
        print('Index error in lemma', analysis1, analysis2)
        return 0
    except KeyError:
        print('Key error in lemma', analysis1, analysis2)
        return 0
    if lemma1 == lemma2:
        return 1
    return 0


def gramm(analysis1, analysis2):
    try:
        gram1 = analysis1[0]['analysis'][0]['gr'].split(',')[1:]
        gram2 = analysis2[0]['analysis'][0]['gr'].split(',')[1:]
        if gram1 == gram2:
            return 1
        return 0
    except IndexError:
        print('Index error in gramm ', analysis1, analysis2)
        return 0
    except KeyError:
        print('Key error in gramm ', analysis1, analysis2)
        return 0


def length(words):
    if words == '':
        return 0
    return len(words.split(' '))


def bastard(analysis):
    try:
        if 'qual' in analysis[0]['analysis']:
            if analysis[0]['analysis']['qual'] == 'bastard':
                return 0
    except:
        print('bastard error ', analysis)
        return 1
    return 1


def pos(analysis1):
    pos1 = ''
    for word in analysis1:
        pos1 += ' '
        if 'analysis' in word:
            try:
                pos1 += word['analysis'][0]['gr'].split(',')[0]
            except IndexError:
                print('Index error in pos', analysis1, word)
    return pos1[1:]


def stemming(word1, word2):
    stem1 = stemmer.stemWord(word1)
    stem2 = stemmer.stemWord(word2)
    if stem1 == stem2:
        return 1
    return 0


f = codecs.open('rlc_db.csv', 'r', 'utf-8')
w = codecs.open('rlc_features.csv', 'a', 'utf-8')
# w.write('sentid	sent	start	finish	error	correction	tag\tlevenstein\tlemmaequal\tgrammequal\tstemequal\t'
#         'lenorig\tlencorr\tbastard\tpos1\tpos2\r\n')

first = True
for line in f:
    data = line.rstrip().split('\t')
    if first:
        if data[0] == '3710':
            first = False
        else:
            continue
    try:
        words1 = data[4]
        words2 = data[5]
    except IndexError:
        print('Index Error in data reading', data)
        continue
    # print('here are the boys', words1,'-----', words2, ' !')
    levenstein = leven(words1, words2)
    analysis1 = m.analyze(words1)
    analysis2 = m.analyze(words2)
    lenorig = length(words1)
    lencorr = length(words2)
    if lencorr == 1 and lenorig == 1:
        lemmaequal = lemma(analysis1, analysis2)
        grammequal = gramm(analysis1, analysis2)
        stemequal = stemming(words1, words2)
        bast = bastard(analysis1)
    else:
        bast = 0
        stemequal = 0
        grammequal = 0
        lemmaequal = 0
    pos1 = pos(analysis1)
    pos2 = pos(analysis2)
    w.write('\t'.join([line.rstrip(), str(levenstein), str(lemmaequal), str(grammequal), str(stemequal),
        str(lenorig), str(lencorr), str(bast), pos1, pos2]) + '\r\n')
f.close()
w.close()
