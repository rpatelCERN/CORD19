from sklearn.manifold import TSNE
from CreateTopics import FillSciKitText,CreateNMFTopics,SelectDFRows
from InitNLP import *
from matplotlib import pyplot as plt
import seaborn as sns
from celluloid import Camera
import matplotlib
import pandas as pd
import sys
matplotlib.rc('font',family='monospace')
plt.style.use('ggplot')

fig, ax = plt.subplots()
plt.xlabel("tsne Dimension 1")
plt.ylabel("tsne Dimension 2")
camera = Camera(fig)

def tSNEPlot(nmf,tfidf,no_topics, perplexity,Scan=False):
    nmf_embedding = nmf.transform(tfidf)
    nmf_embedding = (nmf_embedding - nmf_embedding.mean(axis=0))/nmf_embedding.std(axis=0)
    tsne = TSNE(random_state=3211,perplexity=perplexity)
    tsne_embedding = tsne.fit_transform(nmf_embedding)
    tsne_embedding = pd.DataFrame(tsne_embedding,columns=['x','y'])
    tsne_embedding['hue'] = nmf_embedding.argmax(axis=1)
    data = tsne_embedding
    scatter=ax.scatter(data=data,x='x',y='y',s=no_topics,c=data['hue'],cmap="tab20")
    handles, labels =scatter.legend_elements(num=no_topics)
    #print(type(labels))
    #labels[0]="test" Use this to create the labels
    #legend1 = ax.legend(handles, labels,loc="upper left", title="Topics",ncol=5)
    #ax.add_artist(legend1)
    if Scan:
        camera.snap()
        #plt.show()
def BuildNTopics(skl_texts,no_features,no_top_words,no_topics):
        print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
        nmf,tfidf_feature_names,tfidf=CreateNMFTopics(skl_texts,no_features,no_topics)
        return nmf,tfidf
def ScanNTopics(skl_texts,TopicScan,perplexity):
    no_top_words=10
    no_features=30000
    for t in TopicScan:
        nmf,tfidf=BuildNTopics(skl_texts,no_features,no_top_words,t)
        tSNEPlot(nmf,tfidf,t,perplexity,True)
    animation = camera.animate(blit=True,interval=1000,repeat_delay=15000)
    return animation
def RunTopicScans(df,SetTrue,SetFalse,stopwords,TopicScan,fname,perplexity):
    SelectedRows=SelectDFRows(df,SetTrue,SetFalse)
    del df
    ListOfTitleWords=SelectedRows['Title Qualifier Words'].tolist()
    nlp = InitNLPPyTextRank();
    nlp.disable_pipes("ner")
    for w in stopwords:nlp.vocab[w].is_stop = True;
    #################  No need to go from .txt back to a text string
    docs = list(nlp.pipe(ListOfTitleWords))#### Matching based on Title and abstract
    skl_texts=[]
    for doc in docs:
            tempskl_texts,texts=FillSciKitText(doc)
            skl_texts.extend(tempskl_texts)

    animation=ScanNTopics(skl_texts,TopicScan,perplexity)
    animation.save(fname, writer = 'imagemagick')
