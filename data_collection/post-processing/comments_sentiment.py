import json
import sys
import time
start_time = time.time()

from nltk.sentiment.vader import SentimentIntensityAnalyzer

import indicoio
from indicoio import political
indicoio.config.api_key = "656f0d163f4f34b477145c7495b42612" #My API key

#indicoio.config.api_key = "598d8af7949f6586681afe593346a87d" #Julie's API key

#indicoio.config.api_key = '2ccb28236e4172929679bf7edf504083' # Oliver's API Key

################################################################################

# COMMENTS SENTIMENTS
# VADER AND POLITICAL SENTIMENT ANALYSIS ON TOP POSTS ONLY

################################################################################

# 10/26/2017 - 11/19/2017.
# or maybe Nov 1.
#date = "20171026"
date = sys.argv[1]

# data source: the top posts file.
with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
    allPosts = json.load(data_file)

################################################################################

# VADER COMMENT SENTIMENT ANALYSIS ON TOP POSTS IN ALL SUBREDDITS

# per date: comments_posneg_sentiment_<date>.json

# post id
# tc_strongly_pos, tc_pos, tc_neu, tc_neg, tc_strongly_neg
# cc_strongly_pos, cc_pos, cc_neu, cc_neg, cc_strongly_neg

################################################################################

sid = SentimentIntensityAnalyzer()
strongly_negative_cutoff = -0.6
negative_cutoff = -0.3
neutral_cutoff = 0.3
positive_cutoff = 0.6

comment_postneg_sentiments = []

for post in allPosts:
    data = {}
    data['id'] = post['id']

    if len(post['top_comments']) != 0:
        #dup_comment_ids = []

        top_comments_body = []
        controversial_comments_body = []

        tc_strongly_negative_set = []
        tc_negative_set = []
        tc_neutral_set = []
        tc_positive_set = []
        tc_strongly_positive_set = []

        cc_strongly_negative_set = []
        cc_negative_set = []
        cc_neutral_set = []
        cc_positive_set = []
        cc_strongly_positive_set = []

        # Gather top comments
        for comment in post['top_comments']:
            top_comments_body.append(comment['body'])

        # Gather controversial comments
        for comment in post['controversial_comments']:
            controversial_comments_body.append(comment['body'])

        # # Store the overlap percentage.
        # print 'dup count', dup_count, post['subreddit']
        # data['overlap'] = float(dup_count)/len(post['top_comments'])

        # Compute sentiments for top_comments_body
        for comment in top_comments_body:
            ss = sid.polarity_scores(comment)
            score = ss['compound']
            if score < strongly_negative_cutoff:
                tc_strongly_negative_set.append(comment)
            elif score < negative_cutoff:
                tc_negative_set.append(comment)
            elif score < neutral_cutoff:
                tc_neutral_set.append(comment)
            elif score < positive_cutoff:
                tc_positive_set.append(comment)
            else:
                tc_strongly_positive_set.append(comment)

        # Compute sentiments for controversial_comments_body
        for comment in controversial_comments_body:
            ss = sid.polarity_scores(comment)
            score = ss['compound']
            if score < strongly_negative_cutoff:
                cc_strongly_negative_set.append(comment)
            elif score < negative_cutoff:
                cc_negative_set.append(comment)
            elif score < neutral_cutoff:
                cc_neutral_set.append(comment)
            elif score < positive_cutoff:
                cc_positive_set.append(comment)
            else:
                cc_strongly_positive_set.append(comment)

        # Store counts.
        data['tc_strongly_neg'] = len(tc_strongly_negative_set)
        data['tc_neg'] = len(tc_negative_set)
        data['tc_neu'] = len(tc_neutral_set)
        data['tc_pos'] = len(tc_positive_set)
        data['tc_strongly_pos'] = len(tc_strongly_positive_set)

        data['cc_strongly_neg'] = len(cc_strongly_negative_set)
        data['cc_neg'] = len(cc_negative_set)
        data['cc_neu'] = len(cc_neutral_set)
        data['cc_pos'] = len(cc_positive_set)
        data['cc_strongly_pos'] = len(cc_strongly_positive_set)
        comment_postneg_sentiments.append(data)
    else:
        print 'Post with zero comments! ', post['subreddit'], ' ', post['title'], ' ', post['permalink']
        data['tc_strongly_neg'] = 0
        data['tc_neg'] = 0
        data['tc_neu'] = 0
        data['tc_pos'] = 0
        data['tc_strongly_pos'] = 0
        data['cc_strongly_neg'] = 0
        data['cc_neg'] = 0
        data['cc_neu'] = 0
        data['cc_pos'] = 0
        data['cc_strongly_pos'] = 0
        comment_postneg_sentiments.append(data)

# Write file.
with open('./jsonfiles/comments_posneg_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(comment_postneg_sentiments, outfile)

print 'finished comment pos/neg sentiment analysis for ', date
print "time elapsed so far:", (time.time() - start_time), " seconds"

################################################################################

# POLITICAL SENTIMENT ANALYSIS ON TOP POSTS IN R/POLITICS ONLY

# Outputs 1 JSON file in the format to preserve the raw data in API calls.
# RAW_comments_political_sentiment_<date>.json
# {post id, top_sentiments = [], controversial_sentiments = []
           # obj: {libertarian, liberal, conservative, liberatarian}}

# Outputs another JSON file in the format
# comments_political_sentiment_<date>.json
# id, tc_libertarian_avg, tc_liberal_avg, tc_conservative_avg,
# cc_libertarian_avg, cc_liberal_avg, cc_conservative_avg

################################################################################

# Obtain only posts in political subreddits

allPoliticalPosts = []

for post in allPosts:
    if post['subreddit'] == 'politics':
        allPoliticalPosts.append(post)

# First make indico calls, write output to json (as backup)

raw_sentiments = []

postCount = 0

for post in allPoliticalPosts:
    data1 = {}
    data1['id'] = post['id']

    top_comments_body = []
    controversial_comments_body = []

    # Gather top comments
    for comment in post['top_comments']:
        top_comments_body.append(comment['body'])

    # Gather controversial comments
    for comment in post['controversial_comments']:
        controversial_comments_body.append(comment['body'])

    print len(controversial_comments_body), ' controversial comments to analyze'

    top_comments_political_sentiments = []
    controversial_comments_political_sentiments = []

    # Indico call, compute sentiments for each post.
    count = 0
    cur_comment_body = None
    try:
        for comment_body in top_comments_body:
            if comment_body is None or comment_body == '' or 'http' in comment_body:
                continue
            cur_comment_body = comment_body
            data = indicoio.political(comment_body)
            top_comments_political_sentiments.append(data)
            count += 1
    except:
        print 'Error occured when calculating sentiment for top comment #', count, ' in post ',  postCount ,'writing output to json file.'
        print cur_comment_body
        with open('./jsonfiles/ERR_RAW_comments_political_sentiment_' + date + '.json', 'w') as outfile:
            json.dump(raw_sentiments, outfile)
        sys.exit()

    count = 0
    try:
        for comment_body in controversial_comments_body:
            if comment_body is None or comment_body == '' or 'http' in comment_body:
                continue
            cur_comment_body = comment_body
            data = indicoio.political(comment_body)
            controversial_comments_political_sentiments.append(data)
            count += 1
    except:
        print 'Error occured when calculating sentiment for controversial comment #', count, ' in post ',  postCount ,'writing output to json file.'
        print cur_comment_body
        with open('./jsonfiles/ERR_RAW_comments_political_sentiment_' + date + '.json', 'w') as outfile:
            json.dump(raw_sentiments, outfile)
        sys.exit()

    # Store raw data indico into dataset 1
    data1['top_sentiments'] = top_comments_political_sentiments
    data1['controversial_sentiments'] = controversial_comments_political_sentiments
    raw_sentiments.append(data1)
    print 'finished calling indico for post ', post['id']
    postCount += 1

with open('./jsonfiles/RAW_comments_political_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(raw_sentiments, outfile)

print 'wrote indico data to RAW_comments_political_sentiment_', date, '.json'
print "time elapsed so far:", (time.time() - start_time), " seconds"
# with open(
# './jsonfiles/RAW_comments_political_sentiment_' + date + '.json') as data_file:
#     raw_sentiments = json.load(data_file)

# Now compute the averaged values

avg_sentiments = [] # averaged.

for post_sentiment in raw_sentiments:
    data2 = {}
    data2['id'] = post_sentiment['id']

    # compute the average sentiment, store into dataset 2.
    tc_libertarian = []
    tc_conservative = []
    tc_liberal = []
    cc_libertarian = []
    cc_conservative = []
    cc_liberal = []

    for comment_sentiment in post_sentiment['top_sentiments']:
        tc_libertarian.append(comment_sentiment['Libertarian'])
        tc_conservative.append(comment_sentiment['Conservative'])
        tc_liberal.append(comment_sentiment['Liberal'])

    data2['tc_libertarian_avg'] = sum(tc_libertarian)/float(len(tc_libertarian))
    data2['tc_conservative_avg'] = sum(tc_conservative)/float(len(tc_conservative))
    data2['tc_liberal_avg'] = sum(tc_liberal)/float(len(tc_liberal))

    if len(post_sentiment['controversial_sentiments']) == 0:
        data2['cc_libertarian_avg'] = float(-1)
        data2['cc_conservative_avg'] = float(-1)
        data2['cc_liberal_avg'] = float(-1)
    else:
        for comment_sentiment in post_sentiment['controversial_sentiments']:
            cc_libertarian.append(comment_sentiment['Libertarian'])
            cc_conservative.append(comment_sentiment['Conservative'])
            cc_liberal.append(comment_sentiment['Liberal'])

        data2['cc_libertarian_avg'] = sum(cc_libertarian)/float(len(cc_libertarian))
        data2['cc_conservative_avg'] = sum(cc_conservative)/float(len(cc_conservative))
        data2['cc_liberal_avg'] = sum(cc_liberal)/float(len(cc_liberal))

    avg_sentiments.append(data2)

# Write output to json.
with open('./jsonfiles/comments_political_sentiment_' + date + '.json', 'w') as outfile:
    json.dump(avg_sentiments, outfile)
print "time elapsed so far:", (time.time() - start_time), " seconds"
print 'finished comment political sentiment analysis for ', date
