import spacy
import scispacy
import en_core_sci_sm
import pytextrank
from rake_nltk import Rake,Metric

def InitNLPPyTextRank():
    nlpPyRank = spacy.load("en_core_web_sm")
    tr = pytextrank.TextRank()
    # add PyTextRank to the spaCy pipeline
    nlpPyRank.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    return nlpPyRank
def InitSciSpacy():
    nlp = en_core_sci_sm.load()
    return nlp;


def InitNLPRake():
    nlp=Rake(ranking_metric=Metric.DEGREE_TO_FREQUENCY_RATIO,max_length=6)
    #nlp=Rake(StopWords);
    return nlp

def TextRankPIPE(texts,nlp):
 docs = nlp.pipe(texts)
 rankedphrases=[]
 for doc in docs:rankedphrases.extend(doc._.phrases)
 return rankedphrases

def TextRank(text,nlp):
 doc = nlp(text)
 return doc._.phrases

def KeyPhrases(doc,nlp):
    nlp.extract_keywords_from_text(doc.text)
    doc =nlp.get_ranked_phrases();
    return doc

def KeySciPhrases(text,nlp):
    doc = nlp(text)
    #doc =nlp.get_ranked_phrases();
    return doc.ents

def StopWordslist(StopWordsToAdd):
    spacy_nlp = spacy.load('en_core_web_sm')
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
    fstop=open(StopWordsToAdd)
    StopList=[]
    for line in fstop:
        StopList.append(line.rstrip('\n'));
    fstop.close();
    spacy_stopwords=spacy_stopwords.union(set(StopList));
    return spacy_stopwords;
