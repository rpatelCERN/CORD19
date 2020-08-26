
# CORD-19: COVID-19 Open Research Dataset

"Today, researchers and leaders from the Allen Institute for AI, Chan Zuckerberg Initiative (CZI), Georgetown University’s Center for Security and Emerging Technology (CSET), Microsoft, and the National Library of Medicine (NLM) at the National Institutes of Health released the COVID-19 Open Research Dataset (CORD-19) of scholarly literature about COVID-19, SARS-CoV-2, and the Coronavirus group.

Requested by The White House Office of Science and Technology Policy, the dataset represents the most extensive machine-readable Coronavirus literature collection available for data and text mining to date, with over 29,000 articles, more than 13,000 of which have full text.

Now, The White House joins these institutions in issuing a call to action to the Nation’s artificial intelligence experts to develop new text and data mining techniques that can help the science community answer high-priority scientific questions related to COVID-19."
- [White House Office of Science and Technology Policy](https://www.whitehouse.gov/briefings-statements/call-action-tech-community-new-machine-readable-covid-19-dataset/)

## Downloading the Data

Several locations:
[Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)
[Semantic Scholar](https://www.semanticscholar.org/cord19/download)

# Overall Goal: 

The CORD dataset is a large chunk of machine readable publications that date from 1870 up until the present (within a few weeks). The dataset consists of a vast number of publications that span a variety of topics including studies on agravated respiratory conditions, international epidemics like Ebola and SARS, and the latest publications on COVID-19. The overall goal is to take this dense web of information and turn it into a comprehensive picture. 

This code attempts to do this by creating a set of topics for a given time slice (for more dense spans of time we also divide them into sub-topics), finding the most similar documents in each topic, and creating extractive summaries for the topic. These are included in the wiki for the repository.



# CORD Crusher Main Executable

CORDCrusher.py is the main executable file that calls the set of functions in the NLP pipeline that create keywords, categorizes documents, and summaries the text. 




```

```


## NLP and Visualization Python Packages
The setup shell file consists of all necessary python packages for running the code.  I will highlight a few key packages that form the backbone of the code as well as useful packages for visualization. 

* [Spacy](https://spacy.io/usage) and also (SciSpacy)[https://allenai.github.io/scispacy/] is used to perform tokenization, recognize parts of speech, pattern and phrase match, and also clean up stop words. 
* [RAKE](https://pypi.org/project/rake-nltk/}) or Rapid Automatic Keyword Extraction algorithm is used as a fairly general and also rapid keyword extraction tool for the first stage of the algorithm (Layer 1 ) to quickly extract keywords from the title and abstract
* [Fuzzy string matching](https://pypi.org/project/fuzzywuzzy/) uses the Levenshtein Distance between sequences of tokens to decide if they are synonms. Some examples include (reading frame and open reading frame, gastroentritis and transmissble gastroentritis virus). My convention is to always keep the longer N-gram (longer sequence of words)
* [NMF](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) or Non-Negative Matrix factorization is an unsupervised learning algorithm similar to Latent Dirichlet Allocation but converges more rapidly using a more advanced minimization technique. In this process, a document-term matrix is constructed with the weights of various terms from a set of documents. This matrix is factored into a term-feature and a feature-document matrix. The features are derived from the contents of the documents, and the feature-document matrix describes data clusters of related documents. A detailed description can be found here: [Fast Local Algorithms for Large Scale Nonnegative Matrix and Tensor Factorizations](https://www.researchgate.net/publication/220241471_Fast_Local_Algorithms_for_Large_Scale_Nonnegative_Matrix_and_Tensor_Factorizations)
* The document features are represented using [Term-Frequency Inverse Document Frequency](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) matrices. The matrix is fit and transformed to create document clusters using NMF. Rare words (with a small document frequency) that are not frequent across all documents are emphasized more with a larger TFIDF score. Cosine similarity between TFIDF vectors is used to create summaries for each topic. [Count Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) is similar but consists only of a matrix of token counts, these vectors are used to create a histogram of word counts
*  [PyTextRank](https://pypi.org/project/pytextrank/) is used for a more advanced but slower recognition of key phrases that contain the topic words. Cutting off the rank score removes more general phrases that would blow up the size of the text summaries.
* [T-distributed Stochastic Neighbor Embedding](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html) is a tool for visualizing the topics by projecting the higher dimensional document space onto a 2D plane.  It converts similarities between data points to joint probabilities and tries to minimize the Kullback-Leibler divergence between the joint probabilities of the low-dimensional embedding and the high-dimensional data. This in effect clusters points that have similarity and pushes away dissimilar clusters. This algorithm is used to visualize topic clusters. A key tunable parameter in the algo is the [perplexity](https://distill.pub/2016/misread-tsne/) and in general it should scale with the number of features.
* [celluloid](https://pypi.org/project/celluloid/) provides gif animations from matlibplot. I use it to step though tSNE plots that scan over different number of topics. This shows visualizes how many topics might be necessary for a given time slice.

```	
bash setup.sh 
```	

