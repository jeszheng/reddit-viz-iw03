from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)

# TODO COMMENT OUT LINE BELOW BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pdljaindlmyhbe:008fbca0484298c84029cbb521369c31b2bf7387a854310f44853c9b00e5d98a@ec2-54-204-41-80.compute-1.amazonaws.com:5432/dfnh4bhma6efun'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<h1>%r</h1>' % self.title

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
    submission_time = db.Column(db.String())

    def __init__(self, post_id, date, permalink, url, title, selftext, author_link_karma, subreddit, score, upvote_ratio, num_comments, libertarian, green, liberal, conservative, submission_time):
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
        self.submission_time = submission_time

    def __repr__(self):
        return '<p>%r</p>' % (self.post_id)

class ControversialPost(db.Model):
    __tablename__ = "controversialPost"
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
    submission_time = db.Column(db.String())

    def __init__(self, post_id, date, permalink, url, title, selftext, author_link_karma, subreddit, score, upvote_ratio, num_comments, libertarian, green, liberal, conservative, submission_time):
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
        self.submission_time = submission_time

    def __repr__(self):
        return '<p>%r</p>' % (self.post_id)
