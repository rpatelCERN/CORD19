import pandas as pd
import numpy as np
import spacy


#text="In December 2019 a group of patients with pneumonia of unknown cause were confirmed to be infected with a novel coronavirus, known as 2019-nCoV, in Wuhan, Hubei province, China, which had previously not been detected in humans or animals. 1 Epidemiological evidence suggested that most of these patients had visited a local seafood market in Wuhan 2 and that the gene sequence of the virus obtained from these patients was highly similar to that identified in bats. 3 The virus was subsequently renamed SARS-Cov-2 as it is similar to the coronavirus responsible for severe acute respiratory syndrome (SARS-CoV), a member of the subgenus Sarbecovirus (Beta-CoV lineage B), with which it shares more than 79% of its sequence, but it is more distant to the coronavirus responsible for Middle East respiratory syndrome (MERS-CoV), a member of the Merbecovirus subgenus (only 50% homology with SARS-Cov-2). All these viruses are categorised within the same genus of the subfamily Orthocoronavirinae within the family Coronaviridae. [4] [5] [6] [7] Some researchers have found that SARS-Cov-2 has strong affinity to human respiratory receptors, 8 suggesting a potential threat to global public health."
#
#text=nlp(text)
#textlist=list(text.sents);
#pos= {}
#for token in text:
#    pos[token]=token.pos_
#print(pos.keys())

def clean_up_spacy(text,nlp):
    #nlpClean = spacy.load('en')
    removal= ['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE']
    text_out = []
    doc= nlp(text)
    for token in doc:
        if token.is_stop == False and token.is_alpha and len(token)>2 and token.pos_ not in removal:
            text = token.text
            text_out.append(text)
    return " ".join(text_out)
#text_out=clean_up_spacy(text)

#print(text_out)
