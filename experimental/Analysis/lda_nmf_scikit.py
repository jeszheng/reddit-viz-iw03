from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import json
#
# #
# # html_escape_table = {
# #     "&amp;" : "&",
# #     "&quot;" : '"',
# #     "&apos;" : "'",
# #     "&gt;" : ">",
# #     "&lt;" : "<",
# #     }
# #
# # def html_escape(text):
# #     # """Produce entities within text."""
# #     return "".join(html_escape_table.get(c,c) for c in text)
#
# #
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
# #
# # def clean(doc):
# #     stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
# #     punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
# #     normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
# #     return normalized
# #
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        #print "Topic %d:" % (topic_idx)
        print "Topic %d:" % (topic_idx), " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])
#
#
date = '20171002'
subreddit_of_interest = 'politics'

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

politicsPostTitles = []

for post in allPosts:
    if post['subreddit'] == subreddit_of_interest:
        #politicsPostTitles.append(post['title'])
        politicsPostTitles.append(post['title'])

# titles_clean = [clean(title).split() for title in politicsPostTitles]
#
#
# date = '20171008'
# subreddit_of_interest = 'news'
#
# with open(
# '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
#     allPosts = json.load(data_file)
#
# politicsPostTitles = []
#
# for post in allPosts:
#     if post['subreddit'] == subreddit_of_interest:
#         #politicsPostTitles.append(post['title'])
#         politicsPostTitles.append(post['title'])
#
# # do i need t split them? NO
# #dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
documents = politicsPostTitles
# # for i in range(5):
# #     print i
# #     print documents[i]
# #     print '---divider---'
#
no_features = 500 #1000
#
# NMF is able to use tf-idf
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
# tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
# tf = tf_vectorizer.fit_transform(documents)
# tf_feature_names = tf_vectorizer.get_feature_names()
#
no_topics = 5

# Run NMF
nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

# # Run LDA
# lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='batch', learning_offset=50.,random_state=0).fit(tf)
#
no_top_words = 4
print 'NMF'
display_topics(nmf, tfidf_feature_names, no_top_words)
#
# print 'LDA'
# display_topics(lda, tf_feature_names, no_top_words)
