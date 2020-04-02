import pandas as pd
from InitNLP import *
import re
import matplotlib.pyplot as plt

#def FillWordBag(f,text):
    #print(text)
def RankWordsBag(f,nlp):
    Alltext=f.readline()
    phrases=TextRank(Alltext,nlp)
    return phrases
    
def FillCSV(phrases,minrank,minfreq):
    rank=[]
    frequency=[]
    phrase=[]
    for p in phrases:
            if(p.count>=minfreq and p.rank>=minrank):###Require minimum frequncy
                print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
                phrase.append(p.text)
                rank.append(p.rank)
                frequency.append(p.count)
    mapofWords={'rank':rank,'frequency':frequency, 'text':phrase}
    outputDF=pd.DataFrame(mapofWords)
    outputDF.to_csv(r'ProcessedCSV/AbstractWordRanking.csv', index = True)
    return outputDF;
    
def PlotRanking(PlotDF):
    PlotDF.plot(kind='scatter',x='rank',y='frequency',color='red')
    plt.show()

df=pd.read_csv('ProcessedCSV/AnalyzedTitlesAbstract.csv', low_memory=False)
nlp = InitNLPPyTextRank();
f=open('wordbag.txt','w');####Fill this with the full text of abstracts for all selected papers flagged as cov19
for i in range(len(df)):
    AbstractText=df.loc[i,'abstract']
    TitleQualifiers=df.loc[i,'Title Qualifier Words']
    if AbstractText=="null" or isinstance(AbstractText,float):continue
    if not "covid19" in TitleQualifiers:continue
    #print(AbstractText)
    f.write(" "+AbstractText)
f.close()
print("All found abstracts in WordBag")
f=open('wordbag.txt','r');
print("Ranking")

phrases=RankWordsBag(f,nlp)
#print(phrases)
f.close()
print("Writing out CSV")
FillCSV(phrases,0.01,4)
