from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import json
import gensim
from gensim import corpora
import time

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

number_of_topics = 4
number_of_words = 5

# take in sub as a param.
# num passes experiment.
#                           25      time        50      time
# news:                     1       4s       DECIDED: 25.
# politics:                 :/        5s        :/      6s          10 is crap. Decided 50 for now.
#   this sub looks a little harder to stabilize.
# worldnews:                  fine          4s        fine     5s DECIDE 25.
# tecchnology:               :/             5.5s         DECIDED 50
number_of_passes = 25

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

date = '20171002'
subreddit_of_interest = 'politics'
# worldnews takes kind of long?

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

start_time = time.time()

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
ldamodel1 = Lda(title_term_matrix, num_topics=number_of_topics, id2word = dictionary, passes=number_of_passes)
ldamodel2 = Lda(title_term_matrix, num_topics=number_of_topics, id2word = dictionary, passes=number_of_passes)

# num_topics: required.
# id2word: required. The LdaModel class requires our previous dictionary to map ids to strings.
# passes: optional. The number of laps the model will take through corpus. The greater the number of passes, the more accurate the model will be. A lot of passes can be slow on a very large corpus.
# 20 is fine?

# Adjusting the models number of topics and passes is important to getting a good result. Two topics seems like a better fit for our documents
print "total analysis time: ", (time.time() - start_time), " seconds"

# print(ldamodel1.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True))

# get all keywords from a lda.

#print (ldamodel2.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True))
# print ''

checker_lda = ldamodel2.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True)
checker_keyword_list = []
for topic_tuple in checker_lda:
    topic_and_weights = topic_tuple[1].split(' + ')
    for item in topic_and_weights:
        checker_keyword_list.append(item[7:-1])

#print checker_keyword_list

original_model = ldamodel1.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True)

print(ldamodel1.print_topics(num_topics=5, num_words=3))

# topic_models = []
# topic_group = 0
# for topic_tuple in original_model:
#     topic_and_weights = topic_tuple[1].split(' + ')
#     for item in topic_and_weights:
#         keyword = item[7:-1]
#         if (keyword not in checker_keyword_list):
#             # print keyword, " skipped!"
#             continue
#         topic = {}
#         topic['keyword'] = keyword
#         topic['weight'] = float(item[0:5])
#         topic['group'] = topic_group
#         topic_models.append(topic)
#     topic_group += 1
#
# for model in topic_models:
#     print model['keyword'], model['group']

# appears decently consistent.



# clear() Clear model state (free up some memory). Used in the distributed algo.
