from JSONInputsBodyText import *
import pandas as pd
import csv
import matplotlib.pyplot as plt
import string
import sys
from rank_bm25 import BM25Okapi

def CleanupKeyword(word):
        word=word.replace("[","");
        word=word.replace("]","");
        word=word.replace("'", "");
        word=word.replace(")","")
        word=word.replace("(","")
        if a=='2019' or a=="''" or a=="'":word=""
        return word
df=pd.read_csv('ProcessedCSV/AnalyzedTitlesAbstract.csv', low_memory=False)
dfRank=pd.read_csv('ProcessedCSV/AbstractWordRanking.csv', low_memory=False)
PATH="%s" %sys.argv[1]
PublicationsMined=[]
KeyWordsUsed=[]
KeyWordsFound=[]
LinesFound=[]
Allines=""
FullAbstractKeys=[]
CandidateCategories=[]
f=open('wordbagTotal.txt','w');

for i in range(len(dfRank  )):
    AbstractOnlyKeywords=dfRank ['text']
    TextRank=dfRank .loc[i,'rank']
    Freq=dfRank .loc[i,'frequency']
    for a in AbstractOnlyKeywords:
        a=CleanupKeyword(a)
        FullAbstractKeys.append(a)
for i in range(len(df)):
    TitleKeyWords=df.loc[i,'Title Qualifier Words']
    if isinstance(TitleKeyWords,float):continue
    if "covid19" not in TitleKeyWords:continue
    TitleKeyWords=TitleKeyWords.replace("covid19,","")
    Categories=TitleKeyWords.split(",");
    #print(TitleKeyWord)
    #print(Categories)
    #for c in Categories:
        #if c=="covid19":continue
    #print(c)
    AbstractKeyWords=df.loc[i,'Matched Abstract Qualifier Words']
    if isinstance(AbstractKeyWords,float):continue
    AbstractKeyWords=AbstractKeyWords.split(",");
    if len(AbstractKeyWords)<1:continue
    Cleanup=[]
    for a in AbstractKeyWords:
        a=CleanupKeyword(a)
        Cleanup.append(a)
    AbstractKeyWords=list(set(Cleanup));#unique instances
    if AbstractKeyWords==[''] or len(AbstractKeyWords)<1:continue
    #AbstractKeyWords=['wet market']
    sha=df.loc[i,'sha']
    sha=sha.split("; ")
    location=df.loc[i,'full_text_file^M']

    for s in sha:
        filename=PATH+location+"/"+location+"/"+s+".json"
        #print(AbstractKeyWords)
        MatchInfo=SearchKeyWordList(AbstractKeyWords,filename)
        PublicationsMined.append(filename)
        KeyWordsUsed.append(AbstractKeyWords)
        #
        #if(len(MatchInfo)>0):
        MatchedKeys=[]
        MatchedLineToKey=[]
        for m in MatchInfo:
             #print(m[1]+".")#Matched line
             MatchedKeys.append(m[0]);
             MatchedLineToKey.append(m[1]+".")
             f.write(m[1]);
        f.write("\n");
        MatchedKeys=list(set(MatchedKeys))#unique list
        KeyWordsFound.append(MatchedKeys);
        LinesFound.append(MatchedLineToKey);
        CandidateCategories.append(Categories);
f.close();
mapofWords={'sha':PublicationsMined,'Candidate Category':CandidateCategories,'Initial Keywords':KeyWordsUsed, 'Matched Keywords':KeyWordsFound, 'Text Matches':LinesFound}
PlotDF=pd.DataFrame(mapofWords)
PlotDF.to_csv(r'ProcessedCSV/SearchWithKeyWords.csv', index = True)

f=open('wordbag.txt','w');
for list in LinesFound:
    if len(list)<1:continue;
    text=""
    text="\n"+text.join(list)
    f.write(text)
f.close()


    #if(i>10):break;
        #for list in Matchedline:

        #print(filename)
        #print(Nlines_in_paper(filename));
