from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import time

# -----------------------------------------------------------------------------#
# topicmodel.py - NO LONGER USED
# -----------------------------------------------------------------------------#
# This file was previously used to perform topic model computation via LDA.
# However, I eventually decided to use IBM Watson's Natural Language understanding
# service instead. 
# -----------------------------------------------------------------------------#

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def get_topics(titles, subreddit_of_interest):
    start_time = time.time()

    # vary between subs?
    number_of_topics = 3
    number_of_words = 5

    if subreddit_of_interest == 'politics':
        number_of_passes = 50
    elif subreddit_of_interest == 'news':
        number_of_passes = 25
    elif subreddit_of_interest == 'worldnews':
        number_of_passes = 25
    elif subreddit_of_interest == 'technology':
        number_of_passes = 50

    titles_clean = [clean(title).split() for title in titles]

    # Creating the term dictionary of our corpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(titles_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    title_term_matrix = [dictionary.doc2bow(title) for title in titles_clean]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Training LDA model on the document term matrix.
    ldamodel1 = Lda(title_term_matrix, num_topics=number_of_topics, id2word = dictionary, passes=number_of_passes)
    ldamodel2 = Lda(title_term_matrix, num_topics=number_of_topics, id2word = dictionary, passes=number_of_passes)

    # TODO comment out print statement beefore deploy!
    #print "analysis time: ", (time.time() - start_time), " seconds"

    # Create checker list for  batch modeling
    checker_lda = ldamodel2.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True)
    checker_keyword_list = []
    for topic_tuple in checker_lda:
        topic_and_weights = topic_tuple[1].split(' + ')
        for item in topic_and_weights:
            checker_keyword_list.append(item[7:-1])

    # Return results that are in the intersection of both batches
    result = ldamodel1.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True)

    topic_models = []
    topic_group = 0
    for topic_tuple in result:
        topic_and_weights = topic_tuple[1].split(' + ')
        for item in topic_and_weights:
            keyword = item[7:-1]
            if (keyword not in checker_keyword_list):
                continue
            topic = {}
            topic['keyword'] = keyword
            topic['weight'] = float(item[0:5])
            topic['group'] = topic_group
            topic_models.append(topic)
        topic_group += 1
    return topic_models
