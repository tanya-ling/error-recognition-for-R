import os
import codecs
import nltk

print('\u043d\u0430\u0448\u0435\u043c \u043f\u0435\u0440\u0432\u043e\u043c \u0432\u044b\u0432\u043e\u0434\u0435')
print('"7538";"5";"517";"12d029b9-602b-4e46-95ed-1dc72be2ffb3";"2016-01-13 22:21:37";"2016-03-25 20:51:06";"{""corrs"": ""\u0447\u0442\u043e"", ""quote"": ""\u043a\u0430\u043a"", ""text"": ""\u043e\u0448\u0438\u0431\u043a\u0430 \u0432 \u0441\u043e\u044e\u0437\u0435"", ""ranges"": [{""start"": ""/span[2]"", ""end"": ""/span[2]"", ""startOffset"": 0, ""endOffset"": 3}], ""tags"": [""Lex""]}";"Lex";"2";"2";"0";"3";"как";"что"')
print('"7505";"5";"258";"20632fcd-37e9-4e1b-b51e-9fd00f2d0a82";"2016-01-09 20:17:08";"2016-04-12 13:41:36";"{""corrs"": ""\u044d\u043a\u0441\u043a\u0443\u0440\u0441\u0438\u044f"", ""quote"": ""\u044d\u0441\u043a\u0443\u0440\u0441\u0438\u044f"", ""text"": """", ""ranges"": [{""start"": ""/span[2]"", ""end"": ""/span[2]"", ""startOffset"": 0, ""endOffset"": 8}], ""tags"": [""Ortho"", ""Del""]}";"Ortho, Del";"2";"2";"0";"8";"эскурсия";"экскурсия"')
def look_for_word(sentences, prev_sentid, start, finish, error, word_ind, direct='down'):
    i = 0
    sent = ''
    pi = prev_sentid
    i = 0
    for sentence in sentences:
        i += 1
        tokens = nltk.word_tokenize(sentence)
        if word_ind >= len(tokens):
            continue
        if tokens[word_ind] == error:
            sentid = i
            sent = sentence
            if sentid >= prev_sentid:
                w.write('\t'.join([index, str(sentid), sent, start, finish, error, data[2], data[3], data[0]]) + '\r\n')
                prev_sentid = sentid
                return prev_sentid
            else:
                sent = ''
    if sent == '':
        i = 0
        for sentence in sentences:
            i += 1
            # if i < prev_sentid:
            #     continue
            tokens = nltk.word_tokenize(sentence)
            for word in tokens:
                if error == word:
                    sentid = i
                    sent = sentence
                    w.write('\t'.join([index, str(sentid), sent, start, finish, error, data[2], data[3], data[0]]) + '\r\n')
                    prev_sentid = sentid
                    return prev_sentid
        w2.write('\t'.join([index, '?', '?', start, finish, error, data[2], data[3], data[0]]) + '\r\n')
        # if word_ind > 1 and direct == 'down':
        #     prev_sentid = look_for_word(sentences, pi, start, finish, error, word_ind - 1)
        # elif direct == 'down':
        #     word_ind = int(start) - 1
        #     prev_sentid = look_for_word(sentences, pi, start, finish, error, word_ind + 1, direct='up')
        # else:
        #     prev_sentid = look_for_word(sentences, pi, start, finish, error, word_ind + 1, direct='up')
    return prev_sentid



path = 'C:\\Tanya\\НИУ ВШЭ\\диплом\\rlc\\texts'
w = codecs.open('rlc.csv', 'w', 'utf-8')
w2 = codecs.open('rlc_failed.csv', 'w', 'utf-8')
w.write('docid\tsentid\tsent\tstart\tfinish\terror\tcorrection\ttag\tannotator')
for filename in os.listdir(path):
    f = codecs.open(path + '\\' + filename, 'r', 'utf-8')
    text = f.read()
    f.close()
    index = filename[:-4]
    f = codecs.open('C:\\Tanya\\НИУ ВШЭ\\диплом\\rlc\\annot\\' + index + '.csv', 'r', 'utf-8')
    ann = f.read().replace('u', '\\u').rstrip().split('\r\n')[1:]
    f.close()
    sentences = nltk.sent_tokenize(text)
    prev_sentid = 0
    for annot in ann:
        sent = ''
        data = annot.split('\t')
        start = data[4]
        finish = data[5]
        error = data[1]
        words = nltk.word_tokenize(error)
        word_ind = int(start) - 1
        try:
            prev_sentid = look_for_word(sentences, prev_sentid, start, finish, words[0], word_ind)
        except IndexError: # DEL!!!
            print(error, index, start, finish)
        # try:
        #     start = data[4]
        #     finish = data[5]
        #     error = data[1]
        # except IndexError:
        #     print('indexerror', index, data)
        # words = nltk.word_tokenize(error)
        # i = 0
        # for sentence in sentences:
        #     i += 1
        #     tokens = nltk.word_tokenize(sentence)
        #     if int(start) > len(tokens):
        #         continue
        #     if tokens[int(start) - 1] == words[0] and int(finish)-int(start)+1 == len(words):
        #         sentid = i
        #         sent = sentence
        #         if sentid >= prev_sentid:
        #             w.write('\t'.join([index, str(sentid), sent, start, finish, error, data[2], data[3], data[0]]) + '\r\n')
        #             prev_sentid = sentid
        #             break
        #         else:
        #             sent = ''
        # if sent == '':
        #     w2.write('\t'.join([index, '?', '?', start, finish, error, data[2], data[3], data[0]]) + '\r\n')
    #break
