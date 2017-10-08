
import json

date = '20170926'

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

topPoliticsPostTitles = []

for post in allPosts:
    if post['subreddit'] == 'politics':
        topPoliticsPostTitles.append(post['title'])

print "Top"
print topPoliticsPostTitles

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
    allControversialPosts = json.load(data_file)

controversialPoliticsPostTitles = []

for post in allControversialPosts:
    if post['subreddit'] == 'politics':
        controversialPoliticsPostTitles.append(post['title'])

print "Controversial"
print controversialPoliticsPostTitles
