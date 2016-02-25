import praw
import time
import os
from datetime import datetime
from bot_config import *

r = praw.Reddit('CSA_Test by Sunkinship /u/CIA_bot')
print("Logging in...")
#r.login(disable_warning=True)

#Sets up temporary submission cache and Subreddits to beg @
start_time = datetime.now()
cache = []
subreddits = ["FreeKarma"]

# Create the Reddit instance
user_agent = ("Automated Begging for /u/"+REDDIT_USERNAME)
r = praw.Reddit(user_agent=user_agent)
# and login
r.login(REDDIT_USERNAME, REDDIT_PASS,disable_warning=True)

def get_date(submission):
    time = submission.created
    return datetime.fromtimestamp(time)

def run_bot():
    if not os.path.isfile("bot_config.py"):
        print("Please check that the configuration file is created.")
        exit(1)
    running = True
    n = 1
    while running:
        try:
            for sub in subreddits:
                print("Grabbing subreddit: %s..." %sub)
                subreddit = r.get_subreddit(sub)
                new = subreddit.get_new()
                for submission in new:
                    if get_date(submission) < start_time:
                        print("Old post found... \n These are not the posts you are looking for...\n")

                    elif submission.id not in cache:
                        print(str(datetime.now()))
                        print("Match found! Submission ID: " + submission.id)
                        print("Posted at: %s" %str(get_date(submission)))
                        #submission.add_comment("Hey I'm a new bot! Care to share some love? (Karma==love)")
                        submission.upvote()
                        print("Get dat Karma Brah")
                        cache.append(submission.id)
                        #implement time printing
                        #time.sleep(20)
                print("Beg-cycle number " + str(n) + ": Begging loop finished, time to sleep\n\n")
            time.sleep(600)    
            n = n + 1
        except KeyboardInterrupt:
            running = False
        except Exception as e:
            print('Error: ', e)
            print('Going to sleep for ' + str(10) + ' minutes...\n')
            time.sleep(600)
            
run_bot()

