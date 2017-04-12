import urllib.request
import codecs


f = codecs.open('C:/Tanya/НИУ ВШЭ/диплом/rlc/annotator_sentence.csv', 'r', 'utf-8')
prev_id = 0
for line in f:
    try:
        data = line.rstrip().split('";"')
        text_id = data[2][:-1]
        if text_id == prev_id:
            continue
        # print(data[0], text_id)
        urllib.request.urlretrieve("http://www.web-corpora.net/RLC/download_file/" + text_id + "/text",
                                   "C:/Tanya/НИУ ВШЭ/диплом/rlc/texts/" + text_id + ".txt")

        urllib.request.urlretrieve("http://www.web-corpora.net/RLC/download_file/" + text_id + "/ann",
                                   "C:/Tanya/НИУ ВШЭ/диплом/rlc/annot/" + text_id + ".csv")
        prev_id = text_id
    except urllib.error.HTTPError:
        print(line, text_id)