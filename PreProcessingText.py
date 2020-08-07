import pandas as pd
import numpy as np
import spacy
from fuzzywuzzy import fuzz

def clean_up_spacyLoose(doc):
    removal= ['PRON','SPACE','DET','NUM','SCONJ']
    text_out = []
    for token in doc:
            if (token.is_stop == False and not token.is_digit and token.pos_ not in removal and not token.is_punct and not token.is_bracket):
        #if token.pos_ not in removal and not token.is_digit:
                ttext = token.text
                print(ttext)
                text_out.append(ttext)

    return " ".join(text_out)

def clean_up_spacyDOCPIPE(doc):
    #nlpClean = spacy.load('en')
    removal= ['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE','SYM']
    text_out = []
    #doc= nlp(text)
    for token in doc:
        #if (token.is_stop == False and not token.is_digit and not token.is_punct and not token.is_bracket):
        if (token.is_stop == False and not token.is_digit and token.pos_ not in removal and not token.is_punct and not token.is_bracket):
            ttext = token.text
            text_out.append(ttext)

    return " ".join(text_out)



def clean_up_spacy(text,nlp):
    #nlpClean = spacy.load('en')
    removal= ['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE','SYM']
    text_out = []
    doc= nlp(text)
    for token in doc:
        if (token.is_stop == False and not token.is_digit and token.pos_ not in removal and not token.is_punct and not token.is_bracket):
            ttext = token.text
            text_out.append(ttext)

    #print(text,text_out)

    return " ".join(text_out)

def CleanNgrams(dictClean,sparsematrix,features):
    for key in dictClean.keys():
        columnindexKey=features.index(key)
        columnindexValue=features.index(dictClean[key])
        sparsematrix[:,columnindexValue]=sparsematrix[:,columnindexValue]+sparsematrix[:,columnindexKey]
        sparsematrix[:,columnindexKey]=1*10e-10#### Set to epsilon to downweight
    return sparsematrix

def CreateNgramsDict(sparsematrix,features,no_most_frequent):
    d = pd.Series(sparsematrix.toarray().sum(axis=0),index = features).sort_values(ascending=False)
    terms=d.nlargest(no_most_frequent).keys()
    defineNgrams={}
    for w1 in terms:
        values=[]
        for w2 in terms:
            if(w1==w2):continue
            lev=fuzz.ratio(w1,w2);
            if(lev>=66 and lev<100):
                ### Choose the longest n-gram: prioritize trigrams
                if(len(w1.split(" "))==len(w2.split(" "))):continue
                if(len(w1)>len(w2)):
                    defineNgrams[w2]=w1
                else:
                    defineNgrams[w1]=w2
    return defineNgrams
