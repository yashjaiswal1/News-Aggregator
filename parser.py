import requests
import xml.etree.ElementTree as ET
import sqlite3


def fetchRSS():
    url = "https://hnrss.org/newest"
    response = requests.get(url)
    with open("fetchedBlogs.xml", "wb") as file:
        file.write(response.content)


def parseXML(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    # array of dictionaries consisting of data present in <Item>
    blogitems = []

    for item in root.findall("./channel/item"):

        blog = {}

        for child in item:
            if child.tag == "description" or child.tag == "guid":
                pass
            if child.tag == "pubDate":
                blog[child.tag] = child.text[5:25]
            elif child.tag == "{http://purl.org/dc/elements/1.1/}creator":
                blog["author"] = child.text
            else:
                blog[child.tag] = child.text
        blogitems.append(blog)

    return blogitems


def initDB():
    connection = sqlite3.connect("RSSFeed.db")
    cur = connection.cursor()

    cur.execute('''CREATE TABLE Blogs
               (Title varchar(255) NOT NULL, 
               PubDate datetime NOT NULL, 
               BlogURL varchar(255), 
               Author varchar(255) NOT NULL, 
               CommentsURL varchar(255) NOT NULL,
               PRIMARY KEY (CommentsURL) ON CONFLICT IGNORE);''')

    cur.execute('''CREATE INDEX author_index ON Blogs(Author);''')
    connection.commit()
    connection.close()


def saveToDB(blogitems):
    connection = sqlite3.connect(
        "/Users/yashjaiswal/Desktop/intern_project/News-Aggregator/RSSFeed.db")
    cur = connection.cursor()
    for item in blogitems:
        query = f'INSERT INTO Blogs VALUES("{item["title"]}", "{item["pubDate"]}", "{item["link"]}", "{item["author"]}", "{item["comments"]}");'
        cur.execute(query)
    connection.commit()
    connection.close()


fetchRSS()
blogitems = parseXML("fetchedBlogs.xml")
# initDB()
saveToDB(blogitems)
