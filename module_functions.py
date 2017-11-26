from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost
from topicmodel import get_topics
import json
import time
from ibm_topic_modeler import ibm_get_topics
import tldextract
# from collections import Counter
from source_category import categorize

app = Flask(__name__)

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

def get_domain_name(url):
    try:
        result = tldextract.extract(url)
        domain_name = '.'.join([result.domain, result.suffix])
    except:
        domain_name = ''
    return domain_name

# def get_domain_frequencies(list_of_domains):
#     counts = Counter(list_of_domains)
#     counts_tuple = counts.most_common()
#     counts_dict_raw = dict((x,y) for x,y in counts_tuple)
#     counts_dict = []
#     for entry in counts_dict_raw:
#         element = {}
#         element['domain'] = entry
#         element['count'] = counts_dict_raw[entry]
#         counts_dict.append(element)
#     return counts_dict

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

def getIndividualDayTitles_Top(subreddit_of_interest, start_date, end_date):
    top_titles_by_day = []
    cur_date = start_date
    while cur_date <= end_date:
        element = {}
        element['date'] = cur_date
        top = db.session.query(TopPost).filter(TopPost.date == cur_date).filter_by(subreddit = subreddit_of_interest)
        top_titles = []
        for post in top:
            top_titles.append(unescape(post.title))
        element['titles'] = top_titles
        top_titles_by_day.append(element)
        if cur_date == 20171031:
            cur_date = 20171101
        else:
            cur_date += 1
    return top_titles_by_day

def getIndividualDayTitles_Controversial(subreddit_of_interest, start_date, end_date):
    controversial_titles_by_day = []
    cur_date = start_date
    while cur_date <= end_date:
        element = {}
        element['date'] = cur_date
        controversial = db.session.query(ControversialPost).filter(ControversialPost.date == cur_date).filter_by(subreddit = subreddit_of_interest)
        controversial_titles = []
        for post in controversial:
            controversial_titles.append(unescape(post.title))
        element['titles'] = controversial_titles
        controversial_titles_by_day.append(element)
        if cur_date == 20171031:
            cur_date = 20171101
        else:
            cur_date += 1
    return controversial_titles_by_day

def dataToBeRendered(subreddit_of_interest, start_date, end_date):
    top = db.session.query(TopPost).filter(TopPost.date >= start_date).filter(TopPost.date <= end_date).filter_by(subreddit = subreddit_of_interest)
    controversial = db.session.query(ControversialPost).filter(ControversialPost.date >= start_date).filter(ControversialPost.date <= end_date).filter_by(subreddit = subreddit_of_interest)

    top_titles = []
    controversial_titles = []
    posneg_data = []
    political_data = []
    top_post_data = []
    controversial_post_data = []
    top_domains = []
    controversial_domains = []

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
        posneg['Liberal Sentiment'] = post.liberal
        posneg['Conservative Sentiment'] = post.conservative
        posneg['Libertarian Sentiment'] = post.libertarian
        posneg['Liberal Conservative Ratio'] = post.liberal/post.conservative # can be weird.
        posneg['Liberal Conservative Difference'] = post.liberal - post.conservative
        posneg_data.append(posneg)
        post_data = {}
        post_data['title'] = unescape(post.title)
        post_data['permalink'] = post.permalink
        post_data['post_id']= post.post_id
        controversial_post_data.append(post_data)
        controversial_domains.append(get_domain_name(post.url))

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
        posneg['Liberal Sentiment'] = post.liberal
        posneg['Conservative Sentiment'] = post.conservative
        posneg['Libertarian Sentiment'] = post.libertarian
        posneg['Liberal Conservative Ratio'] = post.liberal/post.conservative
        posneg['Liberal Conservative Difference'] = post.liberal - post.conservative
        posneg_data.append(posneg)
        post_data = {}
        post_data['title'] = unescape(post.title)
        post_data['permalink'] = post.permalink
        post_data['post_id']= post.post_id
        top_post_data.append(post_data)
        top_domains.append(get_domain_name(post.url))

    # temporarily disable.
    topic_model_data = calculateTopicModelData(top_titles, controversial_titles, subreddit_of_interest)
    #topic_model_data = []

    top_titles_by_day = getIndividualDayTitles_Top(subreddit_of_interest, start_date, end_date)
    controversial_titles_by_day = getIndividualDayTitles_Controversial(subreddit_of_interest, start_date, end_date)

    topic_model_data_day = []

    for i in range(0, min(len(top_titles_by_day), len(controversial_titles_by_day))):
        element = {}
        element['date'] = top_titles_by_day[i]['date']
        top_titles_cur_day = top_titles_by_day[i]['titles']
        controversial_titles_cur_day = controversial_titles_by_day[i]['titles']
        topic_model_data_one_day = calculateTopicModelData(top_titles_cur_day, controversial_titles_cur_day, subreddit_of_interest)
        element['data'] = topic_model_data_one_day
        topic_model_data_day.append(element)

    # top_domains_freq = get_domain_frequencies(top_domains)
    # controversial_domains_freq = get_domain_frequencies(controversial_domains)
    top_domains_categories = categorize(top_domains)
    controversial_domains_categories = categorize(controversial_domains)

    dataset = {}
    dataset['top_titles'] = top_titles
    dataset['controversial_titles'] = controversial_titles
    dataset['topic_model_data'] = topic_model_data
    dataset['topic_model_data_day'] = topic_model_data_day
    dataset['start_date'] = start_date
    dataset['end_date'] = end_date
    dataset['subreddit_of_interest'] = subreddit_of_interest
    dataset['posneg_data'] = posneg_data
    dataset['top_post_data'] = top_post_data
    dataset['controversial_post_data'] = controversial_post_data
    dataset['top_domains_categories'] = top_domains_categories
    dataset['controversial_domains_categories'] = controversial_domains_categories
    # dataset['top_domains_freq'] = top_domains_freq
    # dataset['controversial_domains_freq'] = controversial_domains_freq


    return dataset
