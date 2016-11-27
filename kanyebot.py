import os
import markovbot
import time, sched
import tweepy

from markovbot import MarkovBot

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print("...%s tweets downloaded so far" % (len(alltweets)))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
	with open('%s_tweets.txt' % screen_name, 'wb') as f:
                for tweet in alltweets:
                        f.write(tweet.text.encode("utf-8")+' '.encode("utf-8"))

	pass

get_all_tweets("kanyewest")
kanyebot = MarkovBot()

# Get the current directory's path
dirname = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the book
tweets = os.path.join(dirname, 'kanyewest_tweets.txt')
# Make your bot read the book!
kanyebot.read(tweets)

kanyebot.twitter_login(consumer_key, consumer_secret, access_key, access_secret)

# Set some parameters for your bot
targetstring = 'KanyeToTheBot'
keywords = ['kim', 'pablo', 'wavy', 'bill', 'cosby']
prefix = None
suffix = '#KanyeToTheBot'
maxconvdepth = None

# Start periodically tweeting
kanyebot.twitter_tweeting_start(days=0, hours=0, minutes=15, keywords=None, prefix=None, suffix='#KanyeToTheBot')

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    # do your stuff
    s.enter(3600, 1, get_all_tweets("kanyewest"), (sc,))
    print("gathering more tweets...")
s.enter(3600, 1, do_something, (s,))
s.run()
