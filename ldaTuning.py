import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

print('Reading data')
# Import Dataset
df = pd.read_json('https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json')
#print(df.target_names.unique())
#df.head()

# Convert to list
data = df.content.values.tolist()

print('Cleaning')
# Remove Emails
data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]

# Remove new line characters
data = [re.sub('\s+', ' ', sent) for sent in data]

# Remove distracting single quotes
data = [re.sub("\'", "", sent) for sent in data]

print('Preprocessing')
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

data_words = list(sent_to_words(data))

print('Building bigram and trigram models')
# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

print("Removing stopwords")
# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)

# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# python3 -m spacy download en
nlp = spacy.load('en', disable=['parser', 'ner'])

print('Lemmatizing')
# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

print('Creating dictionary')
# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

# Hyperoptimization
from hyperopt import hp
from hyperopt import fmin, tpe, Trials

space = {}

#space['corpus'] = corpus
#space['id2word'] = id2word
#space['update_every'] = 1
#space['per_word_topics'] = True
#space['random_state'] = 100
#space['passes'] = 30
#space['chunksize'] = 200

space['alpha'] = hp.uniform('alpha', 0, 1)
space['eta'] = hp.uniform('eta', 0, 1)
space['num_topics'] = 3 + hp.randint('num_topics', 97)

trials = Trials()

def objective(params):
    pprint(params)
    model = gensim.models.ldamodel.LdaModel(corpus = corpus,
                                            id2word = id2word,
                                            update_every = 1,
                                            per_word_topics = True,
                                            random_state = 100,
                                            **params)
    coherence_model = CoherenceModel(model=model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    coherence = coherence_model.get_coherence()
    print(coherence)
    return 1-coherence # I want to maximize coherence, so I need minize this expression

print('Beginning optimizations')
best = fmin(objective,
            space,
            algo=tpe.suggest,
            max_evals=10,
            trials=trials)

#lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
#                                           id2word=id2word,
#                                           num_topics=20,
#                                           random_state=100,
#                                           update_every=1,
#                                           chunksize=100,
#                                           passes=10,
#                                           alpha='auto',
#                                           per_word_topics=True)

from hyperopt import space_eval

best_params = space_eval(space, best)
print("Found optimum")
pprint(best_params)

lda_model = gensim.models.ldamodel.LdaModel(**best_params)

# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

import pickle

with open('trials.pickle', 'wb') as f:
    pickle.dump(trials, f)

with open('best_config.pickle', 'wb') as f:
    pickle.dump(best, f)
