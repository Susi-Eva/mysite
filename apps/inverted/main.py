resource_package = __name__

import string
import re
from sklearn.feature_extraction.text import CountVectorizer


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