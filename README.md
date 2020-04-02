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
No ML-algos are used thus far because I am still getting my feet wet, but the code in this repository should help other novices like myself use simple NLP libraries to query the dataset. 

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

## Wishlist
Outputs are currently CSV files, but ideally there would be some front end interface for researchers to use as well as a simple "fact sheet" for the general public. 

For a fast-query tool, the above could be reworked to be an RDS. 

Find key words with an ML approach instead of brute force so that it is both robust and fast.  
