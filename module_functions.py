from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost
from topicmodel import get_topics
import json
import time

app = Flask(__name__)

# TODO COMMENT OUT BEFORE PUSH

# purple
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cmodmuptjjyklg:e48f9a96060da864807bd5b967ea0447fd5c4814a7583facde3afd9d729726ce@ec2-184-72-248-8.compute-1.amazonaws.com:5432/dbogg3844cnn32'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def unescape(text):
    text = text.replace("&apos;", "'")
    text = text.replace("&quot;", '"')
    text = text.replace("&amp;", '&')
    return text

def calculateTopicModelData(top_titles, controversial_titles, subreddit_of_interest):
    # TODO control magnitude of each sub.
    if subreddit_of_interest == 'politics':
        multiply_factor = 13
    else:
        multiply_factor = 19
    topic_model_data = []

    top_topic_data = get_topics(top_titles, subreddit_of_interest)
    for model in top_topic_data:
        topic_entry = {}
        topic_entry['keyword'] = model['keyword']
        # Special cases: don't add digits or keywords with only one character.
        if topic_entry['keyword'].isdigit():
            continue
        elif len(topic_entry['keyword']) == 1:
            continue

        topic_entry['weight'] = model['weight'] * multiply_factor
        # correct for extreme values
        if topic_entry['weight'] < 0.25:
            topic_entry['weight'] = 0.25
        elif topic_entry['weight'] > 0.55:
            topic_entry['weight'] = 0.55

        topic_entry['category'] = 'top-' + str(model['group'])
        topic_model_data.append(topic_entry)

    controversial_topic_data = get_topics(controversial_titles, subreddit_of_interest)
    for model in controversial_topic_data:
        topic_entry = {}
        topic_entry['keyword'] = model['keyword']
        # Special cases: don't add digits or keywords with only one character.
        if topic_entry['keyword'].isdigit():
            continue
        elif len(topic_entry['keyword']) == 1:
            continue

        topic_entry['weight'] = model['weight'] * multiply_factor
        # correct for extreme values
        if topic_entry['weight'] < 0.25:
            topic_entry['weight'] = 0.25
        elif topic_entry['weight'] > 0.55:
            topic_entry['weight'] = 0.55

        topic_entry['category'] = 'controversial-' + str(model['group'])
        topic_model_data.append(topic_entry)
    return topic_model_data

def dataToBeRendered(subreddit_of_interest, start_date, end_date):
    top = db.session.query(TopPost).filter(TopPost.date >= start_date).filter(TopPost.date <= end_date).filter_by(subreddit = subreddit_of_interest)
    controversial = db.session.query(ControversialPost).filter(ControversialPost.date >= start_date).filter(ControversialPost.date <= end_date).filter_by(subreddit = subreddit_of_interest)

    top_titles = []
    controversial_titles = []
    posneg_data = []

    for post in top:
        top_titles.append(unescape(post.title))
        posneg = {}
        posneg['Positive-Negative Sentiment'] = post.sentiment_compound
        posneg['Post Score'] = post.score
        posneg['Author Karma'] = post.author_link_karma
        posneg['Upvote Ratio'] = post.upvote_ratio
        posneg['Number of Comments'] = post.num_comments
        posneg['Title'] = unescape(post.title)
        posneg['Category'] = 'top'
        posneg_data.append(posneg)

    for post in controversial:
        controversial_titles.append(unescape(post.title))
        posneg = {}
        posneg['Positive-Negative Sentiment'] = post.sentiment_compound
        posneg['Post Score'] = post.score
        posneg['Author Karma'] = post.author_link_karma
        posneg['Upvote Ratio'] = post.upvote_ratio
        posneg['Number of Comments'] = post.num_comments
        posneg['Title'] = unescape(post.title)
        posneg['Category'] = 'controversial'
        posneg_data.append(posneg)

    topic_model_data = calculateTopicModelData(top_titles, controversial_titles, subreddit_of_interest)

    dataset = {}
    dataset['top_titles'] = top_titles
    dataset['controversial_titles'] = controversial_titles
    dataset['topic_model_data'] = topic_model_data
    dataset['start_date'] = start_date
    dataset['end_date'] = end_date
    dataset['subreddit_of_interest'] = subreddit_of_interest
    dataset['posneg_data'] = posneg_data

    return dataset
