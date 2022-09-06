#Design a Flash API for Mars Data Scrap
from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from scrape_mars import scrape

################################################
# Flask Setup
#################################################
app = Flask(__name__)

################################################
# mongodb connection
#################################################
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# identify the collection
mars_data = mongo.db.mars_data
# mars_data.drop()

#################################################
# List all Flask Routes
#################################################
#Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    mars_details = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_details)
    

#scrape route

@app.route("/scrape")
def scrape():
   # drop collection
    mars_data.drop()

    mars_scraped_data = scrape()
    print (mars_scraped_data)

    #update mongo db
    mars_data.insert_many([mars_scraped_data])
    return redirect("/", code=302)

    session.close()
#################################################
if __name__ == '__main__':
    app.run(debug=True)