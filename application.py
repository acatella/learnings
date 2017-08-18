from flask import Flask, redirect, render_template, request, url_for

import googlemaps
import os
import pprint
import sys
import helpers
from datetime import datetime
from cs50 import SQL
from analyzer import Analyzer

app = Flask(__name__)
pp = pprint.PrettyPrinter(indent=4)

db = SQL("sqlite:///learnings.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET","POST"])
def search():

    # was it a post request? 
    if request.method == "POST":
        
        #validate inputs for location and keyword
        location = request.form.get("location")
        keyword = request.form.get("keyword")
        
        if not keyword or not location:
            return render_template("index.html",error_message="Please enter a valid location and keyword")
            
        # geocode location via google maps api: https://github.com/googlemaps/google-maps-services-python
        with open("gmaps_key.txt","r") as file:
            key = file.read().replace('\n','')
        
        gmaps = googlemaps.Client(key=key)
        geocode_result = gmaps.geocode(location)
            
        if not geocode_result:
            return render_template("index.html",error_message="Sorry... I couln't find that place. Can you try somewhere real?")
        
        formatted_location = geocode_result[0]["formatted_address"]
        geocode = geocode_result[0]["geometry"]["location"]
        
        # pass geocoded location and key word into get_tweets()
        tweet_info = helpers.get_tweets(geocode["lat"],geocode["lng"], keyword)
        
        if not tweet_info:
            error_message = "Sorry, it doesn't look like anyone in " + formatted_location + " is tweeting about " + keyword + " right now"
            return render_template("index.html",error_message=error_message)
            
        tweets = tweet_info[0]
        fav_tweet = tweet_info[1]
        
        # absolute paths to lists
        positives = os.path.join(sys.path[0], "positive-words.txt")
        negatives = os.path.join(sys.path[0], "negative-words.txt")
        
        # instantiate analyzer from Analyzer class
        analyzer = Analyzer(positives,negatives)
        
        # calculate sentiment values
        positive, negative, neutral = 0, 0, 0
        for tweet in tweets:
            score = analyzer.analyze(tweet)
            if score > 0:
                positive += score
            if score < 0:
                negative += score * -1
            else:
                neutral += score
        
        print(positive)
        print(negative)
        print(neutral)
        
        # generate chart
        if (positive == 0 and negative == 0):
            chart = ""
        else:
            chart = helpers.chart(positive, negative)
        
        # create sentence
        diff = positive - negative
        adj = "fairly"
        
        if (diff > 5):
            if diff > 10:
                adj = "very"
            
            sentiment = "positive"
            message = "Recent tweets from " + formatted_location + " contain " + adj + " positive language when referencing " + keyword
            past_tense_message = "recent tweets from " + formatted_location + " contained " + adj + " positive language when referencing " + keyword
        
        elif (diff < -5):
            if diff < -10:
                adj = "very"
            
            sentiment = "negative"
            message = "Recent tweets from " + formatted_location + " contain " + adj + " negative language when referencing " + keyword
            past_tense_message = "recent tweets from " + formatted_location + " contained " + adj + " negative language when referencing " + keyword
        else: 
            sentiment = "neutral"
            message = "Recent tweets from " + formatted_location + " contain neutral language when referencing " + keyword
            past_tense_message = "recent tweets from " + formatted_location + " contained neutral language when referencing " + keyword
            
        # send info to db table
        d = datetime.today()
        date = d.strftime("%A, %B %d %Y")
        
        db.execute("INSERT INTO learnings (message, query, lat, lng, date, past_message, sentiment) VALUES (:message, :query, :lat, :lng, :date, :past_message, :sentiment)",message=message,query=keyword,lat=geocode["lat"],lng=geocode["lng"], date=date, past_message=past_tense_message,sentiment=sentiment)
        
        # render template
        return results(message, fav_tweet, chart)
    else:
        return render_template("index.html", error_message="")
    
@app.route("/learnings", methods=["GET"])
def learnings():
    """ Displays past learnings to users"""
    
    if request.method == "POST":
        return render_template("index.html", error_message="")
    else:
        total_learnings = db.execute("SELECT COUNT(*) FROM learnings")
        
        if not total_learnings:
            message = "Looks like we haven't learned anything recently. Can you help?"
            return render_template("learnings.html",headline=message)
            
        total_learnings = total_learnings[0]["COUNT(*)"]
        if total_learnings > 25:
            min_index = total_learnings - 25
            total_learnings = 25
        else:
            min_index = 0
        
        if (total_learnings == 1):
            message = "Here's the most recent thing we've learned."
        else:
            message = "Here's the " + str(total_learnings) + " most recent things we've learned."
            
        past_learnings = db.execute("SELECT * FROM learnings WHERE id > :min_index ORDER BY id DESC", min_index=min_index)
        
        return render_template("learnings.html", learnings=past_learnings, headline=message)
        
@app.route("/results")
def results(message="",fav_tweet="",chart=""):
    """ Displays results based on users inputs"""
    if not message:
        return render_template("index.html")
        
    return render_template("result.html",message=message,fav_tweet=fav_tweet, chart=chart)
    