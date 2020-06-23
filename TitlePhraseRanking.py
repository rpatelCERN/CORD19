#import spacy
#import pytextrank
import pandas as pd

import re
import csv
from InitNLP import *
import sys
import string
from PreProcessingText import clean_up_spacy
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher

def AddSpacyMatchTokens(nlp):
    matcher = Matcher(nlp.vocab)
    ###Influenza seperate H1N1 from specific outbreaks like swine flu and bird flu

    BirdFlu=[{"LOWER":{'IN':["avian","avian-origin"]}},{"LOWER":{'IN':["influenza","flu"]}}]
    matcher.add("BirdFlu",None, BirdFlu)
    SwineFlu=[{"LOWER":"swine","POS":"ADJ"},{"LOWER":{'IN':["influenza","flu"]}}]
    matcher.add("SwineFlu",None, SwineFlu)
    #### Everything else is the H1N1 or a  more general Flu
    Flu=[{'LOWER':{'NOT_IN': ["avian","avian-origin","swine","equine","canine","murine","bat"]}},{"LOWER":{'IN':["influenza","flu"]}}]
    matcher.add("Flu",None, Flu)

    #### Zoonotic influenza:
    #AnimalFlu=[{"LOWER":"canine","LOWER":"equine","LOWER":"murine"},{"LOWER":"influenza","LOWER":"flu"}]
    AnimalFlu=[{"LOWER":{'IN': ["equine","canine","murine","bat"]}},{"LOWER":"influenza"}]
    matcher.add("ZoonoticFlu",None, AnimalFlu)

    #### The same for coronaviruses
    ZooCorona=[{"LOWER":{'IN':["feline","equine","canine","murine","bat","porcine","bovine","bat","coronavirus"]}},{"LOWER":{'IN':["coronavirus","coronaviruses", "respiratory coronavirus","enteric coronavirus","hku15","coronavirus-512","delta coronavirus","deltacoronavirus"]}}]
    HumanCorona=[{"LOWER":"human"},{"LOWER":"coronavirus"},{"LOWER":{'IN':["nl63","oc43","229e","229E-infected","infections"]},"OP": "*"}]
    CoronaRemainder=[{"LOWER":{'NOT_IN':["equine","canine","murine","bat","porcine","bovine"]}},{"LOWER":{'IN':["coronavirus", "respiratory coronavirus"]}}]

    matcher.add("ZoonoticCorona",None, ZooCorona)
    matcher.add("HumanCorona",None, HumanCorona)


    #matcher.add("Corona",None, CoronaRemainder)

    return matcher


def AddSpacyMatchPatterns(nlp):
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    #####NOTE Patterns are case sensitive so may still need token matching for more coverage
    #### Titles though are always capitalized
    covid19_synonyms=["COVID","SARS-CoV-2","2019-nCoV","Coronavirus Disease","coronavirus disease","Novel Coronavirus","novel coronavirus","novel human coronavirus","Novel Human Coronavirus","ncov ","Wuhan Coronavirus"]###First three based on my inital guess, the rest found with 2nd step using pyTextRank from all the found titles in a wordbag

    patterns = [nlp.make_doc(text) for text in covid19_synonyms]#### OR Could be more general as a list of dicts
    matcher.add("COVID19", None, *patterns)
    HIVNames=["HIV-1", "HIV-2","HIV","AIDS","Human Immunodeficiency Virus"];
    patterns = [nlp.make_doc(text) for text in HIVNames]
    matcher.add("HIV", None, *patterns)
    patterns = [nlp.make_doc("Ebola")]
    matcher.add("Ebola", None, *patterns)
    Sars2003=["SARS","SARS-CoV"]
    patterns = [nlp.make_doc(text) for text in Sars2003]
    matcher.add("SARS2003", None, *patterns)
    MERS2012=["MERS","MERS-CoV","Middle East respiratory"]
    patterns = [nlp.make_doc(text) for text in MERS2012]
    matcher.add("MERS", None, *patterns)

    Zika=["zika","ZIKAV","Zika"]
    patterns = [nlp.make_doc(text) for text in Zika]
    matcher.add("zika", None, *patterns)
    patterns = [nlp.make_doc("West Nile")]
    matcher.add("WNileV", None, *patterns)
    GV=["viral gastroenteritis","Gastroenteritis"]
    patterns = [nlp.make_doc(text) for text in GV]
    matcher.add("VGastroEntritis", None, *patterns)

    #### For these need to know if it is human or non-human (zoonotic)
    #matcher.add("Flu", None, Flu)
    return matcher;

def MatchTitlePhrasesAndAbstract(Titlephrases, AbstractPhrases ):
    tempQual=[]
    for p in AbstractPhrases:
        #if p=="covid19":continue ####This is a marker I add myself to flag papers that feature one of the COVID19 synonyms
        for titlep in Titlephrases:
            if titlep in p:tempQual.append(p)
    return tempQual;

df=pd.read_csv('%s' %sys.argv[1], low_memory=False) #Metadata for CORD-19
####Use these to create SPACY match patterns


#####Global Text ranking parameters
StopWords="StopWordsTitle.txt"
stopwordlist=StopWordslist(StopWords);

#NEW COLUMNS to FILL
AllTitles=[]
Titlequalifiers=[]
ViralMatch=[]
Matchedqualifiers=[]
nlpsci=InitSciSpacy();
matcher=AddSpacyMatchPatterns(nlpsci)
matchtokens=AddSpacyMatchTokens(nlpsci);
nlp = InitNLPRake(StopWords);

#nlp=InitSciSpacy();
covid19_synonyms=["COVID","SARS-CoV-2","2019-nCoV","coronavirus disease","novel coronavirus","ncov coronavirus","wuhan coronavirus"]###First three based on my inital guess, the rest found with 2nd step using pyTextRank from all the found titles in a wordbag
df['title'].fillna("title", inplace=True)
df['abstract'].fillna("abstract", inplace=True)

#df.loc[df['title'].notnull(), 'TitleFilled'] = True
#df.loc[df['title'].isnull(), 'TitleFilled'] = False
#df.loc[df['abstract'].isnull(), 'TitleFilled'] = False
#SelectedRows=df[df['TitleFilled']==True]
ListOfTitleWords=df['title'].tolist()    #
ListOfAbstractWords=df['abstract'].tolist()    #
FullListTitleAbs=ListOfTitleWords
#FullListTitleAbs = [i +" " + j for i, j in zip(ListOfTitleWords, ListOfAbstractWords)]
print(len(FullListTitleAbs),len(df))
'''
for i in range(len(df)):
    title=df.loc[i,'title']
    pubtime=df.loc[i,'publish_time']
    abstracttext=df.loc[i,'abstract']
    if title=="null" or isinstance(title,float):title="title";
    #print(title,pubtime)
    AllTitles.append(title)
'''
    #### Also store all abstracts to look for COVID19 match patterns

docs = list(nlpsci.pipe(FullListTitleAbs))#### Matching based on Title and abstract, this part takes a lot of time
for doc in docs:
    #print(doc.text)
    matches=matcher(doc)
    tokmatches=matchtokens(doc)
    CheckCovid=False
    TempID=[]

    #for match_id, start, end in matches:
    for match_id, start, end in matches:
        #if nlpsci.vocab.strings[match_id]=="COVID19":CheckCovid=True
        TempID.append(nlpsci.vocab.strings[match_id])
    for match_id, start, end in tokmatches:TempID.append(nlpsci.vocab.strings[match_id])
    ViralMatch.append(TempID)
    #if CheckCovid:
    Titlephrases=KeyPhrases(doc,nlp);
    if(len(Titlephrases)>0):Titlephrases=clean_up_spacy(','.join(Titlephrases),nlpsci);
    print(doc.text)
    print(Titlephrases)
    Titlequalifiers.append(Titlephrases)###Filled Per Title

    #else:
    #    Titlequalifiers.append("NULL")

print(len(ViralMatch))
#FILL CSV with Keywords found per paper
df.insert(8, "Title Qualifier Words", Titlequalifiers, True);
df.insert(9, "Viral Tag", ViralMatch, True);
df.to_csv(r'ProcessedCSV/TestLatestData.csv', index = True)
