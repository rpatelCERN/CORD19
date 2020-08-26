import spacy
from InitNLP import *
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from CreateTopics import TopicKeywordSearch,TopicKeywordAbstractSearch,GetTopicWords,display_topics,CreateNMFTopics
import sys
from spacy.matcher import Matcher
import pandas as pd
from JSONInputsBodyText import *
from PreProcessingText import *
#CSVFILE=sys.argv[1]
#Topic=int(sys.argv[2])
#FILEPATH="551982_1312270_bundle_archive/"

def SkimallText(filepath,nlp):
    filename=filepath
    BodyText=[]
    for i in range(0,Nlines_in_paper(filename)):
        LineSentence=line_in_paper(filename,i)
        lines=LineSentence.split(".")
        docs = list(nlp.pipe(lines))
        for doc in docs:BodyText.append(clean_up_spacyDOCPIPE(doc))
    return BodyText;

def ReturnMatchedText(CSVFILE,Topic):

    df=pd.read_csv(CSVFILE, low_memory=False)
    df=df[df['topic']==Topic]
    df=df[~(df['matched_lines']=="None")]
    df['matched_lines']
    print(df.head(10))
    #f=open("TotalCORDTopics/Topic%d.txt" %Topic,'r')
    lines=df['matched_lines'].tolist()#.readlines();
    del df
    corpus=lines ### Chunks of matched lines in the document
    return list(set(corpus))



def BuildSummary(corpus):
    TotalSize=len(corpus)
    tfidf_vectorizer = TfidfVectorizer(max_df=5000)
    tfidf = tfidf_vectorizer.fit_transform(corpus)
    mostSimilar=0
    SimilarityArray=cosine_similarity(tfidf, tfidf)
    #print(SimilarityArray.shape)

    nx_graph = nx.from_numpy_array(SimilarityArray)#### Convert similarity matrix into a graph
    scores = nx.pagerank(nx_graph)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(corpus)), reverse=True)
    return ranked_sentences

####### For all documents find the most similar documents

def DocumentSimalarity(Filepath,CSVFILE,Topic):
    df=pd.read_csv(CSVFILE, low_memory=False)
    df=df[df['topic']==Topic]
    df=df[df['pdf_json_files'].notnull()]
    PubPaths=df['pdf_json_files'].tolist()
    df.loc[df['pmc_json_files'].notnull(),'Full PMC']=True
    df.loc[df['pdf_json_files'].notnull(),'Full PDF']=True
    df.loc[df['pmc_json_files'].notnull(),'Full PDF']=False#### look at PMC if both PMC and PDF are available
    #df.loc[df['pmc_json_files'].isnull(),'Full PMC']=False
    Titles=df[df['Full PMC']==True]['title'].tolist()
    Titles.extend(df[df['Full PDF']==True]['title'].tolist())

    PubPaths=df[df['Full PMC']==True]['pmc_json_files'].tolist()
    PDFPapers=df[df['Full PDF']==True]['pdf_json_files'].tolist()
    PubPaths.extend(PDFPapers)
#del df
    Corpus=[]
    nlpsci=InitSciSpacy();
    nlpsci.disable_pipes("parser","ner")

    for pub in PubPaths:
        BodyText=[]
        pub=pub.split("; ")
        for p in pub:
            #p=p.replace(" ","")
            print(p)
            SkimmedText=SkimallText(Filepath+p,nlpsci)
            if len(SkimmedText)==0:continue
            BodyText.extend(SkimmedText)####Full text not just the abstract
        Doc=".".join(BodyText)
        Corpus.append(Doc)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(Corpus)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    SimilarityArray=cosine_similarity(tfidf, tfidf)
    print(len(PubPaths),SimilarityArray.shape)
    nx_graph = nx.from_numpy_array(SimilarityArray)#### Convert similarity matrix into a graph
    scores = nx.pagerank(nx_graph)
    return scores,Titles
def ShortNotes(Topic,fbase):
        f=open("%sTopicSummary%d.txt" %(fbase,Topic),'r')
        paragraphs=f.readlines();
        total=int(len(paragraphs)*0.5)
        #if(len(paragraphs)>10):
        paragraphs=paragraphs[0:total]
        Corpus=[]
        for p in paragraphs:
            Corpus.extend(p.split("..."))
        #print(Corpus, len(Corpus))
        ranked_sentences=BuildSummary(Corpus)
        return ranked_sentences,Corpus
        #fshort=open("ShortNotes%d.txt" %Topic,'w')
        #for i in range(len(Corpus)):fshort.write(ranked_sentences[i][1]+'\n')#####Return this as a list
        #fshort.close()
def RunSummaries(FILEPATH,CSVFILE,Topic):

    Corpus=ReturnMatchedText(CSVFILE,Topic)
    filebase=CSVFILE.replace(".csv","")

    ranked_sentences=BuildSummary(Corpus)
    fout=open("%sTopicSummary%d.txt" %(filebase,Topic),'w')
    fout.seek(0)
    for i in range(len(Corpus)):fout.write(ranked_sentences[i][1]+'\n')#####Return this as a list
    fout.close()
#####For writing out a summary
#ranked_documents = sorted(((scores[i],s) for i,s in enumerate(Titles)), reverse=True)
    scores,Titles=DocumentSimalarity(FILEPATH,CSVFILE,Topic)
    fout=open("%sDocRanking%d.txt" %(filebase,Topic),'w')
    fout.seek(0)
    rank=[]
    titles=[]
    for i,s in enumerate(Titles):
        rank.append(scores[i])
        titles.append(s)
        fout.write("%g %s \n" %(scores[i],s))#####Return this as a list
    fout.close()
    OutputScores={'Rankscore':rank,'title':titles}
    OutputDF=pd.DataFrame(OutputScores)
    OutputDF.to_csv('%s_Topic%d.csv'%(filebase,Topic))

    ranked_sentences,Corpus=ShortNotes(Topic,filebase)
    fshort=open("%sShortNotes%d.txt" %(filebase,Topic),'w')
    for i in range(len(Corpus)):fshort.write(ranked_sentences[i][1]+'\n')#####Return this as a list
    fshort.close()
#RunSummaries()
