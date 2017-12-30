#prints a dictionary of the votes from the thread in the readme

import praw
import re
from coins import coinlist

#convert the coin list to a dict to count votes
coindict= {key:0 for key in coinlist}

#connect and get the appropriate thread
user_agent = "coinVote 1.0 by /u/wjhall"
r = praw.Reddit(client_id = "your client_id",
                client_secret = " your client_secret",
                user_agent = user_agent)

submission = r.submission(id='7mgd3g')

for comment in submission.comments:
    #get the top level comment body, strip out punctuation and split to words
    body = comment.body
    body = body.upper()
    body = re.sub(r'([^A-Z])',' ',body)
    body = re.split(r'( +)',body)

    #compare each word against the coin dictioary and record in the temp_list
    #set to True avoids double count where coins are mentioned multiple times
    #in a single comment
    temp_list={}
    for word in body:
        if word in coindict:
            temp_list[word]=True

    #+1 vote for each coin identified in the comment
    for key, value in temp_list.iteritems():
        coindict[key]+=1

#remove any with nil votes and print
votelist = {key:value for key, value in coindict.iteritems() if value!=0}

# sort the dictionary to know the most voted
votelist_sort = sorted(votelist, key=votelist.get, reverse=True)

print votelist

# create a file with all the votes
fo = open("Votes.txt", "w")
for k in votelist_sort:
    v = votelist[str(k)]
    fo.write("> " + str(k) + ': '+ str(v) + '\n\n')
fo.close()
