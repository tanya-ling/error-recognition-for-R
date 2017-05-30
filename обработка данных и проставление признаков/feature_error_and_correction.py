from pymystem3 import Mystem
import snowballstemmer
import Levenshtein
import re
import codecs

def get_list(filename):
    k_f = codecs.open(filename, 'r', 'utf-8')

    words = []
    for line in k_f:
        line = line.rstrip()
        if line != '' and '_' not in line:
            word = line.split(' ')[0].lower()
            if word not in words:
                words.append(word)
    k_f.close()
    return words

words = get_list('tf-idr-error.txt')
words_c = get_list('tf-idr-correction.txt')

reg = re.compile('=.*?([ !])')
stemmer = snowballstemmer.stemmer('russian')
m = Mystem()
LETTERS = 'ETAOINSHRDLCUMWFGYPBVKXJQZ'
CYRILLIC = 'йцукенгшщзхъфывапролджэячсмитьбю'
d = {}
poslist = 'A ADVPRO PART CONJ ANUM ADV SPRO S COM V APRO INTJ PR NUM'.split(' ')
j = 0
for i in poslist:
    d[i] = j
    j += 1
SOMETHING = {'brev': ['кр', 'полн'],
             'gender': ['муж', "жен", "сред"],
             'num': ['мн', "ед"],
             'pers': ['1-л', "2-л", "3-л"]}
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
for p in POS:
    POS[p] = [i - 59 for i in POS[p]]


def main(words1, words2):
    analysis1 = m.analyze(words1)
    analysis2 = m.analyze(words2)

    analysis1_text = analysisstring(analysis1)
    analysis2_text = analysisstring(analysis2)

    features = []
    features.append(Levenshtein.distance(words1, words2))

    lenorig = length(words1)
    lencorr = length(words2)
    if lencorr == 1 and lenorig == 1:
            lemmaequal = lemma(analysis1, analysis2)
            grammequal = gramm(analysis1, analysis2)
            stemequal = stemming(words1, words2)
            bast = bastard(analysis1)
    else:
            bast = -1
            stemequal = -1
            grammequal = -1
            lemmaequal = -1
    pos1 = clearpos(pos(analysis1)).replace('', '')[1:-1].split(' ')
    pos2 = clearpos(pos(analysis2)).replace('', '')[1:-1].split(' ')

    features += [lemmaequal, grammequal, stemequal, lenorig, lencorr, bast]
    features += [hyphen(words1, words2), graph(words1), neg(words1, words2), space(words1, words2)]
    features.append(hasaux(analysis1, analysis2))
    features += [samesomething(analysis1_text, analysis2_text, 'brev'),
                                     samesomething(analysis1_text, analysis2_text, 'gender'),
                                     samesomething(analysis1_text, analysis2_text, 'num'),
                                     samesomething(analysis1_text, analysis2_text, 'pers')]

    features.append(cons_lev(words1, words2))

    arr = ['0' for i in poslist]
    arr2 = ['0' for i in poslist]
    for i in pos1:
        if i in d:
            arr[d[i]] = '1'
    for i in pos2:
        if i in d:
            arr2[d[i]] = '1'

    pos1 = j_pos(arr)
    pos2 = j_pos(arr2)
    features += pos1
    features += pos2
    features += [has_passive(analysis1_text, analysis2_text), hascyr(words1)]

    n_f = []
    for word in words:
        if word in words1:
            n_f.append('1')
        else:
            n_f.append('0')
    n_f_c = []
    for word in words_c:
        if word in words2:
            n_f_c.append('1')
        else:
            n_f_c.append('0')
    features += n_f + n_f_c

    return features


def hascyr(words1):
    for letter in words1.lower():
        if letter in CYRILLIC:
            return '1'
    return '0'


def has_passive(analysis1, analysis2):
    if 'страд' in analysis1 or 'страд' in analysis2:
        return '1'
    return '0'


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


def clearpos(posline):
    posline = posline + '!'
    posline = '"' + reg.sub('\1', posline)
    posline = posline[:-1] + '"'
    posline = posline.replace('  ', ' ').replace('" ', '"').replace(' "', '"')
    return posline


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
                # print('Index error in pos', analysis1, word)
                pass
    return pos1[1:]


def stemming(word1, word2):
    stem1 = stemmer.stemWord(word1)
    stem2 = stemmer.stemWord(word2)
    if stem1 == stem2:
        return 1
    return 0


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


def samesomething(analysis1, analysis2, something):
    for element in SOMETHING[something]:
        if element in analysis1 and element in analysis2:
            return '1'
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

print(main('он алтын киндергартен из стали тате петрова командировал', 'и всегда прав'))