#import spacy
#import pytextrank
import pandas as pd

import re
import csv
from InitNLP import *
#import sys
import string
from PreProcessingText import clean_up_spacy
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher


def AddSpacyMatchTokens(nlp):
    matcher = Matcher(nlp.vocab)
    ###Influenza seperate H1N1 from specific outbreaks like swine flu and bird flu
    EM=[{"LOWER":"electron"},{"LOWER":"microscopy"}]
    matcher.add("EM",None,EM)
    BirdFlu=[{"LOWER":{'IN':["avian","avian-origin"]}},{"LOWER":{'IN':["influenza","flu"]}}]
    matcher.add("BirdFlu",None, BirdFlu)
    SwineFlu=[{"LOWER":"swine","POS":"ADJ"},{"LOWER":{'IN':["influenza","flu"]}}]
    matcher.add("SwineFlu",None, SwineFlu)
    #### Everything else is the H1N1 or a  more general Flu
    Flu=[{'LOWER':{'NOT_IN': ["avian","avian-origin","swine","equine","canine","murine","bat"]}},{"LOWER":{'IN':["influenza","flu"]}}]
    matcher.add("Flu",None, Flu)

    #### Zoonotic influenza:
    AnimalFlu=[{"LOWER":{'IN': ["equine","canine","murine","bat"]}},{"LOWER":"influenza"}]
    matcher.add("ZoonoticFlu",None, AnimalFlu)

    #### The same for coronaviruses
    ZooCorona=[{"LOWER":{'IN':["avian","feline","equine","canine","murine","bat","porcine","bovine","bat","coronavirus"]}},{"LOWER":{'IN':["coronavirus","coronaviruses", "respiratory coronavirus","enteric coronavirus","hku15","coronavirus-512","delta coronavirus","deltacoronavirus"]}}]
    HumanCorona=[{"LOWER":"human"},{"LOWER":"coronavirus"},{"LOWER":{'IN':["nl63","oc43","oc 43","229e","HKU1","229E-infected","infections"]},"OP": "*"}]
    CoronaRemainder=[{"LOWER":{'NOT_IN':["equine","canine","murine","bat","porcine","bovine"]},"OP":"?"},{"LOWER":{'IN':["coronavirus","coronaviruses", "respiratory coronavirus"]}}]
    CommonCold=[{"LOWER":"common"},{"LOWER":"cold"}]
    matcher.add("CommonCold",None,CommonCold)
    CommonCold=[{"LOWER":"rhinovirus"}]
    matcher.add("CommonCold",None,CommonCold)

    Heptatis=[{"LOWER":{'IN':["mouse","murine"]},"OP":"?"},{"LOWER":"hepatitis"}]
    matcher.add("ZoonoticCorona",None, ZooCorona)
    matcher.add("HumanCorona",None, HumanCorona)
    matcher.add("CoronaUnclassified",None, CoronaRemainder)

    matcher.add("Hep",None,Heptatis)
    AvianCorona=[{"LOWER":{'IN':["infectious","bronchitis","avian"]}},{"LOWER":{'IN':["bronchitis","infectious","coronavirus"]}},{"LOWER":"virus","OP":"?"}]
    Scelorsis=[{"LOWER":"multiple"}, {"LOWER":"sclerosis"}]
    matcher.add("MS",None,Scelorsis)
    matcher.add("IBV",None,AvianCorona)
#Add ARDS acute respiratory distress (Can be missing) syndrome
    ARDS=[{"LOWER":"acute"},{"LOWER":"respiratory"},{"LOWER":"distress","OP":"?"},{"LOWER":"syndrome"}]
    matcher.add("ARDS",None,ARDS)

    Pneu=[{"LOWER":{'IN':["pneumoniae","pneumonia"]}}]
    matcher.add("Pneumonia",None,Pneu)
    Asthma=[{"LOWER":{'IN':["asthma","asthmatic"]}}]
    matcher.add("asthma",None,Asthma)
    GV=[{"LOWER":"viral","OP":"?"},{"LOWER":"transmissible"},{"LOWER":"gastroenteritis"},{"LOWER":"virus","OP":"?"}]
    matcher.add("VGastroEntritis", None, GV)

    PRRS=[{"LOWER":"porcine"},{"LOWER":{"IN":["reproductive","respiratory"]},"OP":"+"},{"LOWER":{"IN":["virus","syndrome"]},"OP":"?"}]
    matcher.add("PorcineRRVirus", None, PRRS)

    PCR=[{"LOWER":"reverse","OP":"?"},{"LOWER":"transcription","OP":"?"},{"IS_PUNCT": True,"OP":"?"},{"LOWER":"polymerase"}, {"LOWER":"chain"},{"LOWER":"reaction"}]
    matcher.add("PCR", None, PCR)
    ACE=[{"LOWER":"angiotensin", "OP":"?"}, {"LOWER":"convert"}, {"LOWER":"enzyme"}]
    ACE2=[{"LOWER":"ace2"}]
    matcher.add("ACE",None,ACE)
    matcher.add("ACE",None,ACE2)
    Public=[{"LOWER":"public", "LOWER":"health"}]
    matcher.add("PublicHealth",None,Public)
    ELISA=[{"LOWER":"enzyme","OP":"?"},{"IS_PUNCT": True, "OP":"?"},{"LOWER":"linked"},{"LOWER":"immunosorbent"},{"LOWER":"assay"}]
    matcher.add("ELISA",None,ELISA)

    MonoAnti=[{"LOWER":"monolocal"},{"LEMMA":"antibodies"}]
    matcher.add("MonoAnti",None,MonoAnti)
    return matcher


def AddSpacyMatchPatterns(nlp):
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    #####NOTE Patterns are case sensitive so may still need token matching for more coverage
    #### Titles though are always capitalized
    covid19_synonyms=["COVID","covid","SARS-CoV-2","2019-nCoV","severe acute respiratory syndrome coronavirus","novel coronavirus","novel human coronavirus","ncov ","wuhan coronavirus","coronavirus disease"]###First three based on my inital guess, the rest found with 2nd step using pyTextRank from all the found titles in a wordbag

    patterns = [nlp.make_doc(text) for text in covid19_synonyms]#### OR Could be more general as a list of dicts
    matcher.add("COVID19", None, *patterns)
    HIVNames=["HIV-1", "HIV-2","HIV","AIDS","human immunodeficiency virus"];
    patterns = [nlp.make_doc(text) for text in HIVNames]
    matcher.add("HIV", None, *patterns)
    patterns = [nlp.make_doc("Ebola")]
    matcher.add("Ebola", None, *patterns)
    Sars2003=["SARS","SARS-CoV","sars coronavirus","sars","sars cov","severe acute respiratory syndrome","sars coronavirus","respiratory syndrome coronavirus","acute respiratory syndrome coronavirus","sars associated coronavirus"]
    patterns = [nlp.make_doc(text) for text in Sars2003]
    matcher.add("SARS2003", None, *patterns)
    MERS2012=["MERS","MERS-CoV","middle east respiratory","middle east respiratory syndrome","coronavirus middle east","severe acute respiratory syndrome middle east","middle east respiratory syndrome coronavirus","mers cov","mers"]
    patterns = [nlp.make_doc(text) for text in MERS2012]
    matcher.add("MERS", None, *patterns)

    Zika=["zika","ZIKAV","Zika"]
    patterns = [nlp.make_doc(text) for text in Zika]
    matcher.add("zika", None, *patterns)
    patterns = [nlp.make_doc("West Nile")]
    matcher.add("WNileV", None, *patterns)
    GV=["viral gastroenteritis","Gastroenteritis","gastroenteritis"]
    patterns = [nlp.make_doc(text) for text in GV]
    matcher.add("VGastroEntritis", None, *patterns)
    CommonBirdFluStrains=["H5N1", "H7N3", "H7N7", "H7N9","H9N2"]
    patterns = [nlp.make_doc(text) for text in CommonBirdFluStrains]
    matcher.add("BirdFlu",None, *patterns)
    patterns=[nlp.make_doc('respiratory syncytial virus')]
    matcher.add("RSV", None, *patterns)
    ViralGenome=['nucleotide sequence','open reading frame','ribosomal frameshifting','gene expression','gene transfer']
    patterns = [nlp.make_doc(text) for text in ViralGenome]
    matcher.add("VGenome", None, *patterns)
    patterns=[nlp.make_doc('intensive care unit')]
    matcher.add("ICU", None, *patterns)

    patterns=[nlp.make_doc('porcine epidemic diarrhea')]
    matcher.add("PEDV", None, *patterns)
    MitigationMeasures=['social media','social distancing','personal protective equipment','machine learning']
    patterns = [nlp.make_doc(text) for text in ViralGenome]
    matcher.add("MitigationMeasures", None, *patterns)
    patterns=[nlp.make_doc('feline infectious peritonitis')]
    matcher.add("ZoonoticCorona",None, *patterns)
    return matcher;

def MatchTitlePhrasesAndAbstract(Titlephrases, AbstractPhrases ):
    tempQual=[]
    for p in AbstractPhrases:
        for titlep in Titlephrases:
            if titlep in p:tempQual.append(p)
    return tempQual;
def RakeTitleAbstract(df,Cutoff,YearBegin,YearEnd):
    # #Metadata for CORD-19
    #NEW COLUMNS to FILL
    AllTitles=[]
    Titlequalifiers=[]
    ViralMatch=[]
    Matchedqualifiers=[]
    nlpsci=InitSciSpacy();
    matcher=AddSpacyMatchPatterns(nlpsci)
    matchtokens=AddSpacyMatchTokens(nlpsci);
    nlp = InitNLPRake();
    df['title'].fillna("title", inplace=True)
    df['abstract'].fillna("abstract", inplace=True)
    stopwords=['abstract','title','vivo','datum','subject','index','article']
    for w in stopwords:nlpsci.vocab[w].is_stop = True;
    ListOfTitleWords=df['title'].tolist()    #
    ListOfAbstractWords=df['abstract'].tolist()    #
    FullListTitleAbs=ListOfTitleWords
    FullListTitleAbs = [i +" " + j for i, j in zip(ListOfTitleWords, ListOfAbstractWords)]


    docs = list(nlpsci.pipe(FullListTitleAbs))#### Matching based on Title and abstract, this part takes a lot of time
    for doc in docs:
        #print(doc.text)
        matches=matcher(doc)
        tokmatches=matchtokens(doc)
        CheckCovid=False
        TempID=[]
        for match_id, start, end in matches:
            TempID.append(nlpsci.vocab.strings[match_id])
        for match_id, start, end in tokmatches:TempID.append(nlpsci.vocab.strings[match_id])
        ViralMatch.append(TempID)
        Titlephrases=KeyPhrases(doc,nlp);
        NRanked=len(Titlephrases)

        if(NRanked>Cutoff):Titlephrases=Titlephrases[0:Cutoff]
        if(len(Titlephrases)>0):Titlephrases=clean_up_spacy(' '.join(Titlephrases),nlpsci);
        Titlequalifiers.append(Titlephrases)###Filled Per Title

    #FILL CSV with Keywords found per paper
    df.insert(8, "Title Qualifier Words", Titlequalifiers, True);
    df.insert(9, "Viral Tag", ViralMatch, True);
    df.to_csv(r'ProcessedCSV/AnalyzedTitles%dto%d.csv' %(YearBegin,YearEnd), index = True)
#RakeTitleAbstract(20)
