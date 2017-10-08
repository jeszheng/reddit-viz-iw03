from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import TopPost, ControversialPost

app = Flask(__name__)

# TODO COMMENT OUT BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/devel_db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cqvjbobiquqase:a7d4d05d62c673ed79207cd44c9ae86573c164871b6c26e6b46bed410624295e@ec2-54-221-221-153.compute-1.amazonaws.com:5432/dac5ce63jaaa4s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route('/')
def render():
	#entries = db.session.query(TopPost).filter_by(date = 20171005).filter_by(subreddit = 'technology')
	date_of_interest = 20171007
	subreddit_of_interest = 'news'

	top = db.session.query(TopPost).filter_by(date = date_of_interest).filter_by(subreddit = subreddit_of_interest)
	controversial = db.session.query(ControversialPost).filter_by(date = date_of_interest).filter_by(subreddit = subreddit_of_interest)
	# TODO unescape titles.

	topics = [];
	topic_entry = {}
	topic_entry["label"] = 'Category 1';
	topic_entry["value"] = 1;
	topic_entry["category"] = 'top';
	topics.append(topic_entry);

	return render_template('index.html', top_posts = top, controversial_posts = controversial, topic_model_data = topics)

# @app.route('/')
# def show_entries():
# 	entries = db.session.query(TopPost).filter_by(date = 20171005).filter_by(subreddit = 'technology')
# 	return render_template('show_entries.html', entries=entries)

# @app.route('/add', methods=['POST'])
# def add_entry():
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.debug = True
    app.run()
