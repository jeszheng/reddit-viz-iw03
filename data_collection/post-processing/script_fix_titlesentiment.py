from subprocess import call

# 20171002
for i in range(20171026, 20171032):
    date = i
    call(["python", "redo_title_sentiment.py", str(date)])
