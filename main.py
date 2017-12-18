#coding=utf-8
import tweepy
from pymongo import MongoClient
from tweepy import OAuthHandler


class MyStreamListener(tweepy.StreamListener):
    counter = 0

    def __init__(self, max_tweets=1000, *args, **kwargs):
        self.max_tweets = max_tweets
        self.counter = 0
        super(self).__init__(*args, **kwargs)

    def on_connect(self):
        self.counter = 0

    def on_status(self, status):
        self.counter += 1
        db.tojson.insert_one(status._json)


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
    client = MongoClient('172.17.0.1', 27017)
    db = client.tweets
    myStreamListener = MyStreamListener(max_tweets=100)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    keywords = ["Jupiter",
                "Python",
                "Data Mining",
                "Machine Learning",
                "Data Science",
                "Big Data",
                "DataMining",
                "MachineLearning",
                "DataScience",
                "BigData",
                "IoT",
                "#R",
                ]

    # Start a filter with an error counter of 20
    for error_counter in range(20):
        try:
            myStream.filter(track=keywords)
            print("Tweets collected: %s" % myStream.listener.counter)
            break
        except Exception as error:
            print("ERROR# %s" % (error_counter + 1))
            print (error)
    '''
    search_results = api.search(q="grip", rpp=100)
    client = MongoClient('172.17.0.1', 27017)
    db = client.tweets
    for tweet in search_results:
        print (dir(tweet))
        if tweet.lang == 'tr':
            db.tweetcolls.insert(tweet_to_json(tweet))
    '''
