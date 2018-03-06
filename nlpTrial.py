import nltk
from nltk import word_tokenize
from nltk import pos_tag
from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""

# tokens = nltk.word_tokenize(sentence)

# print("tokens:")
# print(tokens)

# words = [w.lower() for w in tokens]

tokens = word_tokenize(sentence)

tagged = nltk.pos_tag(tokens)


# only_pos = list(zip(*tokens_pos))[1]

print(tagged)

# converting pos tags from treebank to wordnet


words = [w.lower() for w in tokens]

print("words:")
print(words)


def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

stemmed_words = [stemmer.stem(word) for word in words]

print("stemmed words")
print(stemmed_words)

lemmatized_no_context = [lemmatiser.lemmatize(word) for word in words]

print("lemmatized_no_context")
print(lemmatized_no_context)

lemmatized_context =[]

for word, tag in tagged:
    wntag = get_wordnet_pos(tag)
    if wntag is None:# not supply tag in case of None
        lemma = lemmatiser.lemmatize(word)
    else:
        lemma = lemmatiser.lemmatize(word, pos=wntag)

    lemmatized_context.append(lemma)

print("lemmatized_context")
print(lemmatized_context)


# vocab = sorted(set(words))
#
# print("vocab:")
# print(vocab)

# snowball_stemmer = SnowballStemmer("english")
#
# stemmed_words_snowball =  [snowball_stemmer.stem(word) for word in words]
#
# print("stemmed_words_snowball:")
# print(stemmed_words_snowball)
#
# lancaster_stemmer = LancasterStemmer()
#
# stemmed_words_lancaster =  [lancaster_stemmer.stem(word) for word in words]
#
# print("stemmed_words_lancaster:")
# print(stemmed_words_lancaster)
#
# porter_stemmer = PorterStemmer()
#
# stemmed_words_porter =  [porter_stemmer.stem(word) for word in words]
#
# print("stemmed_words_porter:")
# print(stemmed_words_porter)

 # for easy if-statement