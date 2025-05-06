import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()

def scrape_user_tweets_mook(username, num_tweets=5, mook: bool= True):
    """
    Scrape a Twiter user's original tweets (i.e., not retweets) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    
    tweets_list = []
    if mook:
        EDEN_TWITTER_GIST= "https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
        tweets = requests.get(EDEN_TWITTER_GIST,timeout=5).json()
        for tweet in tweets:

            tweet_dict = {}
            tweet_dict["text"] = tweet["text"]
            tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
            tweets_list.append(tweet_dict)
    
    return tweets_list


if __name__ == "__main__":
    tweets =  scrape_user_tweets_mook("EdenEmarco177")
    print(tweets)