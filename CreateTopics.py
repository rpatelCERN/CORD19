import gensim
import numpy as np
import spacy
from spacy import displacy
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import matplotlib.patches as mpatches
import matplotlib
import sklearn
import pandas as pd
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel
#from gensim.models.wrappers import LdaMallet
import pyLDAvis.gensim
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.manifold import TSNE

import pyLDAvis.sklearn
import warnings

from InitNLP import *
from spacy.matcher import Matcher,PhraseMatcher

from matplotlib import pyplot as plt
import seaborn as sns
from celluloid import Camera
#from sklearn.manifold import TSNE  ####Just to look at potential topic clusters

import os
import sys
from PreProcessingText import *
from JSONInputsBodyText import *

import psutil
warnings.filterwarnings('ignore')  # Let's not pay heed to them right now

def SelectDFRows(df,TagisTrue, TagisFalse):
    df.loc[df['Viral Tag'].notnull(),'Paper_Tag']=False
    for t in TagisTrue:df.loc[df['Viral Tag'].str.contains(t),'Paper_Tag']=True
    for t in TagisFalse:df.loc[df['Viral Tag'].str.contains(t),'Paper_Tag']=False

    df.loc[df['Title Qualifier Words'].isnull(),'Paper_Tag']=False
    df=df[df['Paper_Tag']==True];
    return df
def FillSciKitText(doc):
    # we add some words to the stop word list
    texts, article,skl_texts = [], [],[]
    for w in doc:
        # if it's not a stop word or punctuation mark, add it to our article!
        if w.text != '\n ' and not w.is_stop and not w.is_punct and not w.like_num and w.text != 'I':
        #if w.text != '\n ' and not w.is_stop and not w.is_punct and not w.like_num and w.text != 'I':
            article.append(w.text)
    if(article!=[]):#continue
        texts.append(article)
        skl_texts.append(' '.join(article))
    return skl_texts,texts

def CreateNMFTopics(skl_texts,no_features,no_topics):
    #######TFIDF vectorizer and NMF SciTopics############
    tfidf_vectorizer = TfidfVectorizer(max_features=no_features,ngram_range=(2,3),max_df=5000)##### Set MinDF and MaxDF
    tfidf = tfidf_vectorizer.fit_transform(skl_texts)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    dictDuplicateTerms=CreateNgramsDict(tfidf,tfidf_feature_names,50)
    tfidf=CleanNgrams(dictDuplicateTerms,tfidf,tfidf_feature_names)
    nmf = NMF(n_components=no_topics, random_state=1,beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,l1_ratio=.5).fit(tfidf)
    return nmf,tfidf_feature_names,tfidf

def display_topics(model, feature_names, no_top_words,topicIndex=0,writeout=False,fbase=""):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(", ".join([feature_names[i]for i in topic.argsort()[:-no_top_words - 1:-1]]))
        if topic_idx is not topicIndex:continue
        if not writeout:continue
        f=open("TopicWords"+"%s_%d.txt" %(fbase,topicIndex),'w')
        f.write(", ".join([feature_names[i]
            for i in topic.argsort()[:-no_top_words - 1:-1]]))
        f.close()

def GetTopicWords(model,feature_names,topicIndex,no_top_words ):
    KeywordsinTopic=[]
    for topic_idx, topic in enumerate(model.components_):
        if topic_idx!=topicIndex:continue
        #print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        KeywordsinTopic.append([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
    return KeywordsinTopic[0];


def MatchDocPhrases(PATH,AbstractKeyWords,nlp,pmatcher,SelectedRows):
    SelectedRows.loc[SelectedRows['pmc_json_files'].notnull(),'Full PMC']=True
    SelectedRows.loc[SelectedRows['pdf_json_files'].notnull(),'Full PDF']=True
    SelectedRows.loc[SelectedRows['pmc_json_files'].notnull(),'Full PDF']=False#### look at PMC if both PMC and PDF are available

    #SelectedRows.loc[SelectedRows['pmc_json_files'].isnull(),'Full PMC']=False
    PMCPapers=SelectedRows[SelectedRows['Full PMC']==True]['pmc_json_files'].tolist()
    PDFPapers=SelectedRows[SelectedRows['Full PDF']==True]['pdf_json_files'].tolist()
    PMCPapers.extend(PDFPapers)
    DocsMatched=[]
    for location in PMCPapers:#### Can't do loc anymore
            sha=location.split("; ")
            Body=[]
            for s in sha:
                filename=PATH+s
                for i in range(0,Nlines_in_paper(filename)):Body.append(line_in_paper(filename,i))
            docs = list(nlp.pipe(Body))
            for doc in docs:
                pmatches=pmatcher(doc)
                if(len(pmatches)>0):
                    DocsMatched.append(location)
                    break;
                    #Body.append(LineSentence)
    return DocsMatched
            #MatchBodyText=[for doc in pmatcher.pipe(Body)]#### Test this someplace


def TopicKeywordAbstractSearch(KeywordsinTopic,nlp,minRank,SelectedRows,Topic):####Use pyTextRank
    SelectedRows.loc[SelectedRows['abstract'].notnull(),'FilledAbs']=True
    SelectedRows.loc[SelectedRows['abstract'].isnull(),'FilledAbs']=False
    SelectedRows.loc[SelectedRows['abstract']=='abstract','FilledAbs']=False
    TopicAbstracts=SelectedRows[SelectedRows['FilledAbs']==True]
    TopicAbstracts['abstract']=TopicAbstracts['abstract'].str.lower()### Need this to match topic words
    TopicAbstracts['FilledAbs%d' %Topic]=False;
    for kw in KeywordsinTopic:TopicAbstracts.loc[TopicAbstracts['abstract'].str.contains(kw.strip()),'FilledAbs%d' %Topic]=True
    Abstracts=TopicAbstracts[TopicAbstracts['FilledAbs%d' %Topic]==True]['abstract'].tolist()
    del TopicAbstracts;
    PassingMatches=[]
    AllRankedPhrases=[]
    #Abstracts=[]
    #for doc in docs:Abstracts.append(clean_up_spacyDOCPIPE(doc))
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
        if p.count>=40:continue
        rankedtext=p.text
        rankedtext=rankedtext.replace("abstract","")
        #if p.rank>0.06 and p.count<=5:PassingMatches.append(rankedtext)# and p.count>=6):print(p.text,p.rank,p.count)

        for kw in KeywordsinTopic:
                if kw in p.text and p.rank>minRank:#Require a minimum rank
                    PassingMatches.append(rankedtext)
                    break;
    return list(set(PassingMatches));

def TopicKeywordSearch(PATH,KeywordsinTopic,nlp,pmatcher,topicnumber,PMCPapers,fbase=""):

    MatchedText=[]
    MatchIndex=[]
    for i in range(len(PMCPapers)):
        sha=PMCPapers[i].split("; ")
        BodyText=[]
        for s in sha:
            filename=PATH+s;
            for j in range(0,Nlines_in_paper(filename)):
                LineSentence=line_in_paper(filename,j).split('.')
                for l in LineSentence:BodyText.append(l)### Sentences in the paper
        ##### Here we could use pyTextRank to summarize
        MatchedTextPub=[]
        docs = list(nlp.pipe(BodyText))
        for doc in docs:
            #matches=matcher(doc)
            pmatches=pmatcher(doc)
            #for match_id, start, end in pmatches:
            #    span = doc[start:end]
                #print(nlp.vocab.strings[match_id],span)
            if(len(pmatches)>0):MatchedTextPub.append(doc.text) ## append the sentence if there is a match
        if(len(MatchedTextPub)>0):
            MatchedText.append("... ".join(MatchedTextPub))### All matched sentences are merged together with a symbol ... for further splitting
            MatchIndex.append(i)
            #print(PMCPapers[i])
            #print(MatchedTextPub)
            #print(i)

    #MatchedText=list(set(MatchedText))
    fout=open("Topic"+"%s_%d.txt" %(fbase,topicnumber), 'w')
    for text in MatchedText:fout.write(text +'\n')
    fout.close()
    return MatchedText,MatchIndex



def OutputCSV(SelectedRows,no_topics,MatchedPapersTopics,DFMatchedText,DFMatchedInd):
        DFTopics=[]
        for i in range(0,no_topics):
            Publications=MatchedPapersTopics[i]
            MatchedText=DFMatchedText[i]
            MatchIndex=DFMatchedInd[i]
            #### This will need to be ordered so that the index matches the order of Publications
            SelectedPub=SelectedRows[(SelectedRows['pmc_json_files'].isin(Publications)) | (SelectedRows['pdf_json_files'].isin(Publications))]
            SelectedPub=SelectedPub.reset_index(drop=True)#This resets the index to the default integer index.
            #SelectedPub=SelectedPub.reindex();
            print(SelectedPub.head())
            #df=df.reindex();

            SortedPubIndex=[]
            for j in range(len(Publications)):
                #print(Publications[j],type(Publications[j]))
                if('pdf_json' in Publications[j]):
                    DFIndex=SelectedPub[SelectedPub['pdf_json_files'].str.strip()==Publications[j]]
                    SortedPubIndex.append(DFIndex.index[0])
                    del DFIndex
                else:
                    DFIndex=SelectedPub[SelectedPub['pmc_json_files'].str.strip()==Publications[j]]
                    SortedPubIndex.append(DFIndex.index[0])
                    del DFIndex
                #SortedPubIndex.append(SelectedPub[SelectedPub['pdf_json_files'].str.strip().contains(Publications[j])| SelectedPub['pmc_json_files'].str.strip().contains(Publications[j])].index[0])
                if not j in MatchIndex:
                    MatchedText.insert(j,"None")### Make it the same length as publications
            #######This is the right order with publications
            SelectedPub=SelectedPub.reindex(SortedPubIndex)
            SelectedPub.insert(len(SelectedPub.columns),'Publications',Publications)
            SelectedPub.insert(len(SelectedPub.columns),'matched_lines',MatchedText)
            SelectedPub.insert(len(SelectedPub.columns),'topic',i)
            DFTopics.append(SelectedPub)
            del SelectedPub;
        outputDF=pd.concat(DFTopics)
        return outputDF;

def BuildTopics(PATH,stop_words,SelectedRows,no_topics,no_top_words,no_features,outputDFname,pytextrank):

    nlp = InitNLPPyTextRank();
    nlp.disable_pipes("ner")
    nlp.vocab['abstract'].is_stop = True;
    ##### Make this an nlp pipeline instead for the list

    for w in stop_words:nlp.vocab[w].is_stop = True;

    print("Building Topics")


    ListOfTitleWords=SelectedRows['Title Qualifier Words'].tolist()
    SelectedRows.drop(columns=['Unnamed: 0','Unnamed: 0.1','authors','doi','journal','source_x','pmcid','pubmed_id','license','arxiv_id','s2_id','Paper_Tag','mag_id','pmcid','pubmed_id','Viral Tag'],axis=1, inplace=True)
    ######Make this a new function with ListOfTitleWords as JSONInputsBodyText

    #text="\n".join(ListOfTitleWords); ##### Just a really long bow string
    #################  No need to go from .txt back to a text string
    skl_texts=[]
    docs = list(nlp.pipe(ListOfTitleWords))
    for doc in docs:
        tempskl_texts,texts=FillSciKitText(doc)
        skl_texts.extend(tempskl_texts)
    print(len(skl_texts))

    print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
    nmf,tfidf_feature_names,tfidf=CreateNMFTopics(skl_texts,no_features,no_topics)
    display_topics(nmf, tfidf_feature_names, no_top_words)
    nmf_embedding = nmf.transform(tfidf)#### Use this to look up papers

    ######## Make this a lookup function
    nmf_embedding = (nmf_embedding - nmf_embedding.mean(axis=0))/nmf_embedding.std(axis=0)
    top_idx = np.argsort(nmf_embedding,axis=0)[-100:]### Top 100 matches
    topic=0
    MatchedPapersTopics=[]
    DFMatchedText=[]
    DFMatchedInd=[]

    #### HERE MAKE A LOOP over topics
    for idxs in top_idx.T:
        print("\nTopic {}:".format(topic))
        MatchedPubs=[]
        matchDFind=[]
        for idx in idxs:
            if(isinstance(SelectedRows.iloc[idx]['pdf_json_files'],float) and isinstance(SelectedRows.iloc[idx]['pmc_json_files'],float)):continue
            if not isinstance(SelectedRows.iloc[idx]['pmc_json_files'],float):
                MatchedPubs.append(SelectedRows.iloc[idx]['pmc_json_files'])
            elif not isinstance(SelectedRows.iloc[idx]['pdf_json_files'],float):
                MatchedPubs.append(SelectedRows.iloc[idx]['pdf_json_files'])
        display_topics(nmf, tfidf_feature_names, no_top_words,topic, True,outputDFname)
        print("Topic %d" %topic)
        TestKeyWords=GetTopicWords(nmf,tfidf_feature_names,topic,no_top_words); #### About vaccines and drug interventions

        MatchedPhrases=TopicKeywordAbstractSearch(TestKeyWords,nlp,pytextrank,SelectedRows,topic)#### This can take a while
        ##### In text files: topic words, phrases.
        nlpsci=InitSciSpacy();
        nlpsci.disable_pipes("tagger","parser","ner")
        docs = list(nlpsci.pipe(MatchedPhrases))
        Pmatcher = PhraseMatcher(nlpsci.vocab, attr="LOWER")
        Pmatcher.add("KeyPhrasesTopic%d"%topic, None, *docs)
        MatchedDocs=MatchDocPhrases(PATH,MatchedPhrases,nlpsci,Pmatcher,SelectedRows)
        MatchedPubs.extend(MatchedDocs)
        MatchedPubs=list(set(MatchedPubs))#### Remove overlapping matches
        print(len(MatchedPubs))
        MatchedPapersTopics.append(MatchedPubs)#### All matched publications for topic
        MatchedText,MatchIndex=TopicKeywordSearch(PATH,MatchedPhrases,nlpsci,Pmatcher,topic,MatchedPubs,outputDFname)
        DFMatchedText.append(MatchedText)
        DFMatchedInd.append(MatchIndex)
        topic += 1

    #### Save all info as a df: sha, title, pub_time, full_pub_link,topic number, rank embed (0,100), matched based on phrase (0,1)
    outputDF=OutputCSV(SelectedRows,no_topics,MatchedPapersTopics,DFMatchedText,DFMatchedInd)
    outputDF.to_csv(outputDFname+".csv")
    del SelectedRows;
#### Make these arguments

def RunTopicBuilding(df,PATH,SetTrue,SetFalse,no_topics,outputDFname,stopwords,pytextrank=0.02):
    no_top_words=10
    no_features=30000

    SelectedRows=SelectDFRows(df,SetTrue,SetFalse)#df[df['Paper_Tag']==True];
    del df;

    BuildTopics(PATH,stopwords,SelectedRows,no_topics,no_top_words,no_features,outputDFname,pytextrank)
