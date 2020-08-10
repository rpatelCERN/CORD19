import pandas as pd
from CreateTopics import TopicKeywordAbstractSearch
from InitNLP import *
from PreProcessingText import *

from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib
import sys

def AbstractRankedPhrases(KeywordsinTopic,nlp,minRank,maxcount,highrank,highcount,SelectedRows):####Use pyTextRank
    SelectedRows.loc[SelectedRows['abstract'].notnull(),'FilledAbs']=True
    SelectedRows.loc[SelectedRows['abstract'].isnull(),'FilledAbs']=False
    SelectedRows.loc[SelectedRows['abstract']=='abstract','FilledAbs']=False
    TopicAbstracts=SelectedRows[SelectedRows['FilledAbs']==True]
    TopicAbstracts['abstract']=TopicAbstracts['abstract'].str.lower()
    TopicAbstracts['FilledTopic']=False;

    for kw in KeywordsinTopic:TopicAbstracts.loc[TopicAbstracts['abstract'].str.contains(kw.strip()),'FilledTopic']=True
    Abstracts=TopicAbstracts[TopicAbstracts['FilledTopic']==True]['abstract'].tolist()
    print(len(Abstracts))
    del TopicAbstracts;

    PassingMatches=[]
    Matches=[]
    rank=[]
    frequency=[]
    phrase=[]

    rankkw=[]
    frequencykw=[]
    phrasekw=[]

    AllRankedPhrases=[]
    CombinedAbstract=", ".join(Abstracts)
    print(len(Abstracts))
    if(len(CombinedAbstract)>1000000):#### Length in characters takes up a lot of memory run into spacy error
            Chunks=int(len(CombinedAbstract)/100000)+1
            print(Chunks)
            interval=int(len(Abstracts)/Chunks)
            for c in range(Chunks):
                start=c*interval
                stop=int((c+1)*interval)
                print(start,stop)
                if(stop>len(Abstracts)):stop=len(Abstracts)
                Ranked=TextRank(", ".join(Abstracts[start:stop]),nlp)
                AllRankedPhrases.extend(Ranked)
    else:AllRankedPhrases=TextRank(", ".join(Abstracts),nlp)

    for p in AllRankedPhrases:
        if(p.text=="abstract"):continue
        rank.append(p.rank)#### The rank in the abstract
        frequency.append(p.count)#### the frequency
        phrase.append(p.text)
        if p.count>=maxcount:continue
        if p.rank>highrank and p.count<=highcount:PassingMatches.append(p.text)# and p.count>=6):print(p.text,p.rank,p.count)
        for kw in KeywordsinTopic:
                #if kw in p.text and p.rank<0.02:print(p.text,p.rank)
                if kw in p.text and p.rank>minRank:
                    #(p.text)
                    #if p.rank>0.02 and p.rank<=0.03:print(p.text,p.rank)
                    PassingMatches.append(p.text)
                    break;
        #if(p.count>=10):print(p.text,p.count)
        for kw in KeywordsinTopic:
            #if kw in p.text:
            if kw in p.text :
                #cleantext=clean_up_spacy(p.text,nlp)
                rankkw.append(p.rank)#### The rank in the abstract
                frequencykw.append(p.count)#### the frequency
                phrasekw.append(p.text)
                break;
    ####
    mapofWords={'textrank':rank,'frequency':frequency,'phrase':phrase}
    outputDF=pd.DataFrame(mapofWords)
    ax=sns.scatterplot(x="textrank", y="frequency", data=outputDF,label='All ranked phrases')
    print(outputDF.head())
    print(type(outputDF.frequency))
    ax2=sns.kdeplot(outputDF.textrank,label='KDE all phrases')#,cmap="Reds", shade=True, shade_lowest=False)
    del outputDF
    mapofWords={'kwtextrank':rankkw,'frequencykw':frequencykw,'phrasekw':phrasekw}
    outputDF=pd.DataFrame(mapofWords)
    ax=sns.scatterplot(x="kwtextrank", y="frequencykw", data=outputDF,label="Matched phrases to topic words")
    ax2=sns.kdeplot(outputDF.kwtextrank,label='KDE matched phrases')#, y="frequencykw", data=outputDF,cmap="Reds", shade=True, shade_lowest=False)
    plt.xlabel("PyText Rank Score")
    plt.ylabel("Count Freq.")
    plt.show()
    return list(set(Matches)),list(set(PassingMatches));


def AbstractRankOptimization(stop_words,SelectedRows,AllTopicKeyWords,minRank):
    nlp = InitNLPPyTextRank();
    nlp.disable_pipes("ner")
    for w in stop_words:nlp.vocab[w].is_stop = True;
    stop_words.extend('coronavirus')
    KeyPhrases,PassPhrases=AbstractRankedPhrases(AllTopicKeyWords,nlp,minRank,40,0.06,5,SelectedRows)
    #print(KeyPhrases)
    print(PassPhrases)
    print(len(PassPhrases))
    return KeyPhrases,PassPhrases
