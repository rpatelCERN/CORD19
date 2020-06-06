import json
from pprint import pprint
from rank_bm25 import BM25Okapi


def Nlines_in_paper(JSON_FILE):
    data = json.load(open(JSON_FILE))
    bodytext = data['body_text']
    return len(bodytext)
def line_in_paper(JSON_FILE,linenumber):
    data = json.load(open(JSON_FILE))
    bodytext = data['body_text']#### This is a list
    tempdict=dict(bodytext[linenumber])
    return tempdict['text']

def SearchKeyWord(word, FNAME):
    matchedline=""
    for i in range(0,Nlines_in_paper(FNAME)):
        if word in line_in_paper(FNAME,i):
            matchedline=line_in_paper;
            break;
    return matchedline;

def SearchKeyWordList(wordlist, FNAME):
    MatchInfo=[]
    for i in range(0,Nlines_in_paper(FNAME)):
        line=line_in_paper(FNAME,i)
        LineSentence=line.split('.')
        Matches=[]
        for keyword in wordlist:
            for l in LineSentence:
                linewords=l.split(" ")
                if keyword in l and keyword in linewords :
                    Matches.append(keyword)
                    Matches.append(l)
        if len(Matches)>0:MatchInfo.append(Matches)
    return MatchInfo;

def BM25Search(corpus,searchquery,ntopsentences):

    #corpus=f.readlines();
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = searchquery.split(" ")
    doc_scores = bm25.get_scores(tokenized_query)
    return (doc_scores,bm25.get_top_n(tokenized_query, corpus, n=ntopsentences))
