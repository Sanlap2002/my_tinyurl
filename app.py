from flask import Flask, render_template, url_for, redirect, request
import string
import random
app=Flask(__name__)

shortened_urls={} 

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
        return render_template("index.html", short_url=request.url_root + short_url)
    return render_template("index.html")   
@app.route("/<short_url>")
def redirect_url(short_url):
    long_url=shortened_urls[short_url]
    if long_url:
        return redirect(long_url)
    else:
        return "404:URL NOT FOUND",404
    
if __name__=='__main__':
        app.run(debug=True)