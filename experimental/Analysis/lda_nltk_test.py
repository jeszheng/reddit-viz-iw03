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

date = '20171008'
subreddit_of_interest = 'news'

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

politicsPostTitles = []

for post in allPosts:
    if post['subreddit'] == subreddit_of_interest:
        #politicsPostTitles.append(post['title'])
        #title = html_escape(post['title']) # ohhhh nvm um not much point in the experimental, as no html chars in first place!!
        politicsPostTitles.append(post['title'])

titles_clean = [clean(title).split() for title in politicsPostTitles]

# Creating the term dictionary of our courpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(titles_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
title_term_matrix = [dictionary.doc2bow(title) for title in titles_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Training LDA model on the document term matrix.
ldamodel = Lda(title_term_matrix, num_topics=6, id2word = dictionary, passes=20)

# num_topics: required.
# id2word: required. The LdaModel class requires our previous dictionary to map ids to strings.
# passes: optional. The number of laps the model will take through corpus. The greater the number of passes, the more accurate the model will be. A lot of passes can be slow on a very large corpus.
# 20 is fine?

# Adjusting the models number of topics and passes is important to getting a good result. Two topics seems like a better fit for our documents

print(ldamodel.show_topics(num_topics=6, num_words=4, log=False, formatted=True))
# clear() Clear model state (free up some memory). Used in the distributed algo.
