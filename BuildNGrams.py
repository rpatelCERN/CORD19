import pandas as pd

from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
import sys
from TitlePhraseRanking import AddSpacyMatchTokens
from InitNLP import *
from spacy.matcher import Matcher

matplotlib.rc('font',family='monospace')
plt.style.use('ggplot')

fig, ax = plt.subplots()
plt.xlabel("Keywords")
plt.ylabel("Count Freq.")

def testMatches(nlp,keywordlist):
    matchtokens=AddSpacyMatchTokens(nlp);
    docs = list(nlp.pipe(keywordlist))
    for doc in docs:
        tokmatches=matchtokens(doc)
        for match_id, start, end in tokmatches:
            if(nlp.vocab.strings[match_id]=="IBV"):print(doc[start:end])


def GetCountFrequency(skl_texts,no_most_frequent,dictForCleaning={}):
    #print(skl_texts)
    #tf_vectorizer = CountVectorizer(ngram_range=(1,2))
    #tf_vectorizer = CountVectorizer(ngram_range=(2,3),max_features=2000)
    tf_vectorizer = CountVectorizer(ngram_range=(2,3),max_features=30000,max_df=5000)
    #tf_vectorizer = CountVectorizer(ngram_range=(2,3))
    tf=tf_vectorizer.fit_transform(skl_texts)####transform and learn the vocab
    features = tf_vectorizer.get_feature_names()
    for key in dictForCleaning.keys():
        columnindexKey=features.index(key)
        columnindexValue=features.index(dictForCleaning[key])
        tf[:,columnindexValue]=tf[:,columnindexValue]+tf[:,columnindexKey]
        tf[:,columnindexKey]=0
    #print(features.index("mouse hepatitis virus"),tf[:,54596])
    '''
    #### Learned vocab from text
    #del vocab['mouse hepatitis']#### map to the same index "can't do that", so delete some of the bigrams
    '''

    #d=tf.toarray().sum(axis=0)
    #d = pd.Series(tf.toarray().flatten(),index = features).sort_values(ascending=False)
    d = pd.Series(tf.toarray().sum(axis=0),index = features).sort_values(ascending=False)

    #ax = d[:no_most_frequent].plot(kind='bar', figsize=(12,10), width=.8, fontsize=12, rot=22,title='Most Frequent Keywords')
    ax = d[:no_most_frequent].plot(kind='bar', figsize=(8,8), width=.8, fontsize=12, rot=22,title='Most Frequent Keywords')
    ax.title.set_size(18)
    #ax.set_autoscale(True)
    #plt.update_xaxes(automargin=True)
    plt.xlabel("Keywords")
    plt.ylabel("Count Freq.")
    plt.show()
    print(d[:no_most_frequent])
    return d
def defineNgrams(terms):
    defineNgrams={}
    #
    for w1 in terms:
        values=[]
        for w2 in terms:
            if(w1==w2):continue
            lev=fuzz.ratio(w1,w2);
            #if(w1=="severe acute" or w2=="severe acute"):


            if(lev>=66 and lev<100):

                if(len(w1.split(" "))==len(w2.split(" "))):continue
                #print(w1,w2,lev)
                if(len(w1)>len(w2)):
                    defineNgrams[w2]=w1
                else:
                    defineNgrams[w1]=w2

    return defineNgrams

def CompareNGramCleaning(AllKeywords,TopWordsToCount,TopWordsToBuild):
    Series=GetCountFrequency(AllKeywords,TopWordsToCount)
    terms=Series.nlargest(TopWordsToCount).keys()
    Series=GetCountFrequency(AllKeywords,TopWordsToBuild,defineNgrams(terms))
'''
df=pd.read_csv('%s'%sys.argv[1], low_memory=True,memory_map=True)
#df2=pd.read_csv('%s'%sys.argv[2], low_memory=False)
#df = pd.concat([df,df2])
#df['publish_time']=pd.to_datetime(df['publish_time'])
#df["publish_time"] = df["publish_time"].astype("datetime64")
#df=df[(df['publish_time']<'2020-1-31')]

#df.loc[df['abstract'].notnull(),'Paper Tag']=True
df.loc[df['abstract'].notnull(),'Paper Tag']=False
#df.loc[df['abstract'].str.contains("abstract"),'Paper Tag']=False

#df.loc[df['Viral Tag'].notnull(),'Paper Tag']=False
#df.loc[df['Viral Tag'].str.contains("SARS2003"),'Paper Tag']=True
#df.loc[df['Viral Tag'].str.contains("COVID19"),'Paper Tag']=True

df.loc[df['Title Qualifier Words'].notnull(),'Paper_Tag']=True

df.loc[df['Viral Tag'].str.contains("COVID19"),'Paper_Tag']=True
df.loc[df['Title Qualifier Words'].isnull(),'Paper_Tag']=False
SelectedRows=df[df['Paper_Tag']==True];

del df;
AllKeywords=SelectedRows['Title Qualifier Words'].tolist()
del SelectedRows;

CompareNGramCleaning(AllKeywords);
'''
