
import json

date = '20171021'
subreddits_of_interest = 'politics'

# with open(
# '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
#     allPosts = json.load(data_file)
with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/experimental/Analysis/20171026_top_exp.json') as data_file:
    allPosts = json.load(data_file)

# topPoliticsPostTitles = []
#

topPosts = []
for post in allPosts:
    # if post['subreddit'] == subreddits_of_interest:
    topPosts.append(post)

print "Top"
for post in topPosts:
    print post['permalink']
    print 'Number of Top Comments Collected', len(post['top_comments'])
    print 'Number of Controversial Comments Collected', len(post['controversial_comments'])
    print ''
# print topPoliticsPostTitles

# with open(
# '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
#     allControversialPosts = json.load(data_file)
#
# controversialPoliticsPostTitles = []
#
# for post in allControversialPosts:
#     if post['subreddit'] == 'politics':
#         controversialPoliticsPostTitles.append(post['title'])
#
# print "Controversial"
# print controversialPoliticsPostTitles
