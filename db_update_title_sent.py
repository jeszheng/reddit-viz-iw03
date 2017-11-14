from models import TopPost, ControversialPost, db
import json
import sys

date = "20171004"

################################################################################

# Fix top title sentiments

################################################################################

# find post id, update, and commit.
with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/post-processing/jsonfiles/FIX_top_title_sentiment_' + date + '.json') as data_file:
    t_titlePosNegSentiments = json.load(data_file)

for sentiment in t_titlePosNegSentiments:
    specified_post_id = sentiment['id']
    posts = db.session.query(TopPost).filter(TopPost.post_id == specified_post_id)
    for post in posts:
        post.sentiment_compound = sentiment['sentiment_compound']
        db.session.commit()
        break; # there should only really be one.

print 'finished updating top posts for ', date

################################################################################

# Fix controversial title sentiments

################################################################################

# find post id, update, and commit.
with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/post-processing/jsonfiles/FIX_controversial_title_sentiment_' + date + '.json') as data_file:
    c_titlePosNegSentiments = json.load(data_file)

for sentiment in c_titlePosNegSentiments:
    specified_post_id = sentiment['id']
    posts = db.session.query(ControversialPost).filter(ControversialPost.post_id == specified_post_id)
    for post in posts:
        post.sentiment_compound = sentiment['sentiment_compound']
        db.session.commit()
        break; # there should only really be one.

print 'finished updating controversial posts for ', date
