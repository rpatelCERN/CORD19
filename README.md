# CORD19
CORD-19 Open dataset text mining project:

# CORD-19: COVID-19 Open Research Dataset

## Where's the data?

Several locations, I first found it on Kaggle:

https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge

This also has more links to check for updates to the dataset from https://pages.semanticscholar.org/coronavirus-research

## Overall Goal: 

"We are issuing a call to action to the world's artificial intelligence experts to develop text and data mining tools that can help the medical community develop answers to high priority scientific questions. "

The Kaggle excerise itself has 10 main tasks which can be used to map the CORD-19 data onto topics by carefully classifying and scoring key sentences in the publications. The large dataset can then be crushed into an RSS feed on a summary webpage. The whole process should be fast and robust so that new papers can be input to the stream and relevant new information is dessiminated. 

## Additional Goodies from Text Mining

Hopefully, the same tools can be used to extract features which can be fed into ML diagnostic algorithms like cv19 vulnerability index: 
https://science-responds.org/projects/ds#cv19_index

## My First Try

The current version of the repository has a more brute force method (counting, tagging and ranking phrases) of mining the data only because this is my first project with any NLP. Also I am biased by many HEP cut and count publications.
No ML-algos are used thus far because I am still getting my feet wet, but the code in this repository should help other novices like myself use simple NLP libraries to query the dataset. I also include a simple KMeans fit algo to check how the body text lines that match keywords can be mapped onto topics.

For ranking phrases I rely on two main NLP tools: PyTextRank and rake-nltk. 
Additional information on these can be found here: 

https://github.com/DerwenAI/pytextrank

https://github.com/csurfer/rake-nltk

rake is a bit more intuitively understood as a matrix of words/phrases where the diagonal is the frequency and the covariance terms give a measure of how often the word is paired with other words in the covariance matrix. PyTextRank is more commonly used and builds an assocation map using graphs (lemma graphs). 

## Getting started

if you don't have these:
```	
	pip install -U spacy
# Download best-matching version of specific model for your spaCy installation
	python -m spacy download en_core_web_sm
	pip install pytextrank
	pip install rake-nltk
```
Also be sure to grab the latest CORD-19 data from the project areas listed above. The executable scripts should run smoothly in python 3 :

This script takes the metadata.csv file with the title and abstract and uses it to find key phrases in the title, abstract and matches between them. The script also flags which papers are likely about the cov19 epidemic (as opposed to SARS 2003 or MERS from 2012) based on a list of synonyms. You can also pass it a filtered CSV file in the same format if you have made one.
```
	python TitlePhraseRanking.py PATH_TO_YOUR CSV file
```
This script now contains found phrases in the abstract, title or both. In addition, we can get key words by merging all the abstracts flagged as covid19 in the previous step and rank the phrases in them using pyTextRank (this might take some time to run):

```
	python AbstractFullTextAnalyze.py
```
The output is a wordbag.txt file that is then used to rank phrases based on the "super" abstract, and also a csv file with the phrase, rank, and frequency. These quantities can also be plotted from this script.

The total list of phrases is used to search the papers flagged as cov19 in the first step

```
 	python SearchPapers.py PATH TO CORD 19 data
```
This produces a CSV file of keywords and lines that match those keywords, as well as a wordbag.txt file of all matched lines. Based on the matched lines we can try to build topics for the publications we have used. One way to do this is a KMeans algorithm (maybe not the best way?) and look at 2D projections of the principle features using a PCA (This is still in development) What is tuneable in this script is the number of clusters/topics fit in the algo. 

```
	python KMeansLearnTopics.py NCLUSTERS
```

## Wishlist
Simple Wrapper code that uses the KMean clusters in the first step to start to make a loop from topics back to keywords

Outputs are currently CSV files, but ideally there would be some front end interface for researchers to use as well as a simple "fact sheet" for the general public. So building more of a front-end

For a fast-query tool, the above could be reworked to be an RDS. 

Find key words with an ML approach instead of brute force so that it is both robust and fast.  

