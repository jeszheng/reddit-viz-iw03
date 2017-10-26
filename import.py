from models import TopPost, ControversialPost, db
import json
import sys

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    # """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def main():
    # file name.
    allPosts = []
    date = "20171025"
    # don't forget to comment out database url in models file!

    ################################################################################

    # Insert in top post data from specified date.

    ################################################################################
    with open(
    '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_top.json') as data_file:
        allPosts = json.load(data_file)

    # Only use posts in subs poltics, news, worldnews, technology
    selectPosts = []
    for post in allPosts:
        if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews' or post['subreddit'] == 'technology':
            selectPosts.append(post)


    for post in selectPosts:
        # filter out pinned or stickied posts.
        if post['stickied'] or post['over_18']:
            continue

        day_date = date

        topPost = TopPost(post['id'],
            day_date,
            post['permalink'],
            post['url'],
            html_escape(post['title']),
            html_escape(post['selftext']),
            post['author_link_karma'],
            post['subreddit'],
            post['score'],
            post['upvote_ratio'],
            post['num_comments'],
            post['libertarian'],
            post['green'],
            post['liberal'],
            post['conservative'],
            post['submission_time'])
        db.session.add(topPost)

    db.session.commit()
    print 'committed top posts from', date

    ################################################################################

    # Insert in controversial post data from specified date.

    ################################################################################

    with open(
    '/Users/jessicazheng/Documents/Academics/2017-2018/IW3/reddit-viz-iw03/data_collection/' + date + '_controversial.json') as data_file:
        allPosts = json.load(data_file)

    selectPosts = []
    for post in allPosts:
        if post['subreddit'] == 'politics' or post['subreddit'] == 'news' or post['subreddit'] == 'worldnews' or post['subreddit'] == 'technology':
            selectPosts.append(post)

    # Only use posts in subs poltics, news, worldnews, technology

    for post in selectPosts:
        # filter out pinned or stickied posts.
        if post['stickied'] or post['over_18']:
            continue

        day_date = date

        controversialPost = ControversialPost(
            post['id'],
            day_date,
            post['permalink'],
            post['url'],
            html_escape(post['title']),
            html_escape(post['selftext']),
            post['author_link_karma'],
            post['subreddit'],
            post['score'],
            post['upvote_ratio'],
            post['num_comments'],
            post['libertarian'],
            post['green'],
            post['liberal'],
            post['conservative'],
            post['submission_time'])
        db.session.add(controversialPost)

    db.session.commit()
    print 'committed controversial posts from ', date

if __name__ == '__main__':
    main()
