from subprocess import call

date = 20171118
call(["python", "title_sentiment.py", str(date)])
call(["python", "comments_sentiment.py", str(date)])
