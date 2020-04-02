import spacy
import pytextrank
from rake_nltk import Rake

def InitNLPPyTextRank():
    nlpPyRank = spacy.load("en_core_web_sm")
    tr = pytextrank.TextRank()
    # add PyTextRank to the spaCy pipeline
    nlpPyRank.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    return nlpPyRank

def InitNLPRake(StopWords):
    nlp=Rake(StopWords);
    return nlp

def TextRank(text,nlp):
 doc = nlp(text)
 return doc._.phrases
 
def KeyPhrases(text,nlp):
    nlp.extract_keywords_from_text(text)
    doc =nlp.get_ranked_phrases();
    return doc
