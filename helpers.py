import html
import os
import plotly
import socket
import pprint
from twython import Twython
from twython import TwythonAuthError, TwythonError, TwythonRateLimitError

pp = pprint.PrettyPrinter(indent=4)

def chart(positive, negative):
    """Return a pie chart for specified sentiments as HTML."""

    # offline plot
    # https://plot.ly/python/pie-charts/
    # https://plot.ly/python/reference/#pie
    figure = {
        "data": [
            {
                "labels": ["positive", "negative"],
                "hoverinfo": "none",
                "marker": {
                    "colors": [
                        "rgb(0,255,00)",
                        "rgb(255,0,0)"
                    ]
                },
                "type": "pie",
                "values": [positive, negative]
            }
        ],
        "layout": {
            "showlegend": False
            }
    }
    return plotly.offline.plot(figure, output_type="div", show_link=False, link_text=False)

def get_tweets(lat, long, keyword):
    """returns parsable tweets based on call to twitter's search API"""
    
    # format inputs
    formatted_geocode = str(lat) + "," + str(long) + "," + "10mi"

    # get keys 
    with open("twitter_keys.txt","r") as file:
        keys = file.readlines()
        
    api_key = keys[1].rstrip("\n")
    api_secret = keys[2].rstrip("\n")
    
    api_url = "https://api.twitter.com/1.1/search/tweets.json"
    keyword = keyword + " -filter:retweets"
    
    try:
        twitter = Twython(api_key, api_secret)
        constructed_url = twitter.construct_api_url(api_url,q=keyword,geocode=formatted_geocode,result_type="recent",tweet_mode="extended",count=200)
        
        results = twitter.request(constructed_url)
        tweets = results["statuses"]
        
        if not tweets:
            return False
        
        if tweets:
            for tweet in tweets:
                fav_count = 0
                rt_count = 0
                if tweet['favorite_count'] > fav_count:
                    fav_text = tweet['full_text']
                    fav_count = tweet['favorite_count']
                    fav_author = "@" + tweet['user']['screen_name']
            
            if fav_count != 0:
                fav_tweet = {"fav_text": fav_text, "fav_count": fav_count, "fav_author": fav_author}
            else: 
                fav_tweet = ""
        
        else:
            fav_tweet = ""
            
        return [[html.unescape(tweet["full_text"].replace("\n", " ")) for tweet in tweets], fav_tweet ]
        
    except TwythonAuthError:
        raise RuntimeError("invalid API key and/or secret. Sorry m8.")
    except TwythonRateLimitError:
        raise RuntimeError("Woa der slow down! You've hit a rate limit.")
    except TwythonError:
        return None
        
    return None
