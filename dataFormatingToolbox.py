import sqlite3


def formatDateTime():
    ''' Converts datetime string (DD month_abr YYYY HH:MM:SS) to (YYYY-MM-DD HH:MM:SS) in SQLite DB'''

    months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
              "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    params = []
    connection = sqlite3.connect(
        "/Users/yashjaiswal/Desktop/intern_project/News-Aggregator/RSSFeed.db")
    cur = connection.cursor()
    cursor = cur.execute("SELECT * FROM Blogs;")

    # formats the datetime string and stores it as a tuple in "params" list
    for row in cursor:
        pubDate = row[1]
        day = pubDate[:2]
        month = months[pubDate[3:6]]
        year = pubDate[7:11]
        time = pubDate[12:]
        formatted_datetime = year + "-" + month + "-" + day + " " + time
        params.append((formatted_datetime, row[4]))
    print(params)

    query = """UPDATE Blogs SET PubDate = ? WHERE CommentsURL = ?"""
    cur.executemany(query, params)
    connection.commit()
    connection.close()


def tupleListToDict(rows):
    ''' converts a list of tuples into a list of dictionaries with a title for each field '''

    for i in range(len(rows)):
        rows[i] = list(rows[i])
        rows[i][0] = ["Title", rows[i][0]]
        rows[i][1] = ["PubDate", rows[i][1]]
        rows[i][2] = ["BlogURL", rows[i][2]]
        rows[i][3] = ["Author", rows[i][3]]
        rows[i][4] = ["CommentsURL", rows[i][4]]
        rows[i] = dict(rows[i])

# This function was called only once to convert the DateTime formats in the DB.
# Current input method takes the input in the correct DateTime format so this function need not be called.
# formatDateTime()
