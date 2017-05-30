import codecs
from transliterate import translit

def get_list(filename):
    k_f = codecs.open(filename, 'r', 'utf-8')

    words = []
    for line in k_f:
        line = line.rstrip()
        if line != '' and '_' not in line:
            word = line.split(' ')[0].lower()
            words.append(word)
    k_f.close()
    words = set(words)
    words = list(words)
    return words

words = get_list('tf-idr-error.txt')
words_c = get_list('tf-idr-correction.txt')
print(len(words), len(words_c))

f = codecs.open('rlc_featured_mod8.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod9.csv', 'w', 'utf-8')

f_lines = f.readlines()

newfeatures = [translit(i, 'ru', reversed=True) + '_e' for i in words]

newfeatures_c = [translit(i, 'ru', reversed=True) + '_c' for i in words_c]

w.write(f_lines[0].rstrip() + '\t' + '\t'.join(newfeatures + newfeatures_c) + '\r\n')


for line in f_lines[1:]:
    line = line.rstrip()
    data = line.split('\t')
    words1 = data[4]
    words2 = data[5]
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
    w.write('\t'.join(data) + '\t' +
            '\t'.join(n_f + n_f_c) + '\r\n')

w.close()