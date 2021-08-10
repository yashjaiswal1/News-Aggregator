from flask import Flask, request
from flask_restful import Resource, Api
from collections import defaultdict
import sqlite3
import json

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {"testJSON": "Hello World!"}


class BlogList(Resource):
    def get(self):
        connection = sqlite3.connect(
            "/Users/yashjaiswal/Desktop/intern_project/News-Aggregator/RSSFeed.db")
        cur = connection.cursor()

        query = "SELECT * FROM Blogs ORDER BY(PubDate) DESC;"
        cur.execute(query)

        rows = cur.fetchall()
        connection.commit()
        connection.close()
        return rows


api.add_resource(HelloWorld, "/")
api.add_resource(BlogList, "/api")

if __name__ == "__main__":
    app.run(debug=True)
