'''
Includes functions for retrieving and storing tweets.
This is intended to be called every minute.
'''

import argparse, json, datetime, uuid, tweepy, tweetwise_config
import logCreater as lc

twitter_logger = lc.setup_logger('first_logger', 'twitter_logfile.log')


class Tweet:
    def __init__(self, author, text, created_at):
        self.author = author
        self.text = text
        self.created_at = created_at
    
    def as_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


def authenticate():
    try:
        # Get api credentials from config file.
        # (config file is added to .gitignore for security)
        consumer_key = tweetwise_config.CONSUMER_KEY
        consumer_secret = tweetwise_config.CONSUMER_SECRET
        access_token = tweetwise_config.ACCESS_TOKEN
        access_token_secret = tweetwise_config.ACCESS_TOKEN_SECRET
    
        # Connect to api
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)
    except:
        print("Failed to authorize Tweepy.")
        return None
   
  
def get_latest_tweets(query, count):
    public_tweets = []
    
    api = authenticate()
    if (api):        
        try:
            for tweet in api.search(q=query, count=count, lang='en'):
                public_tweets.append(Tweet(tweet.author.screen_name,
                                           tweet.text,
                                           tweet.created_at.isoformat()))
        except:
            print("Tweepy request failed. Could not get tweets.")
    
    return public_tweets


def write_tweets_to_file(fname, tweets):
    if len(tweets) == 0:
        print("No tweets to write.")
        return

    try:
        count = 0
        with open(fname, 'a') as f:
            for t in tweets:
                f.write(t.as_json()+"\n")
                count += 1
                
        print("Successfully wrote", count, "tweets")
    except:
        print("Error writing tweets to '" + fname + "'")
    

def collect_tweets(type):
    twitter_info = "Getting tweets... (" +  str(datetime.datetime.now()) + ")"
    twitter_logger.info(twitter_info)
    #print("Getting tweets... (", datetime.datetime.now(), ")")

    query_string = type

    # The Twitter API allows 180 calls every 15 mins.
    # The number 11 gives us 165 calls per 15 mins,
    # putting us right under the limit.

    #All bullshit make 400 or 390
    T = get_latest_tweets(query_string, 390)
    return T

if __name__ == '__main__':
    print("Getting tweets... (", datetime.datetime.now(), ")")

    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output file", required=True)
    args = parser.parse_args()

    print(args.output)

    
    # The query string can be changed to whatever
    # you'd like. I use "bitcoin," as this is the 
    # query used in Colianni et al. At the moment,
    # the query string must be a single word.
    query_string = 'bitcoin'
    

    # The Twitter API allows 180 calls every 15 mins.
    # The number 11 gives us 165 calls per 15 mins,
    # putting us right under the limit.
    T = get_latest_tweets(query_string, 11)
    write_tweets_to_file(args.output, T)
