from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from models import Entry, TopPost, ControversialPost

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/blog'

# TODO COMMENT OUT BEFORE PUSH
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pdljaindlmyhbe:008fbca0484298c84029cbb521369c31b2bf7387a854310f44853c9b00e5d98a@ec2-54-204-41-80.compute-1.amazonaws.com:5432/dfnh4bhma6efun'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

heroku = Heroku(app)
db = SQLAlchemy(app)

@app.route('/')
def show_entries():
	entries = db.session.query(TopPost).filter_by(date = 20171005).filter_by(subreddit = 'technology')
	return render_template('show_entries.html', entries=entries)

# @app.route('/add', methods=['POST'])
# def add_entry():
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                  [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# # Set "homepage" to index.html
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# # Save e-mail to database and send to success page
# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('success.html')
#     return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
