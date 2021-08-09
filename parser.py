import requests
import xml.etree.ElementTree as ET


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
            elif child.tag == "{http://purl.org/dc/elements/1.1/}creator":
                blog["creator"] = child.text
            else:
                blog[child.tag] = child.text

        blogitems.append(blog)

    return blogitems


fetchRSS()
parseXML("fetchedBlogs.xml")
