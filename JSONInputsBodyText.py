import json
from pprint import pprint


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
                if keyword in l:
                    Matches.append(keyword)
                    Matches.append(l)
        if len(Matches)>0:MatchInfo.append(Matches)
    return MatchInfo;


