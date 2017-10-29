from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost
from topicmodel import get_topics
import json
import time

app = Flask(__name__)

# TODO COMMENT OUT BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/devel_db'

# purple
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cmodmuptjjyklg:e48f9a96060da864807bd5b967ea0447fd5c4814a7583facde3afd9d729726ce@ec2-184-72-248-8.compute-1.amazonaws.com:5432/dbogg3844cnn32'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
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

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


@app.route('/')
def main():
    # date_yesterday = int(time.strftime("%Y%m%d-%H%M%S")[:8]) - 1
    # # edge case for october -> november rollover.
    # if (date_yesterday == 20171100):
    #     date_yesterday = 20171031

    subreddit_of_interest = 'politics'
    start_date = 20171001
    end_date = 20171001
    return render(subreddit_of_interest, start_date, end_date)

def render(subreddit_of_interest, start_date, end_date):
    top = db.session.query(TopPost).filter(TopPost.date >= start_date).filter(TopPost.date <= end_date).filter_by(subreddit = subreddit_of_interest)
    controversial = db.session.query(ControversialPost).filter(ControversialPost.date >= start_date).filter(ControversialPost.date <= end_date).filter_by(subreddit = subreddit_of_interest)

    def yield_heartbeat():
        yield 'heartbeat'

    top_titles = []
    for post in top:
        top_titles.append(unescape(post.title))
    controversial_titles = []
    for post in controversial:
        controversial_titles.append(unescape(post.title))

    topic_model_data = calculateTopicModelData(top_titles, controversial_titles, subreddit_of_interest)

    return Response(stream_template('index.html',
                                    top_titles = top_titles,
                                    controversial_titles = controversial_titles,
                                    topic_model_data = topic_model_data,
                                    sub = subreddit_of_interest,
                                    start_date = start_date,
                                    end_date = end_date,
                                    heartbeat = yield_heartbeat()))

@app.route('/updateDataset', methods=['POST'])
def updateDataset():
    subreddit =  request.form['subreddit']
    subreddit_of_interest = subreddit[2:]
    date_range_str = request.form['daterange']
    start_date = int(date_range_str[6:10]+date_range_str[0:2]+date_range_str[3:5])
    end_date = int(date_range_str[19:23]+date_range_str[13:15]+date_range_str[16:18])
    return render(subreddit_of_interest, start_date, end_date)

# @app.route('/updateSubreddit', methods=['POST'])
# def updateSubreddit():
#     subreddit =  request.form['subreddit']
#     subreddit_of_interest = subreddit[2:]
#     date_range_str = request.form['daterange']
#     start_date = int(date_range_str[6:10]+date_range_str[0:2]+date_range_str[3:5])
#     end_date = int(date_range_str[19:23]+date_range_str[13:15]+date_range_str[16:18])
#     return render(subreddit_of_interest, start_date, end_date)
#
# @app.route('/updateDateRange', methods=['POST'])
# def updateDateRange():
#     subreddit =  request.form['subreddit']
#     subreddit_of_interest = subreddit[2:]
#     date_range_str = request.form['daterange']
#     start_date = int(date_range_str[6:10]+date_range_str[0:2]+date_range_str[3:5])
#     end_date = int(date_range_str[19:23]+date_range_str[13:15]+date_range_str[16:18])
#     return render(subreddit_of_interest, start_date, end_date)

if __name__ == '__main__':
    app.debug = True # debug setting!
    app.run()
