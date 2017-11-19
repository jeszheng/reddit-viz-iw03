from subprocess import call

# 20171002
# for i in range(20171116, 20171119):
#     date = i
#     call(["python", "redo_title_sentiment.py", str(date)])


date = 20171118
call(["python", "redo_title_sentiment.py", str(date)])
