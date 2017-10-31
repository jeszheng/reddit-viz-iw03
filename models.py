from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

# TODO COMMENT OUT LINE BELOW BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/devel_db'

# purple
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cmodmuptjjyklg:e48f9a96060da864807bd5b967ea0447fd5c4814a7583facde3afd9d729726ce@ec2-184-72-248-8.compute-1.amazonaws.com:5432/dbogg3844cnn32'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TopPost(db.Model):
    __tablename__ = "topPosts"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String())
    date = db.Column(db.Integer)
    permalink = db.Column(db.String())
    url = db.Column(db.String())
    title = db.Column(db.String())
    selftext = db.Column(db.String())
    author_link_karma = db.Column(db.Integer)
    subreddit = db.Column(db.String())
    score = db.Column(db.Integer)
    upvote_ratio = db.Column(db.Float)
    num_comments = db.Column(db.Integer)
    libertarian = db.Column(db.Float)
    green = db.Column(db.Float)
    liberal = db.Column(db.Float)
    conservative = db.Column(db.Float)
    sentiment_compound = db.Column(db.Float)
    tc_strongly_pos = db.Column(db.Integer)
    tc_pos = db.Column(db.Integer)
    tc_neu = db.Column(db.Integer)
    tc_neg = db.Column(db.Integer)
    tc_strongly_neg = db.Column(db.Integer)
    cc_strongly_pos = db.Column(db.Integer)
    cc_pos = db.Column(db.Integer)
    cc_neu = db.Column(db.Integer)
    cc_neg = db.Column(db.Integer)
    cc_strongly_neg = db.Column(db.Integer)
    tc_libertarian_avg = db.Column(db.Float)
    tc_conservative_avg = db.Column(db.Float)
    tc_liberal_avg = db.Column(db.Float)
    cc_libertarian_avg = db.Column(db.Float)
    cc_conservative_avg = db.Column(db.Float)
    cc_liberal_avg = db.Column(db.Float)

    def __init__(self, post_id, date, permalink, url, title, selftext, author_link_karma, subreddit, score, upvote_ratio, num_comments, libertarian, green, liberal, conservative, sentiment_compound, tc_strongly_pos, tc_pos, tc_neu, tc_neg, tc_strongly_neg, cc_strongly_pos, cc_pos, cc_neu, cc_neg, cc_strongly_neg, tc_libertarian_avg, tc_conservative_avg, tc_liberal_avg, cc_libertarian_avg, cc_conservative_avg, cc_liberal_avg):
        self.post_id = post_id
        self.date = date
        self.permalink = permalink
        self.url = url
        self.title = title
        self.selftext = selftext
        self.author_link_karma = author_link_karma
        self.subreddit = subreddit
        self.score = score
        self.upvote_ratio = upvote_ratio
        self.num_comments = num_comments
        self.libertarian = libertarian
        self.green = green
        self.liberal = liberal
        self.conservative = conservative
        self.sentiment_compound = sentiment_compound
        self.tc_strongly_pos = tc_strongly_pos
        self.tc_pos = tc_pos
        self.tc_neu = tc_neu
        self.tc_neg = tc_neg
        self.tc_strongly_neg = tc_strongly_neg
        self.cc_strongly_pos = cc_strongly_pos
        self.cc_pos = cc_pos
        self.cc_neu = cc_neu
        self.cc_neg = cc_neg
        self.cc_strongly_neg = cc_strongly_neg
        self.tc_libertarian_avg = tc_libertarian_avg
        self.tc_conservative_avg = tc_conservative_avg
        self.tc_liberal_avg = tc_liberal_avg
        self.cc_libertarian_avg = cc_libertarian_avg
        self.cc_conservative_avg = cc_conservative_avg
        self.cc_liberal_avg = cc_liberal_avg

    def __repr__(self):
        return '<p>%r</p>' % (self.post_id)


class ControversialPost(db.Model):
    __tablename__ = "controversialPosts"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String())
    date = db.Column(db.Integer)
    permalink = db.Column(db.String())
    url = db.Column(db.String())
    title = db.Column(db.String())
    selftext = db.Column(db.String())
    author_link_karma = db.Column(db.Integer)
    subreddit = db.Column(db.String())
    score = db.Column(db.Integer)
    upvote_ratio = db.Column(db.Float)
    num_comments = db.Column(db.Integer)
    libertarian = db.Column(db.Float)
    green = db.Column(db.Float)
    liberal = db.Column(db.Float)
    conservative = db.Column(db.Float)
    sentiment_compound = db.Column(db.Float)

    def __init__(self, post_id, date, permalink, url, title, selftext, author_link_karma, subreddit, score, upvote_ratio, num_comments, libertarian, green, liberal, conservative, sentiment_compound):
        self.post_id = post_id
        self.date = date
        self.permalink = permalink
        self.url = url
        self.title = title
        self.selftext = selftext
        self.author_link_karma = author_link_karma
        self.subreddit = subreddit
        self.score = score
        self.upvote_ratio = upvote_ratio
        self.num_comments = num_comments
        self.libertarian = libertarian
        self.green = green
        self.liberal = liberal
        self.conservative = conservative
        self.sentiment_compound = sentiment_compound

    def __repr__(self):
        return '<p>%r</p>' % (self.post_id)
