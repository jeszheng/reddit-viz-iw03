from nltk.sentiment.vader import SentimentIntensityAnalyzer
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json

sid = SentimentIntensityAnalyzer()
natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="9aa73582-d1ff-4cb7-9d92-011e3ee81b05",
  password="Chn7dOdZVaaI",
  version="2017-02-27")

date = '20171103'
subreddits_of_interest = ['news', 'politics', 'worldnews', 'technology']

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
    allCPosts = json.load(data_file)

titles = []

for post in allPosts:
    for subreddit in subreddits_of_interest:
        if post['subreddit'] == subreddit:
            titles.append(post['title'])

num_vader_neutral = 0
num_ibm_neutral = 0

for title in titles:
    ss = sid.polarity_scores(title)
    if ss['compound'] == 0.0:
        print title
        ibm_response = natural_language_understanding.analyze( text = title, features=[ Features.Sentiment()])
        print 'ibm:', ibm_response['sentiment']['document']['score']
        if ibm_response['sentiment']['document']['score'] == 0:
            num_ibm_neutral += 1
        num_vader_neutral += 1

print num_vader_neutral , " on ", date
print num_ibm_neutral , " on ", date




# for post in allCPosts:
#     for subreddit in subreddits_of_interest:
#         if post['subreddit'] == subreddit:
#             titles.append(post['title'])
