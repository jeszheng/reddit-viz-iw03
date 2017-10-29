import praw
import json
import time
import datetime
from copy import deepcopy

import indicoio
from indicoio import political
indicoio.config.api_key = "656f0d163f4f34b477145c7495b42612"

start_time = time.time()

reddit = praw.Reddit(client_id='_7DprL1dYvgqlw',
                     client_secret='V5ZX3LPGxsrUv-ngEVRtg7I-9ko',
                     user_agent='script.best-of-reddit:v1.0 (by /u/<reddit-best-bot>)')

# subreddits used.
subreddits = [  'politics',
                'technology',
                'worldnews',
                'news' ]

# use the date to mark file name.
timestr = time.strftime("%Y%m%d-%H%M%S")
timestr = timestr[:8]

controvesialFileName = timestr + "_controversial.json"
topFileName = timestr + "_top.json"

################################################################################

# get the top 50 controversial posts within the last 24 hours

################################################################################

print "gathering controversial post data:"

controversialPosts = []

for subreddit in subreddits:
    print "gathering post data and comments from", subreddit
    numposts = 0
    for submission in reddit.subreddit(subreddit).controversial('day', limit = 25):
        post = {}

        # obtain author info
        if submission.author is None:
            print "NOT COLLECTED:", submission.title
            continue
        else:
            # in case of broken author links, which sadly occur a lot :(
            try:
                post["author_link_karma"]= reddit.redditor(submission.author.name).link_karma
            except:
                print "NOT COLLECTED:", submission.title, "by author", submission.author.name
                continue

        # no comment collection for controversial posts
        post["controversial_comments"] = []
        post["top_comments"] = []

        # obtain other attributes
        post["permalink"]= submission.permalink
        post["url"]= submission.url
        post["title"]= submission.title
        post["id"]= submission.id
        post["selftext"]= submission.selftext.replace('\n', '')
        post["subreddit"]= submission.subreddit.display_name
        post["score"]= submission.score
        post["upvote_ratio"]= submission.upvote_ratio
        post["num_comments"]= submission.num_comments
        post["over_18"]= submission.over_18
        post["pinned"]= submission.pinned
        post["contest_mode"]= submission.contest_mode
        post["gilded"]= submission.gilded
        post["stickied"]= submission.stickied
        post["spoiler"]= submission.spoiler
        post["submission_time"]= datetime.datetime.fromtimestamp(submission.created).ctime()

        # sentiment analysis for r/politics, r/news, r/worldnews
        if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews':
            # API call made here
            sentiment = political(post['title'] + post['selftext'])
            post['libertarian'] = sentiment["Libertarian"]
            post['green'] = sentiment["Green"]
            post['liberal'] = sentiment["Liberal"]
            post['conservative'] = sentiment["Conservative"]
        else:
            post['libertarian'] = -1.0
            post['green'] = -1.0
            post['liberal'] = -1.0
            post['conservative'] = -1.0
        controversialPosts.append(post)
        numposts = numposts + 1
    print subreddit, ": ", numposts


print "time elapsed so far:", (time.time() - start_time), " seconds"
print "controversial posts collected:", len(controversialPosts)

with open(controvesialFileName, 'w') as outfile:
    json.dump(controversialPosts, outfile)



################################################################################

# get the top 50 top posts within the last 24 hours

################################################################################

print "gathering top post data:"

topPosts = []

for subreddit in subreddits:
    print "gathering post data and comments from", subreddit
    numposts = 0
    for submission in reddit.subreddit(subreddit).top('day', limit = 25):
        post = {}

        # obtain author info
        if submission.author is None:
            print "NOT COLLECTED:", submission.title
            continue
        else:
            # in case of broken author links, which sadly occur a lot :(
            try:
                post["author_link_karma"]= reddit.redditor(submission.author.name).link_karma
            except:
                print "NOT COLLECTED:", submission.title, "by author", submission.author.name
                continue

        # obtain top and controversial comments. no time sort option available.
        submissionCopy = deepcopy(submission) # since comment_sort can only be called once, make a deep copy.
        submission.comment_sort = 'controversial'
        submissionCopy.comment_sort = 'top'

        if submission.comments is None:
                post["controversial_comments"] = none
                post["top_comments"] = none
        else:
            # remove all MoreComments instances from comment forest
            submission.comments.replace_more(limit=0)
            submissionCopy.comments.replace_more(limit=0)

            dup_comment_ids = []

            post["top_comments"] = []
            count = 0
            for comment in list(submissionCopy.comments):
                if count >= 20:
                    break;
                commentElement = {}
                if comment.author is None or comment.stickied:
                    continue
                else:
                    try:
                        commentElement["author_comment_karma"]= reddit.redditor(comment.author.name).comment_karma
                    except:
                        print "NOT COLLECTED: comment by author", comment.author.name, " in post id = ", submission.id, ", ", submission.title
                        continue
                commentElement["body"] = comment.body.replace('\n', '')
                commentElement["score"] = comment.score
                commentElement["comment_id"] = comment.id
                commentElement["submission_time"] = datetime.datetime.fromtimestamp(comment.created).ctime()
                commentElement["gilded"] = comment.gilded
                commentElement["stickied"] = comment.stickied
                commentElement["ups"] = comment.ups
                post["top_comments"].append(commentElement)
                dup_comment_ids.append(comment.id)
                count += 1

            # harvest only controversial comments that are not part of
            # top comments.
            post["controversial_comments"] = []
            count = 0
            for comment in list(submission.comments):
                if count >= 20:
                    break;
                if comment.id in dup_comment_ids:
                    continue
                commentElement = {}
                if comment.author is None or comment.stickied:
                    continue
                else:
                    try:
                        commentElement["author_comment_karma"]= reddit.redditor(comment.author.name).comment_karma
                    except:
                        print "NOT COLLECTED: comment by author", comment.author.name, " in post id = ", submission.id, ", ", submission.title
                        continue
                commentElement["body"] = comment.body.replace('\n', '')
                commentElement["score"] = comment.score
                commentElement["comment_id"] = comment.id
                commentElement["submission_time"] = datetime.datetime.fromtimestamp(comment.created).ctime()
                commentElement["gilded"] = comment.gilded
                commentElement["stickied"] = comment.stickied
                commentElement["ups"] = comment.ups
                post["controversial_comments"].append(commentElement)
                count += 1

        # obtain other attributes
        post["permalink"]= submission.permalink
        post["url"]= submission.url
        post["title"]= submission.title
        post["id"]= submission.id
        post["selftext"]= submission.selftext.replace('\n', '')
        post["subreddit"]= submission.subreddit.display_name
        post["score"]= submission.score
        post["upvote_ratio"]= submission.upvote_ratio
        post["num_comments"]= submission.num_comments
        post["over_18"]= submission.over_18
        post["pinned"]= submission.pinned
        post["contest_mode"]= submission.contest_mode
        post["gilded"]= submission.gilded
        post["stickied"]= submission.stickied
        post["spoiler"]= submission.spoiler
        post["submission_time"]= datetime.datetime.fromtimestamp(submission.created).ctime()

        # sentiment analysis for r/politics, r/news, r/worldnews
        if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews':
            # API call made here
            sentiment = political(post['title'] + post['selftext'])
            post['libertarian'] = sentiment["Libertarian"]
            post['green'] = sentiment["Green"]
            post['liberal'] = sentiment["Liberal"]
            post['conservative'] = sentiment["Conservative"]
        else:
            post['libertarian'] = -1.0
            post['green'] = -1.0
            post['liberal'] = -1.0
            post['conservative'] = -1.0

        topPosts.append(post)
        numposts = numposts + 1
    print subreddit, ": ", numposts

print "top posts collected:", len(topPosts)

with open(topFileName, 'w') as outfile:
    json.dump(topPosts, outfile)

print "total data collection time: ", (time.time() - start_time), " seconds"
