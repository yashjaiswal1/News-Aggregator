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

        # fetching string query params
        page = int(request.args.get("page")) if (request.args.get(
            "page") != None and int(request.args.get("page")) >= 1) else 1
        limit = int(request.args.get("limit")
                    ) if (request.args.get("limit") != None and int(request.args.get("limit")) >= 0) else 50
        author = request.args.get("author")
        start_datetime = request.args.get("start") if request.args.get(
            "start") else "2021-01-01 00:00:00"
        end_datetime = request.args.get("end") if request.args.get(
            "end") else "2022-01-01 00:00:00"

        query_start = f"SELECT * FROM Blogs WHERE PubDate BETWEEN '{start_datetime}' AND '{end_datetime}' "
        query_mid = f'AND Author="{author}" '
        query_end = f"ORDER BY(PubDate) DESC LIMIT {(page-1) * limit},{limit};"

        if author:
            query_main = query_start + query_mid + query_end
        else:
            query_main = query_start + query_end

        cur.execute(query_main)
        rows = cur.fetchall()
        connection.commit()
        connection.close()
        return rows


api.add_resource(HelloWorld, "/")
api.add_resource(BlogList, "/api")

if __name__ == "__main__":
    app.run(debug=True)
