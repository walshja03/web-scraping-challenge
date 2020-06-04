from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_sites

app = Flask(__name__)

# Connect to mongodb

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():

    # Find one record of data from the mongo database
    print("index route")
    website_data = mongo.db.collection.find_one()
    print(website_data)
    # Return template and data
    return render_template("index.html", mars=website_data)


@app.route("/scrape")
def scraper():
    
    # Run the scrape function
    mars_data = scrape_mars_sites.scrape()
    print(mars_data)
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)