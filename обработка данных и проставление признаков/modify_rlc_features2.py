import codecs

f = codecs.open('rlc_featured_mod.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod2.csv', 'w', 'utf-8')

DUMTAGS = ['not-clear', 'transp', 'subst', 'del', 'punc', 'typo', 'orpho', 'argstr', 'altern', 'reflex',
           'gender', 'miss']
GOODTAGS = ['prep', 'phon', 'graph', 'hyphen', 'space', 'ortho', 'translit', 'misspell', 'deriv', 'infl', 'num',
            'morph', 'asp', 'passive', 'agrnum', 'agrcase', 'agrgender', 'agrpers', 'agrgerund', 'transfer',
            'gov', 'ref', 'conj', 'wo', 'neg', 'aux', 'brev', 'syntax', 'constr', 'lex', 'cs', 'par', 'idiom', 'coord',
            'refl', 'insert', 'tense']


# убираем lexcalque, неясно что это;

TAGS = {}
BTAGS = {}
TAGFREQ = {}
j = 0
for tag in GOODTAGS:
    TAGS[tag] = j
    j += 1
    TAGFREQ[tag] = 0
for tag in DUMTAGS:
    TAGS[tag] = j
    j += 1
    TAGFREQ[tag] = 0

TAGS['altern'] = TAGS['subst']
TAGS['argstr'] = TAGS['prep']
TAGS['gender'] = TAGS['agrgender']
TAGS['orpho'] = TAGS['ortho']
TAGS['reflex'] = TAGS['refl']
TAGS['miss'] = TAGS['del']

print('len of tags ', len(TAGS))

def clear_tags(tags):
    nt = []
    tags = tags.replace('+', ', ').replace('\\', ', ').replace(',,', ',').replace('/', ', ')
    tags = tags.split(', ')
    for tag in tags:
        tag = tag.replace('?', '').replace(',', '').replace(' ', '').replace('!', '')
        tag = tag.lower()
        nt.append(tag)
    tags = set(nt)
    nt = []
    for tag in tags:
        if tag in GOODTAGS or tag in DUMTAGS:
            nt.append(tag)
        else:
            if tag in BTAGS:
                BTAGS[tag] += 1
            else:
                BTAGS[tag] = 1
    if len(nt) == 0:
        #print(tags, 'are strange out there')
        # for tag in tags:
        #     if tag in BTAGS:
        #         BTAGS[tag] += 1
        #     else:
        #         BTAGS[tag] = 1
        return 'badtag'
    return ' '.join(nt)

def tagarray(tags):
    tags = tags.split(' ')
    arr = ['0' for j in range(len(TAGS) - 6)]
    for tag in tags:
        if tag in TAGS:
            arr[TAGS[tag]] = '1'
            TAGFREQ[tag] += 1
        else:
            print(tag, 'is unexpected')
    return arr

First = True
for line in f:
    line = line.rstrip()
    if First:
        for tag in GOODTAGS + DUMTAGS:
            if tag == 'orpho':
                break
            line += '\t' + tag
        line += '\r\n'
        w.write(line)
        First = False
        continue
    data = line.split('\t')
    data[6] = clear_tags(data[6][1:-1])
    if data[6] == 'badtag':
        continue
    tarr = tagarray(data[6])
    data += tarr
    w.write('\t'.join(data) + '\r\n')

for tag in sorted(TAGFREQ):
    print(tag, ': ', TAGFREQ[tag])
print('_______________________________________________')
for tag in sorted(BTAGS):
    print(tag, ': ', BTAGS[tag])