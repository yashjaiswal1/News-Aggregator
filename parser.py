import requests
import xml.etree.ElementTree as ET


def fetchRSS():
    url = "https://hnrss.org/newest"
    response = requests.get(url)
    with open("fetchedBlogs.xml", "wb") as file:
        file.write(response.content)


fetchRSS()
