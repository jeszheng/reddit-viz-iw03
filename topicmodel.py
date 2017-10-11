from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
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

def get_topics(titles):

    number_of_topics = 4
    number_of_words = 4
    number_of_passes = 25

    titles_clean = [clean(title).split() for title in titles]

    # Creating the term dictionary of our corpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(titles_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    title_term_matrix = [dictionary.doc2bow(title) for title in titles_clean]

    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel

    # Running and Training LDA model on the document term matrix.
    ldamodel = Lda(title_term_matrix, num_topics=number_of_topics, id2word = dictionary, passes=number_of_passes)

    result = ldamodel.show_topics(num_topics=number_of_topics, num_words=number_of_words, log=False, formatted=True)
    return result
