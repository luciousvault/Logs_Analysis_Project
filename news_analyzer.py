import psycopg2

LIST_TABLES = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_CATALOG = 'news' AND TABLE_SCHEMA = 'public';"""
POPULARITY_QUERY = """SELECT title, COUNT(log.id) as popularity
                        FROM log, articles
                        WHERE CONCAT('/article/',articles.slug) = log.path
                        GROUP BY title
                        ORDER BY popularity DESC
                        LIMIT 3;"""

# method intended to run "safe" select queries
def connect():
    try:
        dbconn = psycopg2.connect(dbname="news")
        cursor = dbconn.cursor()
        return dbconn, cursor
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def select_query(query):
    my_dbconn, my_cursor = connect()
    my_cursor.execute(LIST_TABLES)
    my_cursor.execute(POPULARITY_QUERY)
    return my_cursor.fetchall()
    my_dbconn.close()

def test_print_tables():
    tables = sql_select(LIST_TABLES)
    print(tables)

def print_popular_articles():
    popularity_data = sql_select(POPULARITY_QUERY)
    print(popularity_data)

if __name__ == '__main__':
    test_print_tables()
#    print_popular_articles()