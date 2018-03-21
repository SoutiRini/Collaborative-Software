import nltk
import os
import csv
import sys
nltk.data.path.append('./libs/nltk_data/')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import numpy
nltk.download('stopwords')
SOME_FIXED_SEED = 42

import gensim
from gensim import corpora

csv.field_size_limit(sys.maxsize)

comments = []

with open(os.path.expanduser("~/Downloads/activemq-artemis.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        comments.append(row['IssueBodies'])
        comments.append(row['Comments'])


split = [comment.split("\n") for comment in comments]
paras = [x for sublist in split for x in sublist]

# excluding stopwords
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)

# calling lemmatizer
lemma = WordNetLemmatizer()

# cleaning document and normalizing
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in paras]

# Preparing Document-Term Matrix

# Creating the term dictionary of our courpus, where every unique term is assigned an index. \
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Running LDA Model

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.


#### RESULTS
for i in range(10):
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word=dictionary, passes=3000)
    print(ldamodel.print_topics(num_topics=3, num_words=3))
