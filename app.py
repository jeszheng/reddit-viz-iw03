from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost
from topicmodel import get_topics

# form file import function

app = Flask(__name__)

# TODO COMMENT OUT BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/devel_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)

# html_escape_table = {
#     "&amp;" : "&",
#     "&quot;" : '"',
#     "&apos;" : "'",
#     "&gt;" : ">",
#     "&lt;" : "<",
#     }
#
# def html_unescape(text):
#     # """Produce entities within text."""
#     return "".join(html_escape_table.get(c,c) for c in text)

@app.route('/')
def render():
    #entries = db.session.query(TopPost).filter_by(date = 20171005).filter_by(subreddit = 'technology')
    date_of_interest = 20171008
    subreddit_of_interest = 'news'

    top = db.session.query(TopPost).filter_by(date = date_of_interest).filter_by(subreddit = subreddit_of_interest)
    controversial = db.session.query(ControversialPost).filter_by(date = date_of_interest).filter_by(subreddit = subreddit_of_interest)

    top_titles = []
    for post in top:
        top_titles.append(post.title.replace("&apos;", "'"))
    controversial_titles = []
    for post in controversial:
        controversial_titles.append(post.title.replace("&apos;", "'"))

    topics = []

    unprocessed_topic_data = get_topics(top_titles)

    topicNumber = 0
    for topic_tuple in unprocessed_topic_data:
        topic_and_weights = topic_tuple[1].split(' + ')
        for item in topic_and_weights:
            topic_entry = {}
            topic_entry['weight'] = float(item[0:5]) * 30
            topic_entry['keyword'] = item[7:-1]
            topic_entry['category'] = 'top-' + str(topicNumber)
            topics.append(topic_entry)
        topicNumber += 1

    return render_template('index.html',
                            top_titles = top_titles,
                            controversial_titles = controversial_titles,
                            topic_model_data = topics)


if __name__ == '__main__':
    app.debug = True # debug setting!
    app.run()
