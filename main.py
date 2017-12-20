#coding=utf-8
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.coordinates:
            db.tweetcolls.insert_one(tweet_to_json(status))


def tweet_to_json(tweet):
    tweetcolls = {
        'created_at': tweet.created_at,
        'text': tweet.text,
        'language': tweet.lang,
        'location': tweet.geo,
        'coordinates': tweet.coordinates
    }
    return tweetcolls


def searching_algorithm(tweet):
    txt = tweet.text


if __name__ == '__main__':
    consumer_key = 'nXx5fXyILAgLvlHt2Ko4uMJRJ'
    consumer_secret = 'JbWBH127CE4Ad15vTtCtBkininfhcK5p8znNzvBkHAwz42s9BJ'
    access_token = '916255827765407745-IdwnSRCXVuMOOQDTMlnqKd8raTRSQ3j'
    access_secret = 'sLORGVPeESVgApwKWaUEz0dhh0gmKOxWXFFMMSN7wo59j'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    client = MongoClient('172.17.0.1', 27017)
    db = client.tweets
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    keywords = ["flu", "grip", "illness", "sick", "not feeling good", "ill", "cold", "cholera", "diphtheria"]
    myStream.filter(track=keywords)
    '''
    for error_counter in range(20):
        try:
            myStream.filter(track=keywords)
            break
        except Exception as error:
            print("ERROR# %s" % (error_counter + 1))
            print (error)
    '''
    '''
    search_results = api.search(q="grip", rpp=100)
    client = MongoClient('172.17.0.1', 27017)
    db = client.tweets
    for tweet in search_results:
        print (dir(tweet))
        if tweet.lang == 'tr':
            db.tweetcolls.insert(tweet_to_json(tweet))
    '''