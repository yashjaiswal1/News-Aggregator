import requests
import xml.etree.ElementTree as ET
import sqlite3


def fetchRSS():
    ''' Fetches the RSS XML file from url and overwrites fetchedBlogs.xml with the fetched data'''

    url = "https://hnrss.org/newest"
    response = requests.get(url)
    with open("fetchedBlogs.xml", "wb") as file:
        file.write(response.content)


def parseXML(filename):
    ''' Parses the fetched XML as an XML tree and returns a dictionary of fetched items '''

    tree = ET.parse(filename)
    root = tree.getroot()
    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    # list of dictionaries consisting of data present in <Item>
    blogitems = []

    # traversing XML tree to fetch data
    for item in root.findall("./channel/item"):
        blog = {}

        for child in item:
            if child.tag == "description" or child.tag == "guid":
                pass

            if child.tag == "pubDate":
                pubDate = child.text[5:25]
                day = pubDate[:2]
                month = months[pubDate[3:6]]
                year = pubDate[7:11]
                time = pubDate[12:]
                # datetime format = "YYYY-MM-DD HH:MM:SS"
                formatted_datetime = year + "-" + month + "-" + day + " " + time
                blog[child.tag] = formatted_datetime

            elif child.tag == "{http://purl.org/dc/elements/1.1/}creator":
                blog["author"] = child.text

            else:
                blog[child.tag] = child.text

        blogitems.append(blog)

    return blogitems


def initDB():
    ''' Creates a new table "Blogs" and indexes "Author" column 
        NOTE: This method is used only once to initialize SQLite3 DB'''

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
