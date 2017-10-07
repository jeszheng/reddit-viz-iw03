import sys
import json

allPostsOrig = []

date = "20170925-164850"

with open(
'/Users/jessicazheng/Documents/Academics/2017-2018/IW3/cos-iw-reddit/data_collection/jessica_data/' + date + '_top.json') as data_file:
    allPostsOrig = json.load(data_file)

for cleanPost in allPostsOrig:
    cleanPost["selftext"] = cleanPost["selftext"].replace('\n', '')
    for comment in cleanPost["controversial_comments"]:
        comment["body"] = comment["body"].replace('\n', '')
    for comment in cleanPost["top_comments"]:
        comment["body"] = comment["body"].replace('\n', '')

with open(
date + '_top.json', 'w') as outfile:
    json.dump(allPostsOrig, outfile)
