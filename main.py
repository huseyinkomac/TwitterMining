#coding=utf-8
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler

consumer_key = 'nXx5fXyILAgLvlHt2Ko4uMJRJ'
consumer_secret = 'JbWBH127CE4Ad15vTtCtBkininfhcK5p8znNzvBkHAwz42s9BJ'
access_token = '916255827765407745-IdwnSRCXVuMOOQDTMlnqKd8raTRSQ3j'
access_secret = 'sLORGVPeESVgApwKWaUEz0dhh0gmKOxWXFFMMSN7wo59j'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def tweet_to_json(tweet):
    tweetcolls = {
        'created_at': tweet.created_at,
        'text': tweet.text,
        'language': tweet.lang,
    }
    return tweetcolls


def algorithm_for_search(tweet):
    something = tweet


search_results = api.search(q="grip", count=100)
client = MongoClient('172.17.0.1', 27017)
db = client.tweets
for tweet in search_results:
    if tweet.lang == 'tr':
        db.tweetcolls.insert(tweet_to_json(tweet))
'''
def find_disease(){
}
'''



