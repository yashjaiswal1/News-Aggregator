from os import error
from sqlite3.dbapi2 import OperationalError
from flask import Flask, request
from flask_restful import Resource, Api
from dataFormatingToolbox import tupleListToDict
import sqlite3

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    ''' Test route '''

    def get(self):
        return {"testJSON": "Hello World!"}


class BlogList(Resource):
    ''' Handles HTTP GET request, fetches query params (if any) and returns response '''

    def get(self):
        connection = sqlite3.connect(
            "/Users/yashjaiswal/Desktop/intern_project/News-Aggregator/RSSFeed.db")
        cur = connection.cursor()

        # fetching string query params
        page = int(request.args.get("page")) if request.args.get("page") else 1
        limit = int(request.args.get("limit")
                    ) if request.args.get("limit") else 50
        author = request.args.get("author")
        start_datetime = request.args.get("start") if request.args.get(
            "start") else "2021-01-01 00:00:00"
        end_datetime = request.args.get("end") if request.args.get(
            "end") else "2022-01-01 00:00:00"

        # query param validations
        if page != None and page <= 0:
            return {
                "status": "fail",
                "data": {
                    "title": "page parameter only accepts integers greater than zero"
                }
            }

        if limit != None and limit < 0:
            return {
                "status": "fail",
                "data": {
                    "title": "limit parameter only accepts non-negative integers"
                }
            }

        if start_datetime > end_datetime:
            return {
                "status": "fail",
                "data": {
                    "title": "start DateTime cannot be greater than the end DateTime"
                }
            }

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

        tupleListToDict(rows)

        if rows == []:
            return {
                "status": "success",
                "data": None
            }

        return {
            "status": "success",
            "data": {
                "blogs": rows
            }
        }


class Blog(Resource):
    ''' Handles HTTP GET request and returns JSON response consisting of details of the blog based on provided CommentsURL '''

    def get(self, CommentsURL):
        if CommentsURL == None:
            return {
                "status": "fail",
                "data": {
                    "title": "CommentURL of the blog is required"
                }
            }

        connection = sqlite3.connect(
            "/Users/yashjaiswal/Desktop/intern_project/News-Aggregator/RSSFeed.db")
        cur = connection.cursor()

        # format url to fetch ?id= param from input url
        url = CommentsURL + "?id=" + request.args.get("id")
        query = f"SELECT * FROM Blogs WHERE CommentsURL='{url}';"
        print(query)
        cur.execute(query)
        rows = cur.fetchall()
        connection.commit()
        connection.close()

        tupleListToDict(rows)

        if rows == []:
            return {
                "status": "fail",
                "data": {
                    "title": "CommentsURL does not exist in the database"
                }
            }

        return {
            "status": "success",
            "data": {
                "blog": rows
            }
        }


# registering routes
api.add_resource(HelloWorld, "/")
api.add_resource(BlogList, "/api")
api.add_resource(Blog, "/api/<path:CommentsURL>")

if __name__ == "__main__":
    app.run(debug=True)
