import json
import sys

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

################################################################################

# TOP POST TITLE SENTIMENT

################################################################################

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allTopPosts = json.load(data_file)

top_title_sentiments = []

for post in allTopPosts:
    data = {}
    data['id'] = post['id']
    ss = sid.polarity_scores(post['title'])
    data['sentiment_compound'] = ss['compound']
    top_title_sentiments.append(data)

# Write file.
with open('./jsonfiles/top_title_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(top_title_sentiments, outfile)

################################################################################

# CONTROVERSIAL POST TITLE SENTIMENT

################################################################################

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
    allControversialPosts = json.load(data_file)

controversial_title_sentiments = []

for post in allControversialPosts:
    data = {}
    data['id'] = post['id']
    ss = sid.polarity_scores(post['title'])
    data['sentiment_compound'] = ss['compound']
    controversial_title_sentiments.append(data)

# Write file.
with open('./jsonfiles/controversial_title_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(controversial_title_sentiments, outfile)

print 'finished title pos/neg sentiment analysis for ', date
