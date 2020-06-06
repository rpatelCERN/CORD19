from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import pandas as pd
from textblob import TextBlob
import sys
from nltk.corpus import stopwords

Englishstop=set(stopwords.words('english'))

def textblob_tokenizer(str_input):
    blob = TextBlob(str_input.lower())
    tokens = blob.words
    words = [token.stem() for token in tokens]
    return words
#f=open("wordbag.txt",'r')
#WordBody=f.readline()
df=pd.read_csv('ProcessedCSV/SearchWithKeyWords.csv', low_memory=False)
Custom={'preprint','copyright','medrxiv','author','peer','holder','covid','ncov','cov','coronavirus','novel','19'}
Englishstop=Englishstop.union(Custom)
Englishstop=list(Englishstop)
data = df['Candidate Category']

tf_idf_vectorizor = TfidfVectorizer(stop_words = Englishstop,#tokenizer = textblob_tokenizer,
max_features = 200000)

#tf_idf_vectorizor = TfidfVectorizer(stop_words = 'english',#tokenizer = textblob_tokenizer,
#max_features = 200000)

tf_idf = tf_idf_vectorizor.fit_transform(data)

print(tf_idf_vectorizor.get_feature_names())
print(tf_idf.shape)
tf_idf_norm = normalize(tf_idf)
tf_idf_array = tf_idf_norm.toarray()

Features=pd.DataFrame(tf_idf_array, columns=tf_idf_vectorizor.get_feature_names()).head()
print(Features)
number_of_clusters=int(sys.argv[1])
km = KMeans(n_clusters=number_of_clusters)

km.fit(tf_idf)
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = tf_idf_vectorizor.get_feature_names()
for i in range(number_of_clusters):
    top_ten_words = [terms[ind] for ind in order_centroids[i, :5]]
    print("Cluster {}: {}".format(i, ' '.join(top_ten_words)))
#print(Features)
#sklearn_pca = PCA(n_components = 2)
