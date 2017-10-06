from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/blog'
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<h1>%r</h1>' % self.title

@app.route('/')
def show_entries():
	entries = db.session.query(Entry).all()
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
