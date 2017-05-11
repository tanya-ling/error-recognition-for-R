import codecs

f = codecs.open('rlc_featured_mod2.csv', 'r', 'utf-8')
w = codecs.open('rlc_featured_mod3.csv', 'w', 'utf-8')

f_lines = f.readlines()

w.write(f_lines[0])

f_set = set(f_lines[1:])

for line in f_set:
    w.write(line)

w.close()
