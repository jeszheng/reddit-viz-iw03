import json
import sys

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# import indicoio
# from indicoio import political
# indicoio.config.api_key = "598d8af7949f6586681afe593346a87d" #Julie's API key

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
# allPoliticalPosts = []
#
# for post in allPosts:
#     if post['subreddit'] == 'politics':
#         allPoliticalPosts.append(post)
#
# dataset_1 = [] # RAW
# dataset_2 = [] # averaged.
#
# # TODO test with only one date -- tonight.
# for post in allPoliticalPosts:
#     data1 = {}
#     data2 = {}
#     data1['id'] = post['id']
#     data2['id'] = post['id']
#
#     top_comments_body = []
#     controversial_comments_body = []
#
#     # Gather top comments
#     for comment in post['top_comments']:
#         top_comments_body.append(comment['body'])
#
#     # Gather controversial comments
#     for comment in post['controversial_comments']:
#         controversial_comments_body.append(comment['body'])
#
#     # Indico call, compute sentiments for each post.
#     top_comments_political_sentiments = indicoio.political(top_comments_body)
#     controversial_comments_political_sentiments = indicoio.political(controversial_comments_body)
#
#     # Store raw data indico into dataset 1
#     data1['top_sentiments'] = top_comments_political_sentiments
#     data1['controversial_sentiments'] = controversial_comments_political_sentiments
#     dataset_1.append(data1)
#
#     # compute the average sentiment, store into dataset 2.
#     tc_libertarian = []
#     tc_conservative = []
#     tc_liberal = []
#     cc_libertarian = []
#     cc_conservative = []
#     cc_liberal = []
#
#     for comment_sentiment in top_comments_political_sentiments:
#         tc_libertarian.append(comment_sentiment['Libertarian'])
#         tc_conservative.append(comment_sentiment['Conservative'])
#         tc_liberal.append(comment_sentiment['Liberal'])
#
#     for comment_sentiment in controversial_comments_political_sentiments:
#         cc_libertarian.append(comment_sentiment['Libertarian'])
#         cc_conservative.append(comment_sentiment['Conservative'])
#         cc_liberal.append(comment_sentiment['Liberal'])
#
#     data2['tc_libertarian_avg'] = sum(tc_libertarian)/float(len(tc_libertarian))
#     data2['tc_conservative_avg'] = sum(tc_conservative)/float(len(tc_conservative))
#     data2['tc_liberal_avg'] = sum(tc_liberal)/float(len(tc_liberal))
#
#     data2['cc_libertarian_avg'] = sum(cc_libertarian)/float(len(cc_libertarian))
#     data2['cc_conservative_avg'] = sum(cc_conservative)/float(len(cc_conservative))
#     data2['cc_liberal_avg'] = sum(cc_liberal)/float(len(cc_liberal))
#
#     dataset_2.append(data2)
#
# # Write outputs to 2 different files.
#
# with open('./jsonfiles/RAW_comments_political_sentiment_' + date + '.json', 'w') as outfile:
#     json.dump(dataset_1, outfile)
#
# with open('./jsonfiles/comments_political_sentiment_' + date + '.json', 'w') as outfile:
#     json.dump(dataset_2, outfile)
