resource_package = __name__

import string
import re
from sklearn.feature_extraction.text import CountVectorizer
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from itertools import count
import collections
import math
from xml.etree.ElementTree import ElementTree


##############Remove Punctuation, URL and Tokenize###################
def remove_punc_tokenize(sentence):
    tokens = []
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation," ")
    
    sentence = re.sub(r'^https?:\/\/.*[\r\n]*', '', sentence, flags=re.MULTILINE)
    for w in CountVectorizer().build_tokenizer()(sentence):
        tokens.append(w)
    return tokens


##############Case Folding########################
def to_lower(tokens):
    tokens = [x.lower() for x in tokens]
    return tokens

def generate_ngrams(data, n):
    ngram=[]
    result = []
    
    #menampilkan hasil n-gram per dokumen
    for i in range(len(data)):
        sequences = [data[i][j:] for j in range(n)]
        temp = zip(*sequences)
        lst = list(temp)
        result.append([" ".join(lst) for lst in lst])
    
    #menggabungkan n-gram semua dokumen dalam bentuk array
    for i in range(len(result)):
        for j in range(len(result[i])):
            ngram.append(result[i][j])
            
    return ngram, result

def main(query):

    tree = ElementTree()
    tree.parse("apps/data/BukuNyanyianHKBP.xml")

    all_doc_no = []
    all_headline = []
    all_text = []

    for node in tree.iter("DOCNO"):
        all_doc_no.append(node.text)
        
    for node in tree.iter("HEADLINE"):
        all_headline.append(node.text)
        
    for node in tree.iter("TEXT"):
        all_text.append(node.text)

    N_DOC = len(all_text)

    all_sentence_doc = []
    for i in range(N_DOC):
        all_sentence_doc.append(all_headline[i] + all_text[i])
    tokens_doc = []
    for i in range(N_DOC):
        tokens_doc.append(remove_punc_tokenize(all_sentence_doc[i]))

    for i in range(N_DOC):
        tokens_doc[i] = to_lower(tokens_doc[i])

    stop_words = set(stopwords.words('indonesian'))

    stopping = []
    for i in range(N_DOC):
        temp = []
        for j in tokens_doc[i]:
            if j not in stop_words:
                temp.append(j)
        stopping.append(temp)

    for i in range(N_DOC):
        tokens_doc[i] = ([w for w in stopping[i] if not any(j.isdigit() for j in w)])

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    stemming = []
    for i in range(N_DOC):
        temp=[]
        for j in tokens_doc[i]:
    #         print(j)
            temp.append(stemmer.stem(j))
        stemming.append(temp)

    all_tokens = []
    for i in range(N_DOC):
        for w in stemming[i]:
            all_tokens.append(w)

    new_sentence = ' '.join([w for w in all_tokens])

    for w in CountVectorizer().build_tokenizer()(new_sentence):
        all_tokens.append(w)

    all_tokens = set(all_tokens)
    alls = []
    for i in all_tokens:
        alls.append(i)


    queri=[]
    spl = query.split()
    for i in range(len(spl)):
        if not spl[i].isdigit():
            queri.append(spl[i])

    punc = []
    for i in range(len(queri)):
        no_punc = ""
        for j in range(len(queri[i])):
            if queri[i][j] not in string.punctuation:            
                no_punc = no_punc + queri[i][j]        
        punc.append(no_punc)
    
    lower=[]
    for i in range(len(punc)):
        lower.append(punc[i].lower())

    stop = []
    for i in range(len(lower)):
        if lower[i] not in stop_words:
            stop.append(lower[i])

    stem = []
    for i in range(len(stop)):
        stem.append(stemmer.stem(stop[i]))
        
    join_word = ' '.join([w for w in stem])

    ngram, ngram_doc = generate_ngrams(stemming, len(stem))

    n_gram_index = {}
    for ngram_token in ngram:
        doc_no = []
        for i in range(N_DOC):
            if(ngram_token in ngram_doc[i]):
                doc_no.append(all_doc_no[i])
        n_gram_index[ngram_token] = doc_no

    df = []

    for i in range(N_DOC):
        count = 0
        for j in range(len(ngram_doc[i])):
            if join_word == ngram_doc[i][j]:
                count+=1
        df.append(count)

    idf = []
    for i in range(len(df)):
        try:
            idf.append(math.log10(N_DOC/df[i]))
        except ZeroDivisionError:
            idf.append(str(0))

    #w(t, d)
    #t = term
    #d = document
    wtd = []
    l = []
    for i in range(N_DOC):
        dic = {}
        tf = ngram_doc[i].count(join_word) # menghitung nilai tf
        if tf != 0:
            score = math.log10(tf) #log10(tf(t,d))
            score+=1 # 1 + log(tf(t,d))
            score*=idf[i] #tf * idf
            
            idx = all_doc_no[i]
            judul = all_headline[i]
            
            dic['docno'] = idx
            dic['judul'] = judul
            dic['score'] = score
            
            l.append(dic)
    wtd.append(l) # [i+1] = defenisi nomor dokumen; score = wtd
    #         print(score)


    hasil = []
    hasil.append(sorted(wtd[0], key = lambda x : x['score'], reverse = True))

    top_result = hasil[0][:9]
    N = len(top_result)
    return top_result, N

def detail(nomor):
    tree = ElementTree()
    tree.parse("apps/data/BukuNyanyianHKBP.xml")

    all_doc_no = []
    all_headline = []
    all_text = []

    for node in tree.iter("DOCNO"):
        all_doc_no.append(node.text)
        
    for node in tree.iter("HEADLINE"):
        # all_headline.append(node.text.replace("\n"," "))
        all_headline.append(node.text)
        head = all_headline
        
    for node in tree.iter("TEXT"):
        # all_text.append(node.text.replace("\n"," "))
        all_text.append(node.text)

    N_DOC = len(all_text)
    text = []
    judul=[]
    hasil = []
    id = str(nomor)
    for i in range(N_DOC):
        check = all_doc_no[i]
        if check == id:
            text = all_text[i]
            judul = all_headline[i]
            return text,judul