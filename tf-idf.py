from sklearn.feature_extraction.text import TfidfVectorizer

import math
from textblob import TextBlob as tb
import nltk
import pandas
tf = TfidfVectorizer(analyzer='word', min_df=0)





def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)



df = pandas.read_csv('.\\rlc_featured_mod8.csv', sep='\t')
tagslist = 'prep	phon	graph	hyphen	space	ortho	translit	misspell	deriv	infl	num	morph	' \
           'asp	passive	agrnum	agrcase	agrgender	agrpers	agrgerund	transfer	gov	ref	conj	wo	neg	aux	brev' \
           '	syntax	constr	lex	cs	par	idiom	coord	refl	insert	tense	not-clear	transp	subst	del' \
           '	punc	typo'.split('\t')
new_tags = 'gov_w_prep\tlex_wo_conj\tortho_wo_others\tsyntax_wo_others'.split('\t')

tagslist += new_tags

d = {}

for tag in tagslist:
    d[tag] = [i['correction'] for index, i in df.iterrows() if i[tag] == 1]

d2 = {}
for tag in d:
    d2[tag] = ''
    for word in d[tag]:
        d2[tag] += str(word) + ' '


words = {}
bloblist = []
for tag in d2:
    words[tag] = set(d2[tag].split(' '))
    d2[tag] = tb(d2[tag])
    bloblist.append(d2[tag])


tf_idf_w = {}
for tag in d2:
    tf_idf_w[tag] = {}
    for word in words[tag]:
        tf_idf_w[tag][word] = tfidf(word, d2[tag], bloblist)
        if tfidf(word, d2[tag], bloblist) == None:
            print(word, tag, 'None')
    i = 0
    print()
    print(tag.upper() + '_________________________________________')
    for word in sorted(tf_idf_w[tag], key=tf_idf_w[tag].get, reverse=True):
        print(word, tf_idf_w[tag][word])
        i += 1
        if i == 20:
            break
