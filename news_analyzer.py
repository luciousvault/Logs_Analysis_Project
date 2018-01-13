import psycopg2
from datetime import datetime

LIST_TABLES = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_CATALOG = 'news' AND TABLE_SCHEMA = 'public';"""

POPULARITY_QUERY = """SELECT title, COUNT(log.id) as popularity
                        FROM log, articles
                        WHERE CONCAT('/article/',articles.slug) = log.path
                        GROUP BY title
                        ORDER BY popularity DESC
                        LIMIT 3;"""

AUTHORS_VIEWS_QUERY = """SELECT authors.name, COUNT(log.id) AS views
                            FROM authors, articles, log
                            WHERE authors.id = articles.author
                            AND CONCAT('/article/',articles.slug) = log.path
                            GROUP BY authors.name
                            ORDER BY views DESC;"""

ERROR_PERCENT_QUERY = """SELECT ROUND(errorCount * 100.0 / dayTotal, 1) AS percent, DAY
                         FROM (SELECT COUNT(status) AS dayTotal ,
                         SUM( CASE WHEN status = '404 NOT FOUND'
                                THEN 1 ELSE 0 END) AS errorCount,
                         DATE(time) AS DAY
                         FROM log GROUP BY DAY) AS temp1
                         ORDER BY percent DESC
                         LIMIT 1;"""


def connect():  # method intended to run "safe" select queries
    try:
        dbconn = psycopg2.connect(dbname="news")
        cursor = dbconn.cursor()
        return dbconn, cursor
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def select_query(query):
    my_dbconn, my_cursor = connect()
    my_cursor.execute(query)
    return my_cursor.fetchall()
    my_dbconn.close()


def print_popular_articles():
    print("3 most popular articles\n")
    popularity_data = select_query(POPULARITY_QUERY)
    article_row_format = '"{}" — {} views'
    for row in popularity_data:
        print(article_row_format.format(row[0], row[1]))


def print_popular_authors():
    print("\nAuthors listed by article views:\n")
    views_data = select_query(AUTHORS_VIEWS_QUERY)
    author_row_format = '{} - {} views'
    for row in views_data:
        print(author_row_format.format(row[0], row[1]))


def print_highest_error_percent():
    print("\nDay with highest percentage of errors:\n")
    error_data = select_query(ERROR_PERCENT_QUERY)
    row = error_data[0]
    print('{} - {}%% errors'.format(row[1].strftime('%b %d, %Y'), row[0]))


if __name__ == '__main__':
    print_popular_articles()
    print_popular_authors()
    print_highest_error_percent()
