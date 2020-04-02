#import spacy
#import pytextrank
import pandas as pd
import re
import csv
from InitNLP import *
import sys
import string

def CoVQualifierMatch(phrases):
    qualifier=""

    for p in phrases:####Phrases sorted by rank
           #for punc in string.punctuation:p.replace(punc, "")####Don't want to use all english stop words only filter punctuation
           if "coronavirus" in p and "2019" in p:####Most likely COVID19
                   qualifier="covid19"
                   #match=True
                   #print(p)
                   break
           if "coronavirus" in p and ("2012" in p or "mers" in p or "middle east" in p) :#Middle East Respitory Syndrome
                   qualifier="mers"
                   match=True
                   break
           if "coronavirus" in p and "2003" in p:####2003 Sars epidemic
                      qualifier="sars"
                      #match=True
                      #print(p)
                      break
           if("coronavirus" in p or "cov" in p  or "coronaviruses" in p):################Check additional context of phrase
                   searchObj = re.search(r'(.*) CoV (.*?) .*',p,re.M|re.I)####Check CoV abbreviation with reg expression
                   ####Look at proceding and preceding words
                   if searchObj:
                       qualifier=" %s * %s" %( searchObj.group(1),searchObj.group(2))
                       #match=True
                       break;
                       
                   else:
                       searchObj = re.search(r'(.*) coronavirus (.*?) .*',p,re.M|re.I)#Check Coronavirus full word
                       if searchObj:
                               qualifier=" %s * %s" %( searchObj.group(1),searchObj.group(2))
                               #match=True
                               break;
                   if not searchObj:
                       searchObj = re.search(r'(.*) coronaviruses (.*?) .*',p,re.M|re.I) ###Check plural
                       if searchObj:
                               qualifier=" %s * %s" %( searchObj.group(1),searchObj.group(2))
                               #match=True
                               break;
           for punc in string.punctuation:qualifier.replace(punc, "")####Don't want to use all english stop words only filter punctuation
    return qualifier
def MatchTitlePhrasesAndAbstract(Titlephrases, AbstractPhrases ):
    tempQual=[]
    for p in AbstractPhrases:
        for titlep in Titlephrases:
            if titlep in p:
                tempQual.append(p)
    return tempQual;

df=pd.read_csv('%s' %sys.argv[1], low_memory=False) #Metadata for CORD-19
covid19_synonyms=["COVID","SARS-CoV-2","2019-nCoV","coronavirus disease","novel coronavirus","ncov coronavirus","wuhan coronavirus"]###First three based on my inital guess, the rest found with 2nd step using pyTextRank from all the found titles in a wordbag
#####Global Text ranking parameters
StopWords="StopWordsTitle.txt"
#NEW COLUMNS to FILL
Titlequalifiers=[]
qualifiers=[]
Matchedqualifiers=[]


for i in range(len(df)):
    title=df.loc[i,'title']
    abstracttext=df.loc[i,'abstract']
    if title=="null" or isinstance(title,float):title="title";
    SeveralTitleQual=[]
    
    for c in covid19_synonyms:
        if title.find(c)>=0 and title.find("middle east")==-1:#####Exclude mers
            SeveralTitleQual.append('covid19');
    nlp = InitNLPRake(StopWords);
    phrases=KeyPhrases(title,nlp);
    for p in phrases:SeveralTitleQual.append(p)
    Titlequalifiers.append(','.join(SeveralTitleQual));
    if abstracttext is "":
        qualifiers.append('')
        Matchedqualifiers.append('')
        continue #nan for missing entries
    if pd.isnull(abstracttext):
        qualifiers.append('')
        Matchedqualifiers.append('')
        continue #nan for missing entries
    #nlp = Rake()
    phrases=KeyPhrases(abstracttext,nlp); #just parse pharses and rank them
    
    qualifier=CoVQualifierMatch(phrases)
    if qualifier=="":
        qualifiers.append('Not Found')
    else:
        qualifiers.append(qualifier)
####Now have to sets of qualifiers from the title and the abstract, see what matches:
    if "covid19" in SeveralTitleQual:
        MatchedPhrases=MatchTitlePhrasesAndAbstract(phrases,SeveralTitleQual)
        Matchedqualifiers.append(MatchedPhrases);
    else: Matchedqualifiers.append('')
print(i,len(Matchedqualifiers))
#FILL CSV with Keywords found per paper
df.insert(8, "Title Qualifier Words", Titlequalifiers, True);
df.insert(9, "Abstract Qualifier Words", qualifiers, True);
df.insert(10, "Matched Abstract Qualifier Words", Matchedqualifiers, True);
df.to_csv(r'ProcessedCSV/AnalyzedTitlesAbstract.csv', index = True)
