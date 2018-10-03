from hmmtagger import MainTagger
from tokenization import *
import requests
import string
import re

def do_tokencheck(str):
    # cek token ke db kateglo
    api = "http://kateglo.com/api.php?format=json&phrase="
    if requests.get(api+str).headers['Content-Type'][0] == "a":
        return True
    else: return False

mt = None
def init_tag():
    global mt
    if mt is None:
        mt = MainTagger("resource/Lexicon.trn", "resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)

def do_tag(teks):
    lines = teks.strip().split("\n")
    result = []
    try:
        init_tag()
        for l in lines:
            if len(l) == 0: continue
            out = sentence_extraction(cleaning(l))
            for o in out:
                strtag = " ".join(tokenisasi_kalimat(o)).strip()
                result += [" ".join(mt.taggingStr(strtag))]
    except:
        return "Error Exception"
    return "\n".join(result)

def main():
    table = string.maketrans("", "")
    teks = raw_input("inputkan teks: ")
    # cek token
    sentences = re.split("[^a-z] ", teks)
    for sent in sentences:
        token = {}
        for item in tokenisasi_kalimat(sent.translate(table, string.punctuation)):
            token[item] = do_tokencheck(item)
        if False in token.values():
            notvalid = [i for i, x in enumerate(token.values()) if x == False]
            for j in notvalid:
                print token.keys()[j], " token tidak valid"
        else:
            print "semua token, '%s' , valid" % sent

            # cek pos-tag
            tagseq = re.findall("[A-Z]{1,3}", do_tag(sent))
            print tagseq
            rule = {'tanya1':'WP-PRP-VBI',
                    'tanya2':'PRP-VBI-WP',
                    'tanya4':'PRP-IN-NN-WP',
                    'tanya5': 'WP-NN-VBT-PRP',
                    'tanya6': 'WP-NN-VBT-PRP-DT',
                    'tanya7': 'WP-NN-IN-NN-DT',
                    'preposisi1': 'PRP-VBT-NN-IN-NN',
                    'preposisi2': 'PRP-VBI-VBT-NN-IN-NN',
                    'preposisi3': 'PRP-VBI-IN-NN',
                    'preposisi4': 'NNG-VBI-IN-NN',
                    'general1': 'PRP-VBT-NN',
                    'general2': 'NN-DT-JJ',
                    'frase1': 'NN-JJ'}
            w=False
            for k in rule.values():
                if "-".join(tagseq) in k:
                    print "struktur kalimat, %s ,valid" %k
                    w=True
                    break
            if not w:
                print "struktur kalimat, %s ,tidak valid" %"-".join(tagseq)

main()
