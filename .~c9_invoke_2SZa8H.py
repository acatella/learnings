from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

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
        
        
        # pass geocoded location and key word into get_tweets()
        
        # absolute paths to lists
        
        # instantiate analyzer
        
        # calculate sentiment values
        
        # send info to db table
        
        # create chart
        
        # render template
        return render_template("index.html",error_message="location: {} keyword: {}".format(location,keyword))
    else:
        return render_template("index.html")
    
    