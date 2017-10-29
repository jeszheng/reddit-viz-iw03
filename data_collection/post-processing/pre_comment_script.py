from subprocess import call

# for i in range(20170925, 20170931):
#     date = i
#     call(["python", "title_sentiment.py", str(date)])

for i in range(20171001, 20171029):
    date = i
    call(["python", "title_sentiment.py", str(date)])
