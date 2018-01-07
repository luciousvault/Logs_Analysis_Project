import psycopg2

CONN_STRING = """host='localhost' dbname='news' user='vagrant' password='vagrant'"""

LIST_TABLES = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_CATALOG = 'news' AND TABLE_SCHEMA = 'public';"""

# method intended to run "safe" select queries
def sql_select(query):
    try:
        dbconn = psycopg2.connect(dbname='news')
    except:
        print("Failed to connect to the news db")
        return
    cursor = dbconn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
    dbconn.close()

def test_print_tables():
    tables = sql_select(LIST_TABLES)
    print(tables)

if __name__ == '__main__':
    test_print_tables()