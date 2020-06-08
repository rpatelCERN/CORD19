import gensim
import numpy as np
import spacy
from spacy import displacy
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import matplotlib.pyplot as plt
import sklearn
import keras
import pandas as pd
from gensim.models import CoherenceModel, LdaModel, LsiModel, HdpModel
from gensim.models.wrappers import LdaMallet
import pyLDAvis.gensim
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pyLDAvis.sklearn
import warnings

from InitNLP import *
from spacy.matcher import Matcher

from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE  ####Just to look at potential topic clusters

import os
import sys
from PreProcessingText import clean_up_spacy


from JSONInputsBodyText import *

warnings.filterwarnings('ignore')  # Let's not pay heed to them right now

#nlp = spacy.load("en")

def display_topics(model, feature_names, no_top_words,topicIndex):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
            for i in topic.argsort()[:-no_top_words - 1:-1]]))
        if topic_idx is not topicIndex:continue
        f=open("TopicWords%d.txt" %topicIndex,'w')
        f.write(" ".join([feature_names[i]
            for i in topic.argsort()[:-no_top_words - 1:-1]]))
        f.close()
def GetTopicWords(model,feature_names,topicIndex,no_top_words ):
    KeywordsinTopic=[]
    for topic_idx, topic in enumerate(model.components_):
        if topic_idx!=topicIndex:continue
        #print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        KeywordsinTopic.append([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
    return KeywordsinTopic[0];
def TopicKeywordSearchBM25(KeywordsinTopic):

    for i in range(len(df)):
        sha=df.loc[i,'sha']
        sha=sha.split("; ")
        location=df.loc[i,'full_text_file^M']
        #print(KeywordsinTopic)
        BodyText=[]
        for s in sha:
            filename=PATH+location+"/"+location+"/"+s+".json"
            for i in range(0,Nlines_in_paper(filename)):
                LineSentence=line_in_paper(filename,i).split('.')
                for l in LineSentence:BodyText.append(l+'\n')### Linesin the paper
        for key in KeywordsinTopic:
            doc_scores,topsentences=BM25Search(BodyText,key,10)
            print(key,doc_scores,topsentences)

def TopicKeywordSearch(KeywordsinTopic,nlp,matcher,topicnumber):
    df=pd.read_csv('ProcessedCSV/AnalyzedTitlesAbstract.csv', low_memory=False)

    print(len(df))
    #cnt = Counter()
    #fout=open("%s.txt" %KeywordsinTopic[0], 'w')
    fout=open("Topic%d.txt" %topicnumber, 'w')
    MatchedText=[]

    for i in range(len(df)):
        TitleKeyWords=df.loc[i,'Title Qualifier Words']
        if isinstance(TitleKeyWords,float):continue
        ViralID=df.loc[i,'Viral Tag']

        if not "COVID19" in ViralID:continue
        Titles=df.loc[i,'title']
        #print(Titles)

        sha=df.loc[i,'sha']
        sha=sha.split("; ")
        location=df.loc[i,'full_text_file^M']
        #print(KeywordsinTopic)
        BodyText=[]
        for s in sha:
            filename=PATH+location+"/"+location+"/"+s+".json"
            for i in range(0,Nlines_in_paper(filename)):
                LineSentence=line_in_paper(filename,i).split('.')
                for l in LineSentence:BodyText.append(l)### Linesin the paper
        ##### Here we could use pyTextRank to summarize
        docs = list(nlp.pipe(BodyText))
        for doc in docs:
            matches=matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                #print(span,doc.text)#### Line in the body text
                #print(nlp.vocab.strings[match_id],span)
                MatchedText.append(doc.text)
                fout.write(doc.text +'\n')
    fout.close()
    return list(set(MatchedText))
    '''
        for s in sha:
            filename=PATH+location+"/"+location+"/"+s+".json"
            MatchInfo=SearchKeyWordList(KeywordsinTopic,filename)##### Insted look for match patterns in nlp
            for m in MatchInfo:print(m)
    '''
def AddSpacyMatchPatterns(nlp,doc,matcher,patternName):
    pattern=[]
    for token in doc:
        TextLabel="LOWER"
        text=token.text;
        if(token.pos_=="NOUN" or token.pos_=="VERB"):
            text=token.lemma_
            TextLabel="LEMMA"
        patterndict={TextLabel:token.text,"POS":token.pos_}
        pattern.append(patterndict)#### List of dictionaries

    #print(pattern, len(pattern))
    if len(pattern)>1 :matcher.add(patternName,None,pattern)
    return matcher
def TopicKeywordAbstractSearch(KeywordsinTopic,nlp,minRank):####Use pyTextRank
    df=pd.read_csv('ProcessedCSV/AnalyzedTitlesAbstract.csv', low_memory=False)
    #print(len(df))
    #cnt = Counter()
    Matches=[]

    for i in range(len(df)):
        TitleKeyWords=df.loc[i,'Title Qualifier Words']
        if isinstance(TitleKeyWords,float):continue
        ViralID=df.loc[i,'Viral Tag']

        if not "COVID19" in ViralID:continue

        Titles=df.loc[i,'title']
        Abstract=df.loc[i,'abstract']
        if Abstract=="null" or isinstance(Abstract,float):continue

        phrases=TextRank(Abstract,nlp)
        #print(phrases)
        #### parse it into phrases
        for kw in KeywordsinTopic:
            for p in phrases:
                if kw in p.text and p.rank>minRank:
                    cleantext=clean_up_spacy(p.text,nlp)
                    #print(kw,p.text,p.rank)
                    Matches.append(cleantext)
    return list(set(Matches));
        #print(Matches)
def FillSciKitText(doc,my_stop_words):
    # we add some words to the stop word list
    texts, article,skl_texts = [], [],[]
    for w in doc:
        if w.text in my_stop_words:continue
        #print(w.text)
        # if it's not a stop word or punctuation mark, add it to our article!
        if w.text != '\n ' and not w.is_stop and not w.is_punct and not w.like_num and w.text != 'I':
            # we add the lematized version of the word
            #print(w.lemma_)
            article.append(w.lemma_)

            if w.text == '\n':
                #print("here after \n")
                if(article==[]):continue
                texts.append(article)
                skl_texts.append(' '.join(article))
    #skl_texts=list(set(skl_texts))#### Only unique entries
    return skl_texts
def CreateLDATopics(skl_texts,no_features,no_topics):

    #######Count vectorizer and LDA SciTopics############
    tf_vectorizer = CountVectorizer(max_features=no_features)

    tf = tf_vectorizer.fit_transform(skl_texts)
    tf_feature_names = tf_vectorizer.get_feature_names()
    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=10, learning_method='online')
    lda.fit(tf)
    visualize=pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    #visualize=pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(visualize, 'lda.html')
    return lda,tf_feature_names
def CreateNMFTopics(skl_texts,no_features,no_topics):
    #######TFIDF vectorizer and NMF SciTopics############
    tfidf_vectorizer = TfidfVectorizer(max_features=no_features)
    tfidf = tfidf_vectorizer.fit_transform(skl_texts)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    nmf = NMF(n_components=no_topics, random_state=1,beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,l1_ratio=.5).fit(tfidf)
    return nmf,tfidf_feature_names


def BuildTopics(doLDA,PATH,no_topics,no_top_words,no_features):

    no_topics =10*2
    no_top_words = 5*2



    nlp = InitNLPPyTextRank();
    #no_features = 2000
    #no_top_words = 5*2

    #PATH="../CORD-19-research-challenge/"#"%s" %sys.argv[1]

    print("HERE")
    
    f=open("TitlewordbagTotal.txt",'w');
    df=pd.read_csv('ProcessedCSV/AnalyzedTitlesAbstract.csv', low_memory=False)
    ###For testing words to look for:
    TestWords=[' study',' ace2',' receptor',' expression',' single',' human',' domain',' cell',' bind',' infection',' protein',' cause',' descriptive',' immune',' clinical',' analysis',' case',' center',' epidemic', ' epidemiological']
    #TestWords=[' vaccine ',' ace2 ',' ship ',' healthcare ',' policy ',' policies ', ' intensive ',' potential ',' quarantine ',' pneumonia ']
    for i in range(len(df)):
        TitleQualifiers=df.loc[i,'Title Qualifier Words']
        ViralID=df.loc[i,'Viral Tag']
        #WHOCOV=df.loc[i,'who_covidence_id']
        if TitleQualifiers=="null" or isinstance(TitleQualifiers,float):continue
        #if isinstance(WHOCOV,float): print(TitleQualifiers)

#        if not ("COVID19" in ViralID or not isinstance(WHOCOV,float))  :continue
        if not "COVID19" in ViralID   :continue
        #Writeout=False
        #for test in TestWords:
            #if(test in TitleQualifiers ):
        Writeout=True;
        #print(TitleQualifiers)
        #break;
        if Writeout:f.write(TitleQualifiers+'\n')


    f.close()
    f=open("TitlewordbagTotal.txt",'r');
    f.seek(0)
    text=f.read();

    doc = nlp(text.lower())
    my_stop_words = ['novel','preprint','copyright','medrxiv','author','peer','holder','et_al','cov', '\\ncov', '2019', 'ncov', 'sars', 'covid', 'coronavirus','hcov','19','2019','2019-ncov','covid-19','covid-','cov','title']
    my_stop_words.append('wuhan')
    my_stop_words.append('china')
    my_stop_words.append('disease')
    my_stop_words.append('outbreak')

    skl_texts=FillSciKitText(doc,my_stop_words)


    print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
    nmf,tfidf_feature_names=CreateNMFTopics(skl_texts,no_features,no_topics)
    #print("done in %0.3fs." % (time() - t0))

    if doLDA: #Do LDA:
        #######Count vectorizer and LDA SciTopics############
        lda,tf_feature_names=CreateLDATopics(skl_texts,no_features,no_topics)
        display_topics(lda, tf_feature_names, no_top_words)
        #print("done in %0.3fs." % (time() - t0))
    #### HERE MAKE A LOOP over topics

    for i in range(no_topics):
        display_topics(nmf, tfidf_feature_names, no_top_words,i)

        #if i is not 19:continue
        TestKeyWords=GetTopicWords(nmf,tfidf_feature_names,i,no_top_words); #### About vaccines and drug interventions
        MatchedPhrases=TopicKeywordAbstractSearch(TestKeyWords,nlp,0.04)
        #print(MatchedPhrases)
        nlpsci=InitSciSpacy();
        docs = list(nlpsci.pipe(MatchedPhrases))

        matcher = Matcher(nlpsci.vocab)
        for doc in docs:AddSpacyMatchPatterns(nlpsci,doc,matcher,"KeyPhrasesTopic%d"%i)
        MatchedText=TopicKeywordSearch(MatchedPhrases,nlpsci,matcher,i)
#PATH="../../CORD-19-research-challenge/"
#no_topics=20
#no_top_words=30
#no_features=600
#BuildTopics(False,PATH,no_topics,no_top_words,no_features)
