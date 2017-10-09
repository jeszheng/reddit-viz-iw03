from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import json

date = '20171008'
subreddit_of_interest = 'news'

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

titles = []

for post in allPosts:
    if post['subreddit'] == subreddit_of_interest:
        #politicsPostTitles.append(post['title'])
        #title = html_escape(post['title']) # ohhhh nvm um not much point in the experimental, as no html chars in first place!!
        titles.append(post['title'])


tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
# en_stop = get_stop_words('en')
stop = set(stopwords.words('english'))

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# compile sample documents into a list
doc_set = titles

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)

# print results
print(ldamodel.show_topics(num_topics=5, num_words=4, log=False, formatted=True))


# slightly better accuracy, but displays stem words.
