import sys
import json

allPostsOrig = []
allSentimentsOrig = []

date = "20171001-204638"
topOrControversial = "controversial"

# FIX TOP POST

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/cos-iw-reddit/data_collection/jessica_data/pre-sentiment/' + date + '_' + topOrControversial + '.json') as data_file:
    allPostsOrig = json.load(data_file)

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/cos-iw-reddit/data_collection/jessica_data/sentiments/' + date + '_' + topOrControversial + '_sentiment.json') as data_file:
    allSentimentsOrig = json.load(data_file)

postsWithSentiments = []

for orginalPost in allPostsOrig:
    newPost = {}
    newPost["controversial_comments"] = orginalPost["controversial_comments"]
    newPost["top_comments"] = orginalPost["top_comments"]
    newPost["permalink"]= orginalPost["permalink"]
    newPost["url"]= orginalPost["url"]
    newPost["title"]= orginalPost["title"]
    newPost["author_link_karma"]= orginalPost["author_link_karma"]
    newPost["id"]= orginalPost["id"]
    newPost["selftext"]= orginalPost["selftext"]
    newPost["subreddit"]= orginalPost["subreddit"]
    newPost["score"]= orginalPost["score"]
    newPost["upvote_ratio"]= orginalPost["upvote_ratio"]
    newPost["num_comments"]= orginalPost["num_comments"]
    newPost["over_18"]= orginalPost["over_18"]
    newPost["pinned"]= orginalPost["pinned"]
    newPost["contest_mode"]= orginalPost["contest_mode"]
    newPost["gilded"]= orginalPost["gilded"]
    newPost["stickied"]= orginalPost["stickied"]
    newPost["spoiler"]= orginalPost["spoiler"]
    newPost["submission_time"]= orginalPost["submission_time"]
    # default sentiments to -1
    newPost['libertarian'] = -1.0
    newPost['green'] = -1.0
    newPost['liberal'] = -1.0
    newPost['conservative'] = -1.0
    postsWithSentiments.append(newPost)

# now stupid double searching....
politicsSentiments = []
newsSentiments = []
worldNewsSentiments = []

for sentiment in allSentimentsOrig:
    if sentiment['subreddit'] == 'politics':
        politicsSentiments.append(sentiment)
for sentiment in allSentimentsOrig:
    if sentiment['subreddit'] == 'news':
        newsSentiments.append(sentiment)
for sentiment in allSentimentsOrig:
    if sentiment['subreddit'] == 'worldnews':
        worldNewsSentiments.append(sentiment)

numPosts = 0
numMatches = 0

for post in postsWithSentiments:
    if post['subreddit'] == 'politics':
        numPosts += 1
        for sentiment in politicsSentiments:
            if post['title'] == sentiment['title']:
                numMatches += 1
                post['libertarian'] = sentiment["sentiment"]["Libertarian"]
                post['green'] = sentiment["sentiment"]["Green"]
                post['liberal'] = sentiment["sentiment"]["Liberal"]
                post['conservative'] = sentiment["sentiment"]["Conservative"]
                break
    elif post['subreddit'] == 'news':
        numPosts += 1
        for sentiment in newsSentiments:
            if post['title'] == sentiment['title']:
                numMatches += 1
                post['libertarian'] = sentiment["sentiment"]["Libertarian"]
                post['green'] = sentiment["sentiment"]["Green"]
                post['liberal'] = sentiment["sentiment"]["Liberal"]
                post['conservative'] = sentiment["sentiment"]["Conservative"]
                break
    elif post['subreddit'] == 'worldnews':
        numPosts += 1
        for sentiment in worldNewsSentiments:
            if post['title'] == sentiment['title']:
                numMatches += 1
                post['libertarian'] = sentiment["sentiment"]["Libertarian"]
                post['green'] = sentiment["sentiment"]["Green"]
                post['liberal'] = sentiment["sentiment"]["Liberal"]
                post['conservative'] = sentiment["sentiment"]["Conservative"]
                break
print numMatches, '/', numPosts, ' matches found'

outputFileName = date[:8] + "_" + topOrControversial + ".json"
with open(outputFileName, 'w') as outfile:
    json.dump(postsWithSentiments, outfile)
