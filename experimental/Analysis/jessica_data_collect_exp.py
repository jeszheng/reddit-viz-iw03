import praw
import json
import time
import datetime
from copy import deepcopy

# import indicoio
# from indicoio import political
# indicoio.config.api_key = "656f0d163f4f34b477145c7495b42612"

start_time = time.time()

reddit = praw.Reddit(client_id='_7DprL1dYvgqlw',
                     client_secret='V5ZX3LPGxsrUv-ngEVRtg7I-9ko',
                     user_agent='script.best-of-reddit:v1.0 (by /u/<reddit-best-bot>)')

# subreddits used.
subreddits = [
                'politics',
                # 'technology',
                # 'worldnews',
                #  'news'
                ]

# use the date to mark file name.
timestr = time.strftime("%Y%m%d-%H%M%S")
timestr = timestr[:8]

controvesialFileName = '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/experimental/Analysis/' + timestr + "_controversial_exp.json"
topFileName = '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/experimental/Analysis/' + timestr + "_top_exp.json"


################################################################################

# get the top 50 top posts within the last 24 hours

################################################################################

print "gathering top post data:"

topPosts = []

for subreddit in subreddits:
    print "gathering post data and comments from", subreddit
    numposts = 0
    for submission in reddit.subreddit(subreddit).top('day', limit = 1):
        post = {}
        print submission.permalink

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
        # submission.comment_limit = 25
        submissionCopy.comment_sort = 'top'
        #submissionCopy.comment_limit = 25

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
            for comment in submissionCopy.comments.list():
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
                # commentElement["score"] = comment.score
                commentElement["comment_id"] = comment.id
                # commentElement["submission_time"] = datetime.datetime.fromtimestamp(comment.created).ctime()
                # commentElement["gilded"] = comment.gilded
                # commentElement["stickied"] = comment.stickied
                # commentElement["ups"] = comment.ups
                post["top_comments"].append(commentElement)
                dup_comment_ids.append(comment.id)
                print comment.body.replace('\n', '')
                print ''
                count += 1

            post["controversial_comments"] = []
            count = 0
            dupCount_id = 0
            dupCount_orig = 0
            dupCount_karma = 0
            dup_body = []
            for comment in submission.comments.list():
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
                # commentElement["score"] = comment.score
                commentElement["comment_id"] = comment.id
                # commentElement["submission_time"] = datetime.datetime.fromtimestamp(comment.created).ctime()
                # commentElement["gilded"] = comment.gilded
                # commentElement["stickied"] = comment.stickied
                # commentElement["ups"] = comment.ups
                    # don't scrape if already in top.
                    # dup_body.append(comment.body)
                    # dupCount_id += 1
                post["controversial_comments"].append(commentElement)
                count += 1

        print 'top comments:', len(post['top_comments'])
        #print post['top_comments']
        print 'controversial comments:', len(post['controversial_comments'])
        for comment in post['controversial_comments']:
            if comment['comment_id'] in dup_comment_ids:
                print 'dup! should not occur.'
        # print 'Top Comments:'
        # for comment in post["top_comments"]:
        #     print comment['body']
        # print ''
        # print 'Controversial Comments:'
        # for comment in post["controversial_comments"]:
        #     print comment['body']
        # print 'dup count id: ', dupCount_id
        #print 'dup count orig: ', dupCount_orig
        #print 'dup count karma: ', dupCount_karma
        #print dup_body
        #print post['controversial_comments']

        topPosts.append(post)
        numposts = numposts + 1

    print subreddit, ": ", numposts

print "top posts collected:", len(topPosts)

# TODO print.
# with open(topFileName, 'w') as outfile:
#     json.dump(topPosts, outfile)

print "total data collection time: ", (time.time() - start_time), " seconds"
