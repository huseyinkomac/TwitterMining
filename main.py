#coding=utf-8
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        last_tweet = get_last_tweet()
        if not last_tweet or last_tweet['features'][0]['properties']['text'] != status.text:
            types = get_the_type(status)
            tweet_columns = tweet_to_geojson(status)
            tweet_columns['features'][0]['properties']['types'] = types
            db.tweetcolls.insert_one(tweet_columns)


def get_the_type(tweet):
    for i, word in enumerate(keywords):
        if word in tweet.text.lower().strip():
            if i <= 11:
                types = "flu"
            elif 12 <= i <= 18:
                types = "cholera"
            elif 19 <= i <= 22:
                types = "diphtheria"
            else:
                types = "norovirus"
            return types


def get_last_tweet():
    last_tweet = list(db.tweetcolls.find({}).sort('$natural', -1).limit(1))
    if last_tweet:
        last_tweet = last_tweet[0]
    return last_tweet


def tweet_to_geojson(tweet):
    tweetcolls = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": tweet.coordinates,
            "properties": {
                "text": tweet.text,
                "created_at": tweet.created_at,
                "types": "types"
            }
        }]
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
    client = MongoClient('172.17.0.1', 27017)
    db = client.tweets
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    with open("keywords.txt") as f:
        keywords = f.read().split(",")
    myStream.filter(track=keywords, languages=["en"])
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