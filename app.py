from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv
 
# to avoid multiple running app, make a create_app() function
def create_app():
    app = Flask(__name__)
    dbclient = MongoClient(os.environ.get(MONGODB_BLOG))
    db = dbclient.microblog
    #print(dbclient.list_database_names())

    #entries = []
    #tbentries = db.entries

    @app.route("/", methods = ['GET', 'POST'])
    def home():
        # retrieve info from db
        # print([e for e in app.db.entries.find({})])
        if request.method == "POST":        
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            #print(entry_content, formatted_date)
            #entries.append((entry_content, formatted_date))
            db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        """
        entries_with_date = [
            (
                entry[0],
                entry[1],
                datetime.datetime.strptime(entry[1],"%Y-%m-%d").strftime("%b %d %Y")
            )
            for entry in entries 
        ]
        """
        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.datetime.strptime(entry['date'],"%Y-%m-%d").strftime("%b %d %Y")
            )
            for entry in db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app
