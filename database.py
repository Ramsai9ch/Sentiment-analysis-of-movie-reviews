import sqlite3

create_db = """
CREATE TABLE IF NOT EXISTS MOVIE_REVIEWS
(MOVIE_REVIEW         TEXT    NOT NULL,
PREDICTION             TEXT    NOT NULL);
"""

query_for_all = """
SELECT * FROM MOVIE_REVIEWS
"""

insert_query = """
INSERT INTO MOVIE_REVIEWS VALUES (?, ?);
"""

db_name = "movie_reviews_.db"

def create_movie_db():
    conn, cur = opendb(db_name)
    cur.execute(create_db)
    conn.close
    return "DB Created Successfully!"

def opendb(db_name):
    try:
        conn = sqlite3.connect(db_name)
    except sqlite3.Error:
        return False
    cur = conn.cursor()
    return [conn, cur]


def insert_review(review, prediction):
    conn, cur = opendb(db_name)
    res = cur.execute(insert_query, (review, prediction))
    conn.commit()
    conn.close
    return "Inserted Successfully!"    


def query_all():
    conn, cur = opendb(db_name)
    val= cur.execute(query_for_all)
    conn.close
    return val