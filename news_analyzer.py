#!/usr/bin/env python3
import psycopg2
from datetime import datetime


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

ERROR_PERCENT_QUERY = """SELECT ROUND(errorCount * 100.0 / dayTotal, 1) 
                                    AS percent, 
                                DAY
                         FROM (SELECT COUNT(status) AS dayTotal ,
                         SUM( CASE WHEN status = '404 NOT FOUND'
                                THEN 1 ELSE 0 END) AS errorCount,
                         DATE(time) AS DAY
                         FROM log GROUP BY DAY) AS temp1
                         WHERE ROUND(errorCount * 100.0 / dayTotal, 1) > 1.0
                         ORDER BY percent DESC;"""

def get_query_results(query):
    """method intended to run "safe" select queries"""
    try:
        dbconn = psycopg2.connect(database="news")
        cursor = dbconn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        dbconn.close()
        return result
    except Exception as e:
        print(e)
        exit(1)



def print_popular_articles():
    print("3 most popular articles\n")
    popularity_data = get_query_results(POPULARITY_QUERY)
    article_row_format = '"{}" — {} views'
    for title, views in popularity_data:
        print(article_row_format.format(title, views))


def print_popular_authors():
    print("\nAuthors listed by article views:\n")
    views_data = get_query_results(AUTHORS_VIEWS_QUERY)
    author_row_format = '{} - {} views'
    for author, views in views_data:
        print(author_row_format.format(author, views))


def print_highest_error_percent():
    print("\nDay with highest percentage of errors:\n")
    error_data = get_query_results(ERROR_PERCENT_QUERY)
    row = error_data[0]
    for percent, day in error_data:
        print('{} - {}% errors'.format(day.strftime('%b %d, %Y'), percent))


if __name__ == '__main__':
    print_popular_articles()
    print_popular_authors()
    print_highest_error_percent()
