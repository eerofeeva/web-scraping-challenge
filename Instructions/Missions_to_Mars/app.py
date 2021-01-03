from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection - inline
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    mars_info = scrape_mars.scrape()
    mongo.db.mars_info.update({}, mars_info, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
