from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper

app = Flask(__name__, template_folder='templates')
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    existing_data = mongo.db.mars_data.find_one()
    return render_template("index.html", existing_data=existing_data)

@app.route("/scrape")
def scrape():
    existing_data = mongo.db.mars_data
    website_data = scraper.Scraper()
    existing_data.update({}, website_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)