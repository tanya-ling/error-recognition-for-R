import codecs

f = codecs.open('rlc_featured_mod.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod2.csv', 'w', 'utf-8')

DUMTAGS = ['not-clear', 'add', 'less', 'extra', 'more', 'transp', 'subst']
GOODTAGS = ['prep', 'graph', 'hyphen', 'space', 'ortho', 'translit', 'misspell', 'deriv', 'infl', 'num', 'gender',
            'morph', 'asp', 'passive', 'reflex', 'agrnum', 'agrcase', 'agrgender', 'agrpers', 'agrgerund', 'transfer',
            'gov', 'ref', 'conj', 'wo', 'neg', 'aux', 'brev', 'syntax', 'constr', 'lex', 'cs', 'par', 'idiom']


def clear_tags(tags):
    nt = []
    tags = tags.replace('+', ', ').replace('\\', ', ').replace(',,', ',').replace('/', ', ')
    tags = tags.split(', ')
    for tag in tags:
        tag = tag.replace('?', '').replace(',', '').replace(' ', '')
        tag = tag.lower()
        nt.append(tag)
    tags = set(nt)
    nt = []
    for tag in tags:
        if tag in GOODTAGS or tag in DUMTAGS:
            nt.append(tag)
    if len(nt) == 0:
        print(tags)
        return 'badtag'
    return ' '.join(nt)

First = True
for line in f:
    if First:
        w.write(line)
        First = False
        continue
    data = line.split('\t')
    data[6] = clear_tags(data[6][1:-1])
    if data[6] == 'badtag':
        continue
    w.write('\t'.join(data))