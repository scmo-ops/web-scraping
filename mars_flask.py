from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def ihome():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_dict)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
  
    #Run the scrape funtion
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_dict.mars_collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)