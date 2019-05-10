from django.shortcuts import render
from django.http import HttpResponse
from apps.inverted import main

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request, 'apps/home.html')

def index(request):
    return render(request, 'apps/index.html')

def search():
    import xml.dom.minidom as minidom
    doc_xml = minidom.parse("apps/data/KP.xml")

    all_doc_no = doc_xml.getElementsByTagName('DOCNO')
    all_headline = doc_xml.getElementsByTagName('HEADLINE')
    all_text = doc_xml.getElementsByTagName('TEXT')

    all_sentence_doc = []
    for i in range(N_DOC):
        sentence_doc = all_headline[i].firstChild.data +' '+ all_text[i].firstChild.data
        all_sentence_doc.append(sentence_doc)

    for i in range(N_DOC):
        tokens_doc.append(main.remove_punc_tokenize(all_sentence_doc[i]))

    for i in range(N_DOC):
        tokens_doc[i] = main.to_lower(tokens_doc[i])

    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    import string

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


    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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



    #################Remove Duplicate####################
    all_tokens = set(all_tokens)

    ###########################Proximity Index######################
    from itertools import count
    proximity_index = {}
    for token in all_tokens:
        dict_doc_position = {}
        for n in range(N_DOC):
            if(token in tokens_doc[n]):
                dict_doc_position[all_doc_no[n].firstChild.data] = [i+1 for i, j in zip(count(), tokens_doc[n]) if j == token]
        proximity_index[token] = dict_doc_position


    import collections
    proximity_index = collections.OrderedDict(sorted(proximity_index.items()))
    for key, value in proximity_index.items():
        print (key, value)


    file = open('proximity index after remove number, stopping and stemming.txt','w')
    for key, value in proximity_index.items():
        file.write(key+'\n')
        for key, value in value.items():
            file.write('\t'+str(key)+': ')
            for i in range (len(value)):
                file.write(str(value[i]))
                if not(i == len(value)-1): 
                    file.write(',')
            file.write('\n')
        file.write('\n')
    file.close()  

    # proximity_index['ada'].items()
    for value in proximity_index['adil'].items():
        print(value)


    ##############Query################
    query = request.form['querysearch']

    #############Preprocessing Query##################
    #query = "Sungguh Hatiku"

    queri=[]
    spl = query.split()
    for i in range(len(spl)):
        if not spl[i].isdigit():
            queri.append(spl[i])

    # define punctuation  
    punctuation = '''''!()-[]{};:'"\,<>./?@#$%^&*_~'''  
    # take input from the user  
    my_str = input("Enter a string: ")  
    # remove punctuation from the string  
    no_punct = ""  
    for char in my_str:  
        if char not in punctuation:  
            no_punct = no_punct + char
    # display the unpunctuated string  
    print(no_punct)  

    punc = []
    for i in range(len(queri)):
        no_punc = ""
        for j in range(len(queri[i])):
            if queri[i][j] not in string.punctuation:            
                no_punc = no_punc + queri[i][j]        
        punc.append(no_punc)
                
    url = []
    urlDict = "^https?:\/\/.*[\r\n]*"
    for i in range(len(punc)):
        no_url=""
        for j in range(len(punc[i])):
            if punc[i][j] not in urlDict:
                no_url = no_url + punc[i][j]
        url.append(no_url)
        

    lower=[]
    for i in range(len(url)):
        lower.append(url[i].lower())


    stop = []
    for i in range(len(lower)):
        if lower[i] not in stop_words:
                stop.append(lower[i])


    stem = []
    for i in range(len(stop)):
        stem.append(stemmer.stem(stop[i]))
        

    join_word = ' '.join([w for w in stem])

    ngram, ngram_doc = main.generate_ngrams(stemming, len(stem))

    # join all ngram dalam bentuk kalimat
    ngram_sentence=[]
    for i in range(len(ngram)):
        ngram_sentence.append(' '.join(ngram[i]))
        
    ngram_sentence


    # indexing ngram

    n_gram_index = {}
    for ngram_token in ngram:
        doc_no = []
        for i in range(N_DOC):
            if(ngram_token in ngram_doc[i]):
                doc_no.append(all_doc_no[i].firstChild.data)
        n_gram_index[ngram_token] = doc_no

    hasil = (u', '.join(n_gram_index[join_word]))

    # content= {
    #     'hasil' : hasil
    # }

    return render(request, 'apps/index.html', content= {'hasil' : hasil})


