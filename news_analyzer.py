import psycopg2

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

def test_print_tables():
    tables = select_query(LIST_TABLES)
    print(tables)

def print_popular_articles():
    popularity_data = select_query(POPULARITY_QUERY)
    print(popularity_data)

def print_popular_authors():
    views_data = select_query(AUTHORS_VIEWS_QUERY)
    print(views_data)

def print_highest_error_percent():
    error_data = select_query(ERROR_PERCENT_QUERY)
    print(error_data)

if __name__ == '__main__':
    test_print_tables()
    print_popular_articles()
    print_popular_authors()
    print_highest_error_percent
