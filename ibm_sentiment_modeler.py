import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features
from nltk.sentiment.vader import SentimentIntensityAnalyzer

date = '20171021'
subreddits_of_interest = 'politics'

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

titles = []

for post in allPosts:
    if post['subreddit'] == subreddits_of_interest:
        titles.append(post['title'])

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="9aa73582-d1ff-4cb7-9d92-011e3ee81b05",
  password="Chn7dOdZVaaI",
  version="2017-02-27")

sid = SentimentIntensityAnalyzer()

for title in titles:
    print title
    print 'Vader:'
    ss = sid.polarity_scores(title)
    print ss['compound']
    print 'IBM:'
    response = natural_language_understanding.analyze( text = title, features=[ Features.Sentiment()])
    print response['sentiment']['document']['score']
    print ''
