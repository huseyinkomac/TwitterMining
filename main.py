#coding=utf-8
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            tweet_to_json(data)
        except BaseException as e:
            print ("Error on_data: %s" % str(e))


def tweet_to_json(tweet):
    tweetcolls = {
        'created_at': tweet.created_at,
        'text': tweet.text,
        'language': tweet.lang,
        'location': tweet.geo,
        'metadata': tweet.metadata,
        'coordinates': tweet.coordinates,
        'source_url': tweet.source_url,
        'source': tweet.source,
        'contributors': tweet.contributors,
        'retweeted': tweet.retweeted,
        'entities': tweet.entities,
        'id': tweet.id
    }
    return tweetcolls


if __name__ == '__main__':
    consumer_key = 'nXx5fXyILAgLvlHt2Ko4uMJRJ'
    consumer_secret = 'JbWBH127CE4Ad15vTtCtBkininfhcK5p8znNzvBkHAwz42s9BJ'
    access_token = '916255827765407745-IdwnSRCXVuMOOQDTMlnqKd8raTRSQ3j'
    access_secret = 'sLORGVPeESVgApwKWaUEz0dhh0gmKOxWXFFMMSN7wo59j'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['#grip'])

    search_results = api.search(q="grip", rpp=100)

    client = MongoClient('172.17.0.1', 27017)
    db = client.tweets
    for tweet in search_results:
        print (dir(tweet))
        if tweet.lang == 'tr':
            db.tweetcolls.insert(tweet_to_json(tweet))
