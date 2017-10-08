from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import json
import gensim
from gensim import corpora

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

date = '20170925'

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

politicsPostTitles = []

for post in allPosts:
    if post['subreddit'] == 'politics':
        politicsPostTitles.append(post['title'])

titles_clean = [clean(title).split() for title in politicsPostTitles]

# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(titles_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
title_term_matrix = [dictionary.doc2bow(title) for title in titles_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(title_term_matrix, num_topics=5, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=5, num_words=3))
