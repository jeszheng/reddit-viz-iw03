import json

# import indicoio
# from indicoio import political
# indicoio.config.api_key = "656f0d163f4f34b477145c7495b42612"

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/experimental/Analysis/20171026_top_exp.json') as data_file:
    allPosts = json.load(data_file)



politicalPosts = []
for post in allPosts:
    if post['subreddit'] == 'politics':
        politicalPosts.append(post)

post = politicalPosts[0]

top_comments_body = []
controversial_comments_body = []

for comment in post['top_comments']:
    top_comments_body.append(comment['body'])

for comment in post['controversial_comments']:
    controversial_comments_body.append(comment['body'])

# print top_comments_body

# top_comments_political_sentiments = indicoio.political(top_comments_body)
# controversial_comments_political_sentiments = indicoio.political(controversial_comments_body)

# record.
# with open('20171026_topcomment_political_sentiment.json', 'w') as outfile:
#     json.dump(top_comments_political_sentiments, outfile)
#
# with open('20171026_controversialcomment_political_sentiment.json', 'w') as outfile:
#     json.dump(controversial_comments_political_sentiments, outfile)


with open('20171026_topcomment_political_sentiment.json') as data_file:
    top_comments_political_sentiments = json.load(data_file)

with open('20171026_controversialcomment_political_sentiment.json') as data_file:
    controversial_comments_political_sentiments = json.load(data_file)

# compute averages for top comments
libertarian = []
conservative = []
liberal = []

for comment_sentiment in top_comments_political_sentiments:
    libertarian.append(comment_sentiment['Libertarian'])
    conservative.append(comment_sentiment['Conservative'])
    liberal.append(comment_sentiment['Liberal'])

avg_libertarian = sum(libertarian)/float(len(libertarian))
avg_conservative = sum(conservative)/float(len(conservative))
avg_liberal = sum(liberal)/float(len(liberal))

print 'Top Comments:'
print 'average libertarian: ', avg_libertarian
print 'average conservative: ', avg_conservative
print 'average liberal: ', avg_liberal

# compute averages for controversial comments

libertarian = []
conservative = []
liberal = []

for comment_sentiment in controversial_comments_political_sentiments:
    libertarian.append(comment_sentiment['Libertarian'])
    conservative.append(comment_sentiment['Conservative'])
    liberal.append(comment_sentiment['Liberal'])

avg_libertarian = sum(libertarian)/float(len(libertarian))
avg_conservative = sum(conservative)/float(len(conservative))
avg_liberal = sum(liberal)/float(len(liberal))

print 'Controversial Comments:'
print 'average libertarian: ', avg_libertarian
print 'average conservative: ', avg_conservative
print 'average liberal: ', avg_liberal



# alternatively, compute as one giant string. the batch option would result
# in 1,000 calls per day -> waayyyy too expensive.

# append everything in top comments into one string.
top_comment_string = ' '.join(top_comments_body)
controversial_comment_string = ' '.join(controversial_comments_body)

print top_comment_string

# top_comments_string_sent = indicoio.political(top_comment_string)
# controversial_comments_string_sent = indicoio.political(controversial_comment_string)
#
# print top_comments_string_sent
# print controversial_comments_string_sent
#
# with open('str_20171026_topcomment_political_sentiment.json', 'w') as outfile:
#     json.dump(top_comments_string_sent, outfile)
#
# with open('str_20171026_controversialcomment_political_sentiment.json', 'w') as outfile:
#     json.dump(controversial_comments_string_sent, outfile)

# .. maybe we can split it up into __ groups?
# like 5 groups?
# maybe not 20....
