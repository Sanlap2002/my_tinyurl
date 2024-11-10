from flask import Flask, render_template, url_for, redirect, request
import string
import random
import json
import os
app=Flask(__name__)

shortened_urls={} 
DATA_FILE="urls.json"
#Function to save the urls in JSON file
def save_urls():
     global shortened_urls
     with open("urls.json","w") as file:
          json.dump(shortened_urls,file)

#Function to load urls from the json file
def load_urls():
    global shortened_urls
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                shortened_urls = json.load(file)
        except json.JSONDecodeError:          
            shortened_urls = {}
#Function to shorten an url
def generate_short_url():
    chars=string.ascii_letters + string.octdigits

    short_url="".join(random.choice(chars) for _ in range(9)) #Produces a string of length 9 with random combination of alphabets and octa digits

    return short_url

@app.route("/",methods=["GET","POST"])
def index():
    if request.method== "POST":
        long_url=request.form['long_url']
        short_url=generate_short_url()
        #Check whether the generated url is present in the shortened url or not and keep generating short urls until an unique url is produced
        while short_url in shortened_urls:
            short_url=generate_short_url()
        shortened_urls[short_url]=long_url
        save_urls()
        return render_template("index.html", short_url=request.url_root + short_url)
    return render_template("index.html")   
@app.route("/<short_url>")
def redirect_url(short_url):
    long_url=shortened_urls[short_url]
    if long_url:
        return redirect(long_url)
    else:
        return "404:URL NOT FOUND",404
load_urls()   
if __name__=='__main__':
        app.run(debug=True)