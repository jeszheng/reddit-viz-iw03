import json
import sys

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features
from nltk.sentiment.vader import SentimentIntensityAnalyzer

################################################################################

# TITLES FROM ALL SUBREDDITS IN BOTH TOP AND CONTROVERSIAL

# per date: 	top_title_sentiment_<date>.json
#               controversial_title_sentiment_<date>.json

# store obj: id, sentiment_compound.
################################################################################

# 10/1/2017 starting.
#date = "20171026"
date = sys.argv[1]
sid = SentimentIntensityAnalyzer()

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="b405c5f4-f7ae-4708-a370-068030a6792c",
  password="p60dllepHDrm",
  version="2017-02-27")

num_ibm_calls = 0

################################################################################

# TOP POST TITLE SENTIMENT

################################################################################

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allTopPosts = json.load(data_file)

select_top_posts = []

for post in allTopPosts:
    if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews' or post['subreddit'] == 'technology':
        select_top_posts.append(post)

top_title_sentiments = []

for post in select_top_posts:
    data = {}
    data['id'] = post['id']
    ss = sid.polarity_scores(post['title'])
    vader_sentiment = ss['compound']
    if vader_sentiment == 0.0:
        try:
            ibm_response = natural_language_understanding.analyze(text = post['title'], features=[Features.Sentiment()])
            ibm_raw_sentiment = ibm_response['sentiment']['document']['score']
            final_sentiment = 0.6 * ibm_raw_sentiment # neturalize a bit
            num_ibm_calls += 1
        except:
            final_sentiment = vader_sentiment
    else:
        final_sentiment = vader_sentiment
    data['sentiment_compound'] = final_sentiment
    top_title_sentiments.append(data)

# Write file.
with open('./jsonfiles/FIX_top_title_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(top_title_sentiments, outfile)

print num_ibm_calls, ' ibm calls so far'
################################################################################

# CONTROVERSIAL POST TITLE SENTIMENT

################################################################################

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
    allControversialPosts = json.load(data_file)

select_controversial_posts = []

for post in allControversialPosts:
    if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews' or post['subreddit'] == 'technology':
        select_controversial_posts.append(post)

controversial_title_sentiments = []

for post in select_controversial_posts:
    data = {}
    data['id'] = post['id']
    ss = sid.polarity_scores(post['title'])
    vader_sentiment = ss['compound']
    if vader_sentiment == 0.0:
        try:
            ibm_response = natural_language_understanding.analyze(text = post['title'], features=[Features.Sentiment()])
            ibm_raw_sentiment = ibm_response['sentiment']['document']['score']
            final_sentiment = 0.65 * ibm_raw_sentiment # neturalize a bit
            num_ibm_calls += 1
        except:
            final_sentiment = vader_sentiment
    else:
        final_sentiment = vader_sentiment
    data['sentiment_compound'] = final_sentiment
    controversial_title_sentiments.append(data)

# Write file.
with open('./jsonfiles/FIX_controversial_title_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(controversial_title_sentiments, outfile)

print num_ibm_calls, ' ibm calls so far'
print 'finished FIXING title pos/neg sentiment analysis for ', date
