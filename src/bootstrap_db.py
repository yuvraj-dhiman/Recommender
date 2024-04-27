import sqlite3

CONN = sqlite3.connect("news-recommender.db")
cur = CONN.cursor()
cur.execute('''CREATE TABLE users
           (name text, username text not null primary key, pass text, prefs);''')
cur.execute('''CREATE TABLE articles
           (title text, pubDate int not null, text text, data_text text, summary text, author text, link text, hash text not null primary key);''')
cur.execute('''CREATE TABLE sessions
           (id text not null primary key, starttime integer, username text, active int);''')
cur.execute('''CREATE TABLE events
           (id text, time integer, event text, value text);''')
cur.close()
CONN.commit()

