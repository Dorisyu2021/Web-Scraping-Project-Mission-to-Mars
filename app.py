from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)

#conn = 'mongodb://localhost:27017'
#client = PyMongo.MongoClient(conn)
#db = client.mars_db

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data=mongo.db.mars.find_one()
    return render_template("index.html",data=mars_data)

@app.route("/scrape")
def scrape():
    print("Check out my scrape!")
    mars_data=mongo.db.mars
    mars=scrape_mars.scrape_all()
    mars.update({},mars,upsert=True)
    return"Successful!"

if __name__=="__main":
    app.run(debug=True)