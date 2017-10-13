from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost
from topicmodel import get_topics
import json

app = Flask(__name__)

# TODO COMMENT OUT BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/devel_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)

# A global variable.
subreddit_of_interest = 'politics'

def unescape(text):
    text = text.replace("&apos;", "'")
    text = text.replace("&quot;", '"')
    text = text.replace("&amp;", '&')
    return text

def calculateTopicModelData(top_titles, controversial_titles):
    # politics items tend to have a large magnitude.
    if subreddit_of_interest == 'politics':
        multiply_factor = 13
    else:
        multiply_factor = 17
    topic_model_data = []

    top_topic_data = get_topics(top_titles)
    topicNumber = 0
    for topic_tuple in top_topic_data:
        topic_and_weights = topic_tuple[1].split(' + ')
        for item in topic_and_weights:
            topic_entry = {}
            topic_entry['weight'] = float(item[0:5]) * multiply_factor
            # correct for extreme values
            if topic_entry['weight'] < 0.25:
                topic_entry['weight'] = 0.25
            elif topic_entry['weight'] > 0.55:
                topic_entry['weight'] = 0.55
            topic_entry['keyword'] = item[7:-1]
            topic_entry['category'] = 'top-' + str(topicNumber)
            topic_model_data.append(topic_entry)
        topicNumber += 1

    controversial_topic_data = get_topics(controversial_titles)
    topicNumber = 0
    for topic_tuple in controversial_topic_data:
        topic_and_weights = topic_tuple[1].split(' + ')
        for item in topic_and_weights:
            topic_entry = {}
            topic_entry['weight'] = float(item[0:5]) * multiply_factor
            # correct for extreme values
            if topic_entry['weight'] < 0.25:
                topic_entry['weight'] = 0.25
            elif topic_entry['weight'] > 0.55:
                topic_entry['weight'] = 0.55
            topic_entry['keyword'] = item[7:-1]
            topic_entry['category'] = 'controversial-' + str(topicNumber)
            topic_model_data.append(topic_entry)
        topicNumber += 1
    return topic_model_data

@app.route('/')
def render():
    #entries = db.session.query(TopPost).filter_by(date = 20171005).filter_by(subreddit = 'technology')
    date_of_interest = 20171009

    top = db.session.query(TopPost).filter_by(date = date_of_interest).filter_by(subreddit = subreddit_of_interest)
    controversial = db.session.query(ControversialPost).filter_by(date = date_of_interest).filter_by(subreddit = subreddit_of_interest)

    top_titles = []
    for post in top:
        top_titles.append(unescape(post.title))
    controversial_titles = []
    for post in controversial:
        controversial_titles.append(unescape(post.title))

    topic_model_data = calculateTopicModelData(top_titles, controversial_titles)
    return render_template('index.html',
                            top_titles = top_titles,
                            controversial_titles = controversial_titles,
                            topic_model_data = topic_model_data,
                            sub = subreddit_of_interest)

@app.route('/updateSubreddit', methods=['POST'])
def updateSubreddit():
    subreddit =  request.form['subreddit']
    global subreddit_of_interest
    subreddit_of_interest = subreddit[2:]
    return render()

if __name__ == '__main__':
    app.debug = True # debug setting!
    app.run()
