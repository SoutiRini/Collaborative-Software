import tom_lib.utils as ut
from tom_lib.nlp.topic_model import LatentDirichletAllocation, NonNegativeMatrixFactorization
from tom_lib.visualization.visualization import Visualization
import nltk
import csv
import os
import sys
import string
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

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

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

paras = [clean(x) for x in paras]

model = NonNegativeMatrixFactorization(paras)
model.infer_topics(num_topics=15) #, algorithm="variational")

viz = Visualization(model)
viz.plot_topic_distribution()
